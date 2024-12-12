from __future__ import annotations

from typing import TYPE_CHECKING

from llmling import Config
from llmling.config.models import GlobalSettings, LLMCapabilitiesConfig
from llmling.config.runtime import RuntimeConfig
from pydantic_ai.models.test import TestModel
import pytest

from llmling_agent.models import (
    AgentConfig,
    AgentDefinition,
    ResponseDefinition,
    ResponseField,
)
from llmling_agent.runners import AgentOrchestrator, AgentRunConfig, SingleAgentRunner
from llmling_agent.runners.orchestrator import AgentNotFoundError, NoPromptsError


if TYPE_CHECKING:
    from collections.abc import AsyncGenerator


@pytest.fixture
def test_model() -> TestModel:
    """Create a TestModel that returns simple text responses."""
    return TestModel(custom_result_text="Test response", call_tools=[])


@pytest.fixture
def basic_response_def() -> dict[str, ResponseDefinition]:
    """Create basic response definitions for testing."""
    response = ResponseField(type="str", description="Test message")
    desc = "Basic test result"
    definition = ResponseDefinition(description=desc, fields={"message": response})
    return {"BasicResult": definition}


@pytest.fixture
async def runtime() -> AsyncGenerator[RuntimeConfig, None]:
    """Create a runtime configuration for testing."""
    caps = LLMCapabilitiesConfig(load_resource=False, get_resources=False)
    global_settings = GlobalSettings(llm_capabilities=caps)
    config = Config(global_settings=global_settings)
    runtime = RuntimeConfig.from_config(config)
    await runtime.__aenter__()
    yield runtime
    await runtime.__aexit__(None, None, None)


@pytest.mark.asyncio
async def test_single_agent_runner_basic(
    basic_agent_config: AgentConfig,
    basic_response_def: dict[str, ResponseDefinition],
    runtime: RuntimeConfig,
) -> None:
    """Test basic SingleAgentRunner functionality."""
    async with SingleAgentRunner[str](
        agent_config=basic_agent_config,
        response_defs=basic_response_def,
    ) as runner:
        # Override the model with TestModel
        runner.agent._pydantic_agent.model = TestModel()

        result = await runner.run("Hello!")
        assert isinstance(result.data, str)
        assert result.data  # should not be empty


@pytest.mark.asyncio
async def test_single_agent_runner_conversation(
    basic_agent_config: AgentConfig,
    basic_response_def: dict[str, ResponseDefinition],
) -> None:
    """Test conversation flow with SingleAgentRunner."""
    async with SingleAgentRunner[str](
        agent_config=basic_agent_config,
        response_defs=basic_response_def,
    ) as runner:
        # Override with TestModel that returns specific responses
        runner.agent._pydantic_agent.model = TestModel(custom_result_text="Test response")

        results = await runner.run_conversation(["Hello!", "How are you?"])
        assert len(results) == 2  # noqa: PLR2004
        assert all(r.data == "Test response" for r in results)


@pytest.mark.asyncio
async def test_orchestrator_single_agent(
    basic_agent_config: AgentConfig,
    basic_response_def: dict[str, ResponseDefinition],
) -> None:
    """Test orchestrator with single agent."""
    agents = {"test_agent": basic_agent_config}
    agent_def = AgentDefinition(responses=basic_response_def, agents=agents)

    config = AgentRunConfig(agent_names=["test_agent"], prompts=["Hello!"])

    orchestrator = AgentOrchestrator(agent_def=agent_def, run_config=config)
    results = await orchestrator.run()

    # For single agent, results should be a list of RunResults
    assert isinstance(results, list)
    assert len(results) == 1
    assert isinstance(results[0].data, str)


@pytest.mark.asyncio
async def test_orchestrator_multiple_agents(
    basic_agent_config: AgentConfig,
    basic_response_def: dict[str, ResponseDefinition],
    test_model: TestModel,
) -> None:
    """Test orchestrator with multiple agents."""
    test_config = basic_agent_config.model_copy(update={"model": test_model})
    agents = {"agent1": test_config, "agent2": test_config}
    agent_def = AgentDefinition(responses=basic_response_def, agents=agents)

    config = AgentRunConfig(agent_names=["agent1", "agent2"], prompts=["Hello!"])

    orchestrator = AgentOrchestrator(agent_def=agent_def, run_config=config)
    results = await orchestrator.run()

    assert isinstance(results, dict)
    assert len(results) == 2  # noqa: PLR2004
    assert all(
        isinstance(r[0].data, str) and r[0].data == "Test response"
        for r in results.values()
    )


@pytest.mark.asyncio
async def test_orchestrator_validation(
    basic_agent_config: AgentConfig,
    basic_response_def: dict[str, ResponseDefinition],
) -> None:
    """Test orchestrator validation."""
    agents = {"test_agent": basic_agent_config}
    agent_def = AgentDefinition(responses=basic_response_def, agents=agents)

    # Test no prompts first
    config = AgentRunConfig(agent_names=["test_agent"], prompts=[])
    orchestrator = AgentOrchestrator(agent_def, config)
    with pytest.raises(NoPromptsError):
        orchestrator.validate()

    # Then test missing agent
    config = AgentRunConfig(agent_names=["nonexistent"], prompts=["Hello!"])
    orchestrator = AgentOrchestrator(agent_def, config)
    with pytest.raises(AgentNotFoundError):
        orchestrator.validate()
