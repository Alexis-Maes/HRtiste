from typing import Type, TypeVar

from anthropic import AsyncAnthropic
from anthropic.types import Message
from pydantic import BaseModel

from services.config_service import ConfigService

Model = TypeVar("Model", bound=BaseModel)


class ClaudeService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=ConfigService.anthropic_api_key)

    async def completion(
        self,
        inputs: str,
        model: str = "claude-sonnet-4-5",
        system_prompt: str | None = None,
        max_tokens: int = 800,
    ) -> Message:
        if system_prompt:
            messages = [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": inputs},
            ]
        else:
            messages = [{"role": "user", "content": inputs}]
        completion = await self.client.messages.create(
            model=model, messages=messages, max_tokens=max_tokens
        )
        return completion

    async def structured_completion(
        self, inputs: str, ouput_model: Type[Model], model: str = "claude-sonnet-4-5"
    ):
        """BG: tu vas devoir creer ton model pydantic et gerer les pdf"""
        pass


claude_service = ClaudeService()


async def main() -> None:
    message = await claude_service.completion("Hello, world!")
    print(message.content)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
