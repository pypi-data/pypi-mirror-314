"""Interactive chat command."""

from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

from llmling.core.log import get_logger
from rich.console import Console
from rich.live import Live
from rich.markdown import Markdown
import typer as t

from llmling_agent.cli import resolve_agent_config


if TYPE_CHECKING:
    from pydantic_ai import messages

    from llmling_agent.runners import SingleAgentRunner

console = Console()
logger = get_logger(__name__)


async def chat_session(
    runner: SingleAgentRunner[str],
    history: list[messages.Message] | None = None,
    stream: bool = False,
) -> None:
    """Run interactive chat session with agent."""
    print(f"\nStarted chat with {runner.agent_config.name or 'agent'}")
    print("Type 'exit' or press Ctrl+C to end the conversation\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (KeyboardInterrupt, EOFError):
            break

        if not user_input or user_input.lower() == "exit":
            break

        try:
            console.print("\nAgent:", style="bold blue")
            if stream:
                stream_ctx = runner.agent.run_stream(user_input, message_history=history)
                with Live("", console=console, vertical_overflow="visible") as live:
                    async with await stream_ctx as result:
                        async for message in result.stream():
                            live.update(Markdown(str(message)))
                    history = result.new_messages()
            else:
                result = await runner.agent.run(user_input, message_history=history)
                console.print(Markdown(str(result.data)))
                history = result.new_messages()
            print()  # Empty line for readability

        except Exception as e:  # noqa: BLE001
            console.print(f"\nError: {e}", style="bold red")
            import traceback

            traceback.print_exc()
            continue


def chat_command(
    agent_name: str = t.Argument(help="Name of agent to chat with"),
    config: str | None = t.Option(
        None,
        "--config",
        "-c",
        help="Override agent configuration path",
    ),
    model: str | None = t.Option(
        None,
        "--model",
        "-m",
        help="Override agent's model",
    ),
    stream: bool = t.Option(
        False,
        "--stream",
        "-s",
        help="Stream the response token by token",
    ),
) -> None:
    """Start interactive chat session with an agent.

    Example:
        llmling-agent chat myagent
        llmling-agent chat myagent --model gpt-4
    """
    from llmling_agent.models import AgentDefinition
    from llmling_agent.runners import SingleAgentRunner

    try:
        # Resolve configuration
        try:
            config_path = resolve_agent_config(config)
        except ValueError as e:
            msg = str(e)
            raise t.BadParameter(msg) from e

        # Load agent definition
        agent_def = AgentDefinition.from_file(config_path)
        if agent_name not in agent_def.agents:
            msg = f"Agent '{agent_name}' not found in configuration"
            raise t.BadParameter(msg)  # noqa: TRY301

        # Initialize runner
        agent_config = agent_def.agents[agent_name]
        if model:
            agent_config.model = model  # type: ignore

        async def run_chat() -> None:
            runner = SingleAgentRunner[str](
                agent_config=agent_config,
                response_defs=agent_def.responses,
            )
            async with runner:
                await chat_session(runner, stream=stream)

        asyncio.run(run_chat())

    except t.Exit:
        raise
    except KeyboardInterrupt:
        print("\nChat session ended.")
    except Exception as e:
        print(f"Error: {e}")
        raise t.Exit(1) from e


if __name__ == "__main__":
    chat_command()
