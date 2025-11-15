from mistralai import Mistral

from services.config_service import ConfigService


class EmbeddingService:
    def __init__(self):
        self.client = Mistral(api_key=ConfigService.mistral_api_key)

    async def get_embedding(self, text: str):
        response = await self.client.embeddings.create_async(
            model="mistral-embed", inputs=[text]
        )
        return response.data[0].embedding


embedding_service = EmbeddingService()
