import asyncio
import os
import sys

# Add the cached site-packages path to sys.path so we can import google.antigravity
site_packages = "/Users/ivanleo/.cache/uv/environments-v2/antigravity-sdk-runner-e7d12527c06fb501/lib/python3.13/site-packages"
if site_packages not in sys.path:
    sys.path.insert(0, site_packages)

from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.hooks import policy
from google.antigravity.types import (
    GeminiConfig,
    GenerationConfig,
    ModelConfig,
    ModelEntry,
    StepStatus,
)

async def main():
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        print("Error: GEMINI_API_KEY environment variable not set")
        return

    model_entry = ModelEntry(
        name="gemini-3.5-flash",
        generation=GenerationConfig(),
    )
    gemini_config = GeminiConfig(
        api_key=api_key,
        models=ModelConfig(default=model_entry)
    )

    # Use the tasks/grep/q-1-managed-agents-security/environment/docs directory as documentation
    config = LocalAgentConfig(
        gemini_config=gemini_config,
        policies=[policy.allow_all()],
        workspaces=["/Users/ivanleo/Documents/coding/agent-search/tasks/grep/q-1-managed-agents-security/environment"]
    )

    print("Starting agent...")
    async with Agent(config) as agent:
        # We ask a simple instruction that requires reading a file
        instruction = (
            "Read the file `/docs/agent-environment.md` inside your workspace "
            "and answer what the idle timeout is. "
            "Write the answer to `output.txt` at the root of the workspace."
        )
        print(f"Sending instruction: {instruction}")
        await agent.conversation.send(instruction)

        async for step in agent.conversation.receive_steps():
            print(f"\n--- STEP: source={step.source}, type={step.type}, status={step.status} ---")
            if step.content:
                print(f"Content: {step.content}")
            if step.thinking:
                print(f"Thinking: {step.thinking}")
            if step.error:
                print(f"Error: {step.error}")
            if step.tool_calls:
                print("Tool Calls:")
                for tc in step.tool_calls:
                    print(f"  ID={tc.id}, Name={tc.name}, Args={tc.args}")
                    tc_output = getattr(tc, "output", None)
                    if tc_output:
                        print(f"  Output: {tc_output}")

if __name__ == "__main__":
    asyncio.run(main())
