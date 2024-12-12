from typing import List,Optional
from xml.dom.minidom import Entity
from pydantic import BaseModel,Field

class VidalGeneric(BaseModel):
    nom:str=Field(default="",description="Nomenclature généric Vidal")
    
class VidalProduc(BaseModel):
    code:str=Field(default="",description="Code Vidal")
    product:str=Field(default="",description="Nomenclature Vidal")
    generics:List[VidalGeneric]=[]
    
class Medicament(BaseModel):
    nom:str=Field(default="",description="nom du médicament")
    start_text:int=Field(default=0,description='Début du texte')
    end_text:int=Field(default=0,description='Fin du texte')
    medicament:str=Field(default="",description="Texte reconnu brute")
    posologie:str=Field(default='',description="Posologie application médicament")
    vidal_references:List[VidalProduc]=[]
    class Config:        
        arbitrary_types_allowed = True

class AnalyseOrdonnance(BaseModel):
    nom:str=Field(default='',description="Nom de l'ordonnance")
    raw_text:str=Field(default='',description="Texte océrisé de l'ordonnance")
    medicaments:List[Medicament]=[]
    class Config:        
        arbitrary_types_allowed = True