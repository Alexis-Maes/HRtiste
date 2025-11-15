# claude_api/client.py

from typing import Literal, Optional
from anthropic import AsyncAnthropic
from .config import ANTHROPIC_API_KEY


ClaudeModel = Literal["claude-sonnet-4-5", "claude-haiku-4-5"]

_client = AsyncAnthropic(api_key=ANTHROPIC_API_KEY)


async def ask_raw(
    prompt: str,
    model: ClaudeModel = "claude-sonnet-4-5",
    max_tokens: int = 800,
    system_prompt: Optional[str] = None,
    temperature: Optional[float] = None,
    top_p: Optional[float] = None,
    raw: bool = False,
):
    """
    Send a raw text prompt to Claude and return the response as plain text.

    Args:
        prompt: User content to send to Claude.
        model: Claude model name.
        max_tokens: Maximum number of tokens to generate.
        system_prompt: Optional system prompt to steer behavior.
        temperature: Optional temperature for sampling.
        top_p: Optional top-p sampling.
        raw: If True, return the full response object instead of plain text.

    Returns:
        str or full response object depending on `raw`.
    """

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

    # Top-level system prompt (this is the correct way for Anthropic)
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
