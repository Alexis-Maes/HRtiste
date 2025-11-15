from typing import Type, TypeVar

from anthropic import AsyncAnthropic
from anthropic.types import Message
from pydantic import BaseModel
import base64

from services.config_service import ConfigService
from models.db_models import PDFModel

Model = TypeVar("Model", bound=BaseModel)



# =========================================== #
PDF_PATH = r"C:\Users\gasti\Downloads\CVAlexandreGastinel.pdf"
# =========================================== #


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
        pdf_path: str,
        ouput_model: Type[Model],
        model: str = "claude-sonnet-4-5"
    ) -> str:
        """BG: tu vas devoir creer ton model pydantic et gerer les pdf"""


        with open(pdf_path, "rb") as f:
            pdf_data = base64.standard_b64encode(f.read()).decode("utf-8")

        output_json_schema = ouput_model.model_json_schema()
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
                    "content": [
                        {
                            "type": "document",
                            "source": {
                                "type": "base64",
                                "media_type": "application/pdf",
                                "data": pdf_data
                            }
                        },
                        {
                            "type": "text",
                            "text": inputs
                        }
                    ]
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
