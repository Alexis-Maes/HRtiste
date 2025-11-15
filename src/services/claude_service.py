import base64
from typing import Type, TypeVar, Union
from pathlib import Path

from anthropic import AsyncAnthropic, transform_schema
from anthropic.types import Message
from pydantic import BaseModel

from services.config_service import ConfigService
from models.db_models import PDFModel, Interview

Model = TypeVar("Model", bound=BaseModel)

# =================================== #
PDF_PATH = Path(r"C:\Users\gasti\Downloads\CVAlexandreGastinel.pdf")
# Put your own PDF path
# =================================== #


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
        if system_prompt is None:
            system_prompt = ""
        completion = await self.client.messages.create(
            model=model,
            messages=[{"role": "user", "content": inputs}],
            max_tokens=max_tokens,
            system=system_prompt,
        )
        return completion

    async def structured_completion(
        self,
        inputs: str,
        output_model: Type[Model],
        pdf_data: Union[Path, bytes, str, None] = None,
        model: str = "claude-sonnet-4-5"
    ) -> str:
        """BG: tu vas devoir creer ton model pydantic et gerer les pdf"""

        content = [{"type": "text", "text": inputs}]

        # Encoder le PDF en base64 #
        if pdf_data:
            if isinstance(pdf_data, Path):
                with open(pdf_data, "rb") as f:
                    pdf_bytes = f.read()
            elif isinstance(pdf_data, str):
                pdf_bytes = base64.standard_b64decode(pdf_data)
            else:
                pdf_bytes = pdf_data
            pdf_base64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

            content.append(
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_base64,
                    },
                }
            )


        response = await self.client.beta.messages.create(
            model=model,
            max_tokens=1024,
            betas=["structured-outputs-2025-11-13"],
            messages=[{"role": "user", "content": content}],
            output_format={
                "type": "json_schema",
                "schema": transform_schema(output_model)
            }
        )

        return response.content[0].text


claude_service = ClaudeService()


async def main() -> None:
    message = await claude_service.structured_completion(
        inputs="Analyse this cv",
        output_model=PDFModel,
        pdf_data=PDF_PATH,
    )
    print(message)





if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
