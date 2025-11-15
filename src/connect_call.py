from faster_whisper import WhisperModel
from dotenv import load_dotenv
from services.claude_service import claude_service
from services.config_service import ConfigService

load_dotenv()
# ⚡ Config clés API
model = WhisperModel("small", device="cpu")


# === 2️⃣ Transcrire avec Whisper ===
def transcribe_audio(audio_path: str):
    segments, info = model.transcribe(audio_path, beam_size=5)
    # Concaténer tous les segments pour faire un texte complet
    text = "".join([segment.text for segment in segments])
    return text

# === 3️⃣ Générer le feedback avec Claude ===
async def generate_feedback(transcript):
    system_prompt = f"""
Tu es un recruteur senior spécialisé dans l'analyse d'entretiens.


Ta mission :
- Extraire les informations essentielles
- Produire un feedback structuré exploitable par une équipe RH
- Être neutre et non biaisé
- Ajouter une phrase d'analyse de la qualité de la performance du recruteur

Format attendu :
[Synthèse] : 5-7 lignes
[Points forts] : bullet points
[Points d'attention] : bullet points
"""
    response = await claude_service.completion(inputs = transcript, system_prompt= system_prompt)
    return response

# === 4️⃣ Pipeline complet ===
async def process_audio_feedback(wav_path):
    transcript = transcribe_audio(wav_path)
    feedback = await generate_feedback(transcript)
    return feedback


import asyncio
feedback = asyncio.run(process_audio_feedback("src/data/test.wav"))
print("\n===== FEEDBACK RH =====\n")
print(feedback.content)
