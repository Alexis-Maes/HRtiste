from typing import Type, TypeVar, Union

from anthropic import AsyncAnthropic
from anthropic.types import Message
from pydantic import BaseModel
import base64

from services.config_service import ConfigService
from models.db_models import PDFModel

Model = TypeVar("Model", bound=BaseModel)

# =================================== #
PDF_PATH = ""
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

            
        completion = await self.client.messages.create(
            model=model, messages=[{"role": "user", "content": inputs}], max_tokens=max_tokens, system=system_prompt
        )
        return completion

    async def structured_completion(
        self,
        inputs: str,
        output_model: Type[Model],
        pdf_data: Union[bytes, str, None] = None,
        model: str = "claude-sonnet-4-5"
    ) -> str:
        """BG: tu vas devoir creer ton model pydantic et gerer les pdf"""

        content = [{
            "type": "text",
            "text": inputs
        }]


        # Encoder le PDF en base64 #
        if pdf_data:
            if isinstance(pdf_data, str):
                pdf_bytes = base64.standard_b64decode(pdf_data)
            else:
                pdf_bytes = pdf_data
            pdf_base64 = base64.standard_b64encode(pdf_bytes).decode("utf-8")

            content.append({
                "type": "document",
                "source": {
                    "type": "base64",
                    "media_type": "application/pdf",
                    "data": pdf_base64
                }
            })

        # Gérer le schéma de sortie #
        output_json_schema = output_model.model_json_schema()
        output_json_schema = {
            "properties": {attribute: {'type': details['type']} for attribute, details in output_json_schema['properties'].items()},
            "required": output_json_schema.get("required", []),
        }

        response = await self.client.beta.messages.create(
            model=model,
            max_tokens=1024,
            betas=["structured-outputs-2025-11-13"],
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ],
            output_format={
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    **output_json_schema,
                    "additionalProperties": False
                }
            }
        )

        return response.content[0].text






claude_service = ClaudeService()


async def main() -> None:


    message = await claude_service.structured_completion(
        inputs="Hello, world!",
        pdf_path=PDF_PATH,
        ouput_model=PDFModel
    )
    print(message)


if __name__ == "__main__":
    import asyncio

    asyncio.run(main())
