from fastapi import APIRouter, HTTPException, UploadFile, File

router = APIRouter(tags=["Interviews_audio"])

from src.services.db_service import db_service
from src.models.db_models import Interview
from sqlmodel import select

from src.services.claude_service import claude_service
from src.services.elevenlabs_service import eleven_labs_service

@router.post("/interviews_audio", response_model=str)
async def process_audio_feedback(file: UploadFile = File(...)):

    if not file.content_type.startswith("audio/"):
        raise HTTPException(400, "Le fichier doit être un fichier audio")
    
    audio_bytes = await file.read()

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
    
    
    transcript = await eleven_labs_service.transcript(filename = file.filename, audio_bytes = audio_bytes)
    feedback = await generate_feedback(transcript)
    return (feedback.content[0].text)
