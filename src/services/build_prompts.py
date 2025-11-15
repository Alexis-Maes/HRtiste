

def prompt_complete_category(categorie: str, ancien_contenu: str, nouveau_contenu: str) -> str:
    prompt = (
        "Tu es un assistant RH spécialisé dans l'analyse de profils candidats.\n"
        "On te fournit :\n"
        f"- une categorie : « {categorie} »,\n"
        f"- un contenu existant pour cette catégorie,\n"
        f"- un nouveau contenu proposé.\n\n"
        "Ta mission : construire une description unique et cohérente qui fusionne "
        "l'ancien et le nouveau contenu. Mets l'accent sur les points communs, "
        "les répétitions, les éléments importants, et veille à ce que le résultat "
        "soit clair, professionnel et synthétique.\n\n"
        f"Ancien contenu : {ancien_contenu}\n"
        f"Nouveau contenu : {nouveau_contenu}"
    )
    
    return prompt




def prompt_decoupe_en_category(texte_brut: str) -> str:
    prompt = (
        "Tu es un assistant RH spécialisé dans l'analyse et la structuration de descriptions de candidats.\n"
        "On te fournit un texte brut contenant des informations variées sur un candidat.\n"
        "Ta tâche est de répartir ce texte dans les différentes catégories qui te seront fournies séparément.\n\n"
        "IMPORTANT :\n"
        "- Utilise uniquement les catégories qui seront spécifiées (ne pas en inventer).\n"
        "- Répartis le contenu du texte brut dans ces catégories en tenant compte de la pertinence.\n"
        "- S'il manque du contenu pour une catégorie, renvoie une chaîne vide pour cette catégorie.\n"
        "- S'il y a plusieurs informations pour une même catégorie, synthétise-les proprement.\n"
        "- L'OUTPUT FINAL DOIT ÊTRE STRICTEMENT UN JSON VALIDE.\n"
        "- Le JSON doit contenir une clé par catégorie, avec du texte en valeur.\n\n"
        f"Voici le texte brut à analyser :\n{texte_brut}"
    )
    
    return prompt