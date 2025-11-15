# claude_api/client.py

from typing import Literal, Optional
from anthropic import AsyncAnthropic
from .config import ANTHROPIC_API_KEY

ClaudeModel = Literal["claude-sonnet-4-5", "claude-haiku-4-5"] # Define supported models

_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)

# Wrapper around the Anthropic async client to send a message and get a response
async def ask_raw(
    prompt: str,
    model: ClaudeModel = "claude-sonnet-4-5",
    max_tokens: int = 800,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    raw: bool = False,
):
    # Build the core payload
    kwargs = {
        "model": model,
        "max_tokens": max_tokens,
        "messages": [
            {
                "role": "user",
                "content": prompt,
            }
        ],
    }

    # Top-level system prompt
    if system_prompt:
        kwargs["system"] = system_prompt

    # Optional sampling params
    if temperature is not None:
        kwargs["temperature"] = temperature
    if top_p is not None:
        kwargs["top_p"] = top_p

    msg = await _client.messages.create(**kwargs)

    if raw:
        return msg

    # Merge all text blocks into a single string
    blocks = []
    for block in msg.content:
        blocks.append(getattr(block, "text", str(block)))

    return "\n".join(blocks)
