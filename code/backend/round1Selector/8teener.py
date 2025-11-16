import asyncio
import os
from dotenv import load_dotenv
from pathlib import Path

from semantic_kernel.agents import Agent, ChatCompletionAgent, SequentialOrchestration
from semantic_kernel.connectors.ai.open_ai import AzureChatCompletion
from semantic_kernel.contents import ChatMessageContent
from semantic_kernel.agents.runtime import InProcessRuntime

# Load environment variables from .env file
load_dotenv(dotenv_path=Path(__file__).parent.parent.parent.parent / '.env')


def get_agents() -> list[Agent]:
    """Return a list of agents that will participate in the sequential orchestration.

    Feel free to add or remove agents.
    """
    # Azure OpenAI configuration - replace these with your actual values
    azure_endpoint = os.getenv("OPENAI_ENDPOINT")
    azure_api_key = os.getenv("OPENAI_API_KEY")
    deployment_name = os.getenv("OPENAI_DEPLOYMENT")
    api_version = os.getenv("OPENAI_API_VERSION")

    print(f"Using Azure OpenAI endpoint: {azure_endpoint} with deployment: {deployment_name} ")
    
    concept_extractor_agent = ChatCompletionAgent(
        name="ConceptExtractorAgent",
        instructions=(
            "You are a marketing analyst. Given a product description, identify:\n"
            "- Key features\n"
            "- Target audience\n"
            "- Unique selling points\n\n"
        ),
        service=AzureChatCompletion(
            service_id="concept_extractor_service",
            deployment_name=deployment_name,
            endpoint=azure_endpoint,
            api_key=azure_api_key,
            api_version=api_version,
        ),
    )
    writer_agent = ChatCompletionAgent(
        name="WriterAgent",
        instructions=(
            "You are a marketing copywriter. Given a block of text describing features, audience, and USPs, "
            "compose a compelling marketing copy (like a newsletter section) that highlights these points. "
            "Output should be short (around 150 words), output just the copy as a single text block."
        ),
        service=AzureChatCompletion(
            service_id="writer_service",
            deployment_name=deployment_name,
            endpoint=azure_endpoint,
            api_key=azure_api_key,
            api_version=api_version,
        ),
    )
    format_proof_agent = ChatCompletionAgent(
        name="FormatProofAgent",
        instructions=(
            "You are an editor. Given the draft copy, correct grammar, improve clarity, ensure consistent tone, "
            "give format and make it polished. Output the final improved copy as a single text block."
        ),
        service=AzureChatCompletion(
            service_id="format_proof_service",
            deployment_name=deployment_name,
            endpoint=azure_endpoint,
            api_key=azure_api_key,
            api_version=api_version,
        ),
    )

    # The order of the agents in the list will be the order in which they are executed
    return [concept_extractor_agent, writer_agent, format_proof_agent]


def agent_response_callback(message: ChatMessageContent) -> None:
    """Observer function to print the messages from the agents."""
    print(f"# {message.name}\n{message.content}")


async def main():
    """Main function to run the agents."""
    # 1. Create a sequential orchestration with multiple agents and an agent
    #    response callback to observe the output from each agent.
    agents = get_agents()
    sequential_orchestration = SequentialOrchestration(
        members=agents,
        agent_response_callback=agent_response_callback,
    )

    # 2. Create a runtime and start it
    runtime = InProcessRuntime()
    runtime.start()

    # 3. Invoke the orchestration with a task and the runtime
    orchestration_result = await sequential_orchestration.invoke(
        task="An eco-friendly stainless steel water bottle that keeps drinks cold for 24 hours",
        runtime=runtime,
    )

    # 4. Wait for the results
    value = await orchestration_result.get(timeout=20)
    print(f"***** Final Result *****\n{value}")

    # 5. Stop the runtime when idle
    await runtime.stop_when_idle()

if __name__ == "__main__":
    asyncio.run(main())