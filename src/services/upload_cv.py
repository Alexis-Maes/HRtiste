import json
from services.db_service import db_service
from services.claude_service import claude_service
from models.db_models import Candidate, PDFModel
from fastapi import HTTPException
from pathlib import Path
import base64
from profile_manager import update_description

# =================================== #
PDF_PATH = Path(r"C:\Users\gasti\Downloads\CVAlexandreGastinel.pdf")
# Put your own PDF path
# =================================== #



async def cv_to_db(pdf_bytes: bytes) -> None:
    try:
        result = await claude_service.structured_completion(
            inputs="Extrait les informations du candidat depuis ce CV.",
            output_model=PDFModel,
            pdf_data=pdf_bytes,
            model="claude-sonnet-4-5"
        )
        print(result)
        candidate = Candidate.model_validate(json.loads(result))
        candidate = await update_description(candidate)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Erreur lors du traitement du CV : {str(e)}")

    await db_service.add_element(candidate)



async def main():
    content=PDF_PATH.read_bytes()
    await cv_to_db(content)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
    

