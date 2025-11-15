import asyncio
from ClaudeAPI import ask_raw

def main():
    print("Hello from hrtiste!")
    prompt = "Define your prompt here."
    asyncio.run(runAPI(prompt))


async def runAPI(prompt: str = ""):
    response = await ask_raw("Give me 3 ideas for HR innovation.")
    print("Claude response:\n", response)


if __name__ == "__main__":
    main()
