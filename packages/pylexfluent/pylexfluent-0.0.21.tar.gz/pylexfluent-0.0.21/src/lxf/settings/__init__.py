import logging
import os
import spacy

global nlp_with_vectors
try:
    print("Chargement du modèle SPACY : fr_core_news_lg ")
    nlp_with_vectors = spacy.load("fr_core_news_lg")
except Exception as ex:
    nlp_with_vectors=None
    print("le model SPACY : fr_core_news_lg est obligatoir. Exécuter la ligne de commande suivante: python -m spacy download fr_core_news_lg ")

global nlp
nlp=None
global model_path
model_path='models/nlp/lex-fr.nlp'

global enable_tqdm
enable_tqdm:bool=False

global SET_LOGGING_LEVEL
SET_LOGGING_LEVEL = logging.INFO

if os.path.exists("./logs") ==False:
    print("Création du dossier logs")
    os.mkdir("./logs")

def load_model(path:str=None):
    """
    """
    global model_path
    global nlp
    if path!=None and path!=model_path:
        model_path=path        
        if os.path.exists(model_path) :
            print(f"Chargement du modèle depuis: {model_path}")
            nlp=spacy.load(model_path)
        else :
            print(f"Erreur: le modèle est introuvable: {model_path}")
            return None            
    if nlp==None:
        nlp=spacy.load(model_path)
    return nlp
