import json
import random
from services.db_service import db_service
from services.claude_service import claude_service
from models.db_models import Candidate, PDFModel
from fastapi import HTTPException
from pathlib import Path
from profile_manager import update_description


# =================================== #
PDF_PATH = Path(r"C:\Users\gasti\Downloads\CVAlexandreGastinel.pdf")
# Put your own PDF path
# =================================== #



class MissingRequiredFieldException(Exception):
    pass


prenoms = [
    "Kenza", "Eren", "Soraya", "Ayaan", "Zahra", "Eline", "Soren", "Amani",
    "Freya", "Idris", "Thiago", "Amelie", "Sienna", "Maeva", "Kenzo", "Liv",
    "Cyprien", "Chahinez", "Tanguy", "Lise", "Yann", "Darius", "Élodie", "Imran",
    "Mira", "Yanis", "Nino", "Eden", "Malo", "Lény", "Lohan", "Sélim", "Youssef",
    "Jaden", "Malcolm", "Aaliyah", "Cédric", "Safiya", "Timothé", "Élias", "Nassim",
    "Théodore", "Bilal", "Sofiane", "Yann", "Sami", "Raphaël", "Lény", "Lohan",
    "Kévin", "Lylou", "Nael", "Sélim", "Sofiane", "Youssef", "Jaden", "Malcolm",
    "Aaliyah", "Cyprien", "Chahinez", "Tanguy", "Lise", "Yann", "Darius", "Élodie",
    "Imran", "Mira", "Yanis", "Nino", "Eden", "Malo", "Lény", "Lohan", "Sélim",
    "Kévin", "Lylou", "Nael", "Sofiane", "Théodore", "Bilal", "Safiya", "Timothé",
    "Céleste", "Zahra", "Eline", "Soren", "Amani", "Freya", "Idris", "Thiago",
    "Sienna", "Maeva", "Kenzo", "Liv", "Antoine", "Safiya", "Malcolm", "Aaliyah",
    "Cédric", "Inaya", "Jaden", "Lylou", "Imran", "Sofia", "Yann", "Lise", "Sélim",
    "Aya", "Luce", "Sami", "Raphaël", "Lény", "Lohan", "Kévin", "Lylou", "Nael",
    "Emma", "Liam", "Aïcha", "Mohamed", "Sophie", "Lucas", "Maria", "Carlos",
    "Yasmine", "Thomas", "Anna", "Alexander", "Fatima", "Amir", "Chloe", "Ethan",
    "Mei", "Wei", "Olivia", "Noah", "Aya", "Kofi", "Inaya", "Leo", "Sofia", "Mateo",
    "Elijah", "Zoe", "Hugo", "Camille", "Javier", "Isabella", "Rafael", "Lena",
    "Finn", "Mila", "Kai", "Sana", "Gabriel", "Leila", "Adrian", "Nina", "Julian",
    "Elena", "Diego", "Aisha", "Samuel", "Layla", "Enzo", "Manon", "Luca", "Ava",
    "Rayan", "Iman", "Louis", "Jade", "Nolan", "Sara", "Eva", "Adam", "Lina", "Théo",
    "Inès", "Arthur", "Léa", "Elias", "Naomi", "Simon", "Alice", "Victor", "Rose",
    "Paul", "Lola", "Antonio", "Giovanna", "Ibrahim", "Yara", "Maxime", "Clara",
    "Nathan", "Léonie", "Tom", "Luna", "Aaron", "Maya", "Dylan", "Chloé", "Ruben",
    "Célia", "Evan", "Lyla", "Malik", "Amina", "Jules", "Louise", "Sacha", "Léana"
]
noms = [
    "Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand",
    "Leroy", "Moreau", "Simon", "Laurent", "Lefèvre", "Michel", "Garcia", "David",
    "Bertrand", "Roux", "Vincent", "Fournier", "Morel", "Girard", "Andre", "Lefebvre",
    "Merci", "Bonnet", "Francois", "Martinez", "Legrand", "Garnier", "Faure", "Rousseau",
    "Blanc", "Guerin", "Muller", "Henry", "Roussel", "Nicolas", "Perrot", "Dumont",
    "Lambert", "Dupont", "Carre", "Brun", "Noir", "Leclerc", "Gauthier", "Barbier",
    "Schmitt", "Lopez", "Diaz", "Rodriguez", "Bailly", "Cohen", "Perrier", "Morin",
    "Aubry", "Gillet", "Lecomte", "Marchand", "Duval", "Denis", "Dufour", "Le Goff",
    "Le Roux", "Le Gall", "Colin", "Lucas", "Meunier", "Chevalier", "Adam", "Blanchard",
    "Fleury", "Mathieu", "Carpentier", "Charbonnier", "Germain", "Boyer", "Fernandez",
    "Raymond", "Joly", "Giraud", "Vasseur", "Arnaud", "Renaud", "Dupond", "Roy",
    "Lemaire", "Gaillard", "Perrin", "Leveque", "Bertrand", "Monnier", "Besson", "Jacquet",
    "Benoit", "Meyer", "Dupuis", "Bourgeois", "Gomez", "Pascal", "Picard", "Guillot",
    "Weber", "Vidal", "Lejeune", "Barre", "Albert", "Renard", "Leconte", "Lecomte",
    "Lecuyer", "Lemaître", "Leriche", "Lelong", "Leblanc", "Lefort", "Leduc", "Lebrun",
    "Lemoine", "Lepage", "Lavigne", "Laporte", "Lacroix", "Khan", "O'Connor", "Patel",
    "Kim", "Yamamoto", "Silva", "Rossi", "Bianchi", "Nowak", "Kowalski", "Smith", "Johnson",
    "Williams", "Brown", "Jones", "Miller", "Davis", "Wilson", "Taylor", "Anderson",
    "Nguyen", "Hernandez", "Lopez", "Gonzalez", "Perez", "Sanchez", "Ramirez", "Torres",
    "Flores", "Rivera", "Gomez", "Diaz", "Reyes", "Cruz", "Chavez", "Mendoza", "Alvarez",
    "Jimenez", "Ruiz", "Aguilar", "Castillo", "Soto", "Gutierrez", "Rodriguez", "Martinez",
    "Garcia", "Lee", "Wong", "Zhang", "Li", "Wang", "Chen", "Yang", "Huang", "Liu",
    "Zhao", "Wu", "Zhou", "Xu", "Sun", "Ma", "Hu", "Guo", "Lin", "He", "Gao", "Xie",
    "Song", "Han", "Tang", "Cao", "Xiao", "Feng", "Cui", "Deng", "Yu", "Lu", "Jian",
    "Zeng", "Xiong", "Pan", "Duan", "Peng", "Lu", "Liang", "Zou", "Wu", "Xiong", "Yuan",
    "Lü", "Jiang", "Cai", "Xia", "Fan", "Wei", "Xie", "Wan", "Yan", "Qin", "You", "Shi"
]


async def cv_to_db(pdf_bytes: bytes) -> None:
    try:
        result = await claude_service.structured_completion(
            inputs="Extrait les informations du candidat depuis ce CV. Si une information manque, mets un champ vide.",
            output_model=PDFModel,
            pdf_data=pdf_bytes,
            model="claude-sonnet-4-5"
        )
        d = dict(json.loads(result))
        print("\n".join(f"{k}: {v}" for k, v in d.items()))

        if result["prenom"] == "":
            result["prenom"] = random.choice(prenoms)
        if result["nom"] == "":
            result["nom"] = random.choice(noms)
        if result["email"] == "":
            result["email"] = f"{result['prenom'].lower()}.{result['nom'].lower()}@gmail.com"

            
        d = dict(json.loads(result))
        print("\n".join(f"{k}: {v}" for k, v in d.items()))

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
    

