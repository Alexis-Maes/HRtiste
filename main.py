# main.py

import asyncio # Async support
from claudeAPI import ask_raw # Claude API wrapper

# Configuration constants for the Claude API requests

SYSTEM_PROMPT = "PUT YOUR SYSTEM PROMPT HERE"
PROMPT="PUT YOUR PROMPT HERE"
MODEL = "claude-sonnet-4-5" # Model to use : "claude-sonnet-4-5", "claude-haiku-4-5"
MODEL_TEMP = 0.2
MAX_TOKENS = 800

async def run_api(prompt: str) -> str:
    """
    Execute an LLM request using the Claude wrapper (ask_raw) and return the result.
    """

    response = await ask_raw(
        prompt=prompt,
        system_prompt=SYSTEM_PROMPT,
        max_tokens=MAX_TOKENS,
        temperature=MODEL_TEMP,
        top_p=None,
    )

    return response


async def main() -> None:
    print ("=== Sending request to Claude API ===")
    result = await run_api(PROMPT) # Call the async function

    print("\n=== Claude Response ===\n")
    print(result)


if __name__ == "__main__":
    asyncio.run(main())
