from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from services.claude_service import claude_service
from services.config_service import ConfigService
import os

load_dotenv()
client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))


# Transcription
def transcribe_audio(file_path: str) -> str:
    with open(file_path, "rb") as f:
        result = client.speech_to_text.convert(
            file=f,
            model_id= "scribe_v2"
        )

    return result.text

# generate feedback
async def generate_feedback(transcript):
    system_prompt = f"""
Tu es un recruteur senior spécialisé dans l'analyse d'entretiens.


Ta mission :
- Extraire les informations essentielles
- Produire un feedback structuré exploitable par une équipe RH
- Être neutre et non biaisé
- Analyser le comportement du recruteur

Format attendu :
[Synthèse] : 5-7 lignes
[Points forts] : bullet points - quelques mots clés
[Points d'attention] : bullet points - quelques mots clés
[Analyse du recruteur] : Une phrase d'analyse de la qualité de performance du recruteur
"""
    response = await claude_service.completion(inputs = transcript, system_prompt= system_prompt)
    return response

#pipeline
async def process_audio_feedback(wav_path):
    transcript = transcribe_audio(wav_path)
    feedback = await generate_feedback(transcript)
    return feedback

#pour run
#pas oblige de mettre un .wav
"""
import asyncio
feedback = asyncio.run(process_audio_feedback("src/data/test.wav"))
print("\n===== FEEDBACK RH =====\n")
print(feedback.content[0].text)
"""