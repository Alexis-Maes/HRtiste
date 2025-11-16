import os
import asyncio
from services.upload_cv import cv_to_db, MissingRequiredFieldException
from config import Paths


# ============================ #
dossier_racine = Paths.CVS_DIR
# ============================ #


async def initialize_db_with_cvs() -> None:
    for racine, dossiers, fichiers in os.walk(dossier_racine):
        for fichier in fichiers:
            if fichier.endswith(".pdf"):
                chemin_complet = os.path.join(racine, fichier)
                print(f"Traitement du cv: {chemin_complet}")
                with open(chemin_complet, "rb") as f:
                    pdf_bytes = f.read()
                    try:
                        await cv_to_db(pdf_bytes)
                    except MissingRequiredFieldException as e:
                        print(f"Erreur lors du traitement du CV {chemin_complet} : {e}")
                        continue

            

async def main():
    await initialize_db_with_cvs()


if __name__ == "__main__":
    asyncio.run(main())

