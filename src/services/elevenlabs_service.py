from elevenlabs import ElevenLabs
from services.config_service import ConfigService


class ElevenLabsService:
    def __init__(self):
        self.client = ElevenLabs(api_key=ConfigService.elevenlabs_api_key)

    async def transcript(
        self,
        filename: str,
        audio_bytes : bytes,
        model : str = "scribe_v2"
    ) -> str:

            
    
        result = self.client.speech_to_text.convert(
        file=(filename,audio_bytes),
        model_id= model
        )

        return result.text
    
eleven_labs_service = ElevenLabsService()