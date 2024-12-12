from typing import List
from xml.dom.minidom import Entity
from pydantic import BaseModel,Field

from lxf.domain.tables import lxfTable
from enum import Enum

class LoanTemplate(Enum):
    BPOP=1
    CAISSE_EPARGNE=2


class Montant(BaseModel):
    """
    Montant et devise
    """
    valeur:float=Field(default=0.0)
    devise:str=Field(default="EUR")
    class Config :
        json_schema_extra ={
            "exemple":{
                "valeur":123456.57,
                "devise":"EUR"
            }
        }

class MontantDivers(BaseModel):
    """
    Frais 
    """
    txt_montant:str=""
    nature:str=Field(default="Montant divers)")
    montant:Montant=Field(default=Montant())
    class Config:
        json_schema_extra={
            "exemple":{
                "label":"Garantie (PPD)",
                "nature":"garantie (PPD)",
                "montant":{"valeur":3808.51,"devise":"EUR"}
            }
        }

class Personne(BaseModel):
    """
    Personne Morale ou Persone Physique
    """
    est_personne:bool=Field(default=False)
    civilite:str =Field("")
    prenoms:str=Field("")
    raison_sociale:str=Field("")
    statut_organisation:str=Field("")
    siret:str=Field("")
    siren:str=Field("")
    nom:str=Field("")
    date_naissance:str=Field("")
    adresse:str=Field("")
    code_postal:str=Field("")
    ville:str=Field("")
    metier:str=Field("")
    situation_maritale:str=Field("")
    regime_matrimoniale:str=Field("")
    class Config :
        json_schema_extra ={
            "exemple" :{
                "est_personne":True,
                "cilvilite":"M",
                "prémon":"Jean Marc Antoine",
                "nom":"LEMARCHAND",
                "metier":"cadre fonction publique",
                "situation_maritale":"marié",
                "regime_maritale":"Séparation de biens",
                "adresse":"140, boulevard des Capucines",
                "code_postal":"01234",
                "ville":"Bon Vivre sur Mer et Montagne"
            }
        }

class Preteur(Personne):    
    """
    Organisme prêteur dans le cadre d'un contrat de prêt
    """
    represente_par:List[Personne]=[]
    class Config :
        json_schema_extra ={
            "exemple" :{
                "est_personne":False,
                "raison_sociale":"Banque Crédit Sécure",
                "statut_organisation":"Société Coopérative",
                "siren":"111 222 333",
                "adresse":"140, boulevard des Capucines",
                "code_postal":"01234",
                "ville":"Bon Vivre sur Mer et Montagne",
                "represente_par":[]
            }
        }

class Emprunteur(Personne):
    """
    Personne physique ou morale bénéficière d'un prêt bancaire
    """
    represente_par:List[Personne]=[]
    class Config :
        json_schema_extra ={
            "exemple" :{
                "est_personne":True,
                "civilite":"Mme",
                "premons":"Marie Françoise",
                "nom":"FRIDOMME",
                "metier":"commerçante",
                "situation_maritale":"divorcée",
                "regime_maritale":"",
                "adresse":"140, boulevard des Capucines",
                "code_postal":"01234",
                "ville":"Bon Vivre sur Mer et Montagne",
                "represente_par":[]
            }
        }

class ElementPlanFinancement(BaseModel):
    """
    Element d'un Plan de Financement d'un Prêt
    """
    nature:str=Field("")
    montant:Montant=Field(default=Montant())
    class Config:
        json_schema_extra ={
            "exemple":{
                "nature":"apport",
                "montant":{
                    "valeur":125000.00,
                    "devise":"EUR"
                    }
            }
        }
 
class ProgrammeFinancier(BaseModel):
    """
    Programme Financier d'un prêt
    plan_financement : List of ElementPlanFinancement
    montant_programme : Montant du programme (valeur,devise)
    """
    plan_financement:List[ElementPlanFinancement]=[]
    montant_programme:Montant=Field(default=Montant())
    class Config:
        json_schema_extra={
            "exemple":{
                "plan_financment":[
                    {"nature":"apport",
                     "montant":{
                         "valeur":125000.00,
                         "devise":"EUR"
                     }
                    },
                    {"nature":"subvention",
                     "montant":{
                         "valeur":0.00,
                         "devise":"EUR"
                     }
                    } ,
                    {"nature":"Prêt(s) BPBFC sollicité(s)",
                     "montant":{
                         "valeur":730000.00,
                         "devise":"EUR"
                     }
                    }                                       
                ],
                "montant_programe":{
                    "valeur":855000.00,
                    "devise":"EUR"
                }
            }
        }

class TauxAnnuelEffectifGlobal(BaseModel):
    """
    Taux annuel Effectif Global TAEG
    """
    titre:str=Field("")
    sigle:str=Field("")
    description:str=Field(" ")
    taux_pourcentage:float=Field(0.0)
    taux_periode:float=Field(0.0)
    base_periode:str=Field(default="mensuelle")
    class Config:
        json_schema_extra={
            "exemple":{
                "taux_pourcentage":2.00,
                "base_periode":"mensuelle"
            }
        }
class Domiciliation(BaseModel):
    """
    Domiciliation du compte à créditer
    """
    debiteur:str=Field("")
    compte:str=Field("")
    creancier:str=Field("")
    class Config:
        json_schema_extra={
            "exemple":{
                "crediteur":"Emprunteur",
                "compte":"compte n° 123456789",
                "beneficiaire":"BANQUE CREDIT"
            }
        }

class Frais(BaseModel):
    """
    Frais 
    """
    nature:str=Field(default="Frais Prise de garantie (Hypohteque)")
    montant:Montant=Field(default=Montant())
    class Config:
        json_schema_extra={
            "exemple":{
                "nature":"Frais prise de garantie (PPD)",
                "montant":{"valeur":3808.51,"devise":"EUR"}
            }
        }

class MontantTotalDuEmprunteur(BaseModel):
    """
    Total montant dû par l'emprunteur
    montant_total_credit:Montant total du crédit (valeur,devise)
    cout_total_credit: Cout total du Credit (valeur,devise)
    montant_total_interets: Montant Total des intérets (valeur, devise)
    montant_total_assurance_obligatoire:Montant total des assurances obligatoires (valeur,devise)
    frais: liste de Frais
    montant_total_du_emprunteur: Montant total dû par l'emprunteur (valeur,devise)
    """
    montant_total_credit:Montant=Field(default=Montant())
    cout_total_credit:Montant=Field(default=Montant())
    montant_total_interets:Montant=Field(default=Montant())
    montant_total_assurance_obligatoire:Montant=Field(default=Montant())
    frais:List[Frais]=[]
    montants_divers:List[MontantDivers]=[]
    montant_total_du_emprunteur:Montant=Field(default=Montant())
    class Config:
        json_schema_extra={
            "exemple":{
                "montant_total_credit":{"valeur":730000.00,"devise":"EUR"},
                "cout_total_credit":{"valeur":197342.08,"devise":"EUR"},
                "montant_total_interets":{"valeur":147327.00,"devise":"EUR"},
                "montant_total_assurance_obligatoire":{"valeur":45150.54,"devise":"EUR"},
                "frais":[
                        {
                            "nature":"Frais prise de garantie (PPD)",
                            "montant":{"valeur":3808.51,"devise":"EUR"}
                        },
                        {
                            "nature":"Frais prise de garantie (Hypotheque)",
                            "montant":{"valeur":556.03,"devise":"EUR"}
                        },
                        {
                            "nature":"Frais de dossier",
                            "montant":{"valeur":500.00,"devise":"EUR"}
                        }
                ],
                "montant_total_du_emprunteur":{"valeur":927342.08,"devise":"EUR"}
            }
        }

class PeriodeAmortissement(BaseModel):
    """
    Période d'amortissement d'un prêt
    type_echeance: Type échéance constante
    duree_echeances:la durée des échéances(mensuelle)
    type_taux_debiteur:type de taux débiteur (Fixe)
    taux_debiteur_pourcentage:1.5 
    montant_echeance_sans_assurance:(valeur,devise)
    """
    numero:int=Field(0)
    type_echeance:str=Field(default="constante")
    duree_echeances:str=Field(0)
    periodicite_echeance:str=Field(default="mensuelle")
    type_taux_debiteur:str=Field(default="fixe")
    taux_debiteur_pourcentage:float=Field(0.0)
    montant_echeances:List[MontantDivers] = []
    assurance:Montant=Montant()
    accessoire:Montant=Montant()
    class Config:
        scheam_extra={
            "exemple":{
                "numero":1,
                "type_echeance":"constante",
                "duree_echeances":"8",
                "periodicite_echeance":"mensuelle",
                "type_taux_debiteur":"fixe",
                "taux_debiteur_pourcentage":1.5,
                "montant_echeances":[{"nature":"Montant de l'échéance sans assurance","montant":{"valeur":2000,"devise":"EUR"}}]
            }
        }

class CaracteristiquePret(BaseModel):
    """
    Caractéristique d'un prêt bancaire
    """
    nature:str=Field("")
    numero:str=Field("")
    montant:Montant=Field(default=Montant())
    duree_mois:int = Field(0)
    class Config:
        json_schema_extra={
            "exemple":{
                       "nature":"Pret tout Habitat",
                       "numero":"08801143" ,
                       "montant":{"valeur":730000.00,"devise":"EUR"},
                       "duree_mois":300
                    }
        }
class CaracteristiquesPret(BaseModel):
    """
    Toutes les caractérisitiques d'un pret bancaire
    caracterisitiques : Liste de CrarcterisitiquePret
    """
    #caracteristiques:List[CaracteristiquePret]=[]    
    description:str=Field("")
    numero_pret:str=Field("")
    is_modulable:bool = Field(False)
    montant:str=Field("")
    taux:TauxAnnuelEffectifGlobal=TauxAnnuelEffectifGlobal()
    domiciliation:Domiciliation=Domiciliation()
    montant_total_du_emprunteurs:MontantTotalDuEmprunteur=MontantTotalDuEmprunteur()
    periodes_amortissement:List[PeriodeAmortissement]=[]
    class Config:
        json_schema_extra={
            "exemple":{
                "description":"Prêt Tout Habitat (N°08801143) : 730 000.00 EUR sur 300 mois",
                "numero_pret":"08801143",
                "is_modulable":True,
                "montant":"730 000.00 EUR",
                "domicialiation":{
                    "crediteur":"Emprunteur",
                    "compte":"compte n° 123456789",
                    "beneficiaire":"BANQUE CREDIT"
                }
            }
        }

class Amortissement(BaseModel):
    """
    Amortissement du crédit
    periodes: Liste de PeriodeAmortissement
    """
    periodes:List[PeriodeAmortissement]=[]
    class Config:
        json_schema_extra={
            "exemple":
            {
                "periodes":[
                    {   "type_echeance":"constante",
                        "duree_echeances":8,
                        "periodicite_echeance":"mensuelle",
                        "type_taux_debiteur":"fixe",
                        "taux_debiteur_pourcentage":1.5,
                        "montant_echeance_sans_assurance":{"valeur":2000,"devise":"EUR"}
                    }
                ]
            }
        }

class Assurance(BaseModel):
    """
    Assurance 
    """
    description:str=Field("")
    reference:str=Field("")
    delegation:str=Field("")
    souscripteur:str=Field("")
    nom_naissance_souscripteur:str=Field("")
    date_naissance_souscripteur:str=Field("")
    ville_naissance_souscripteur:str=Field("")
    garanties:str=Field("")
    type_assureur:str=Field("")
    quotite_pret_assure:str=Field("")
    options_choisies:str=Field("")
    hauteur_pourcentage:float=Field(0.0)
    assureur:str=Field("")
    assureur_group:str=Field("")
    couverture:str=Field("")
    tableau_prets:lxfTable=lxfTable()
    class Config:
        arbitrary_types_allowed = True
        json_schema_extra={
            "exemple":{
                "description":"Assurance Déléguée Décés -PTIA I.T.",
                "delegation":"delegation text",
                "souscripteur":"M Alain DUPOND né le 01/01/2001 à MONCHEZMOI",
                "hauteur_pourcentage":100.00,
                "assureur":"ASSURANCE GENERALE",
                "couverture":"Prêt Tout Habitat (N°01234567) : 730 000.00 EUR sur 300 mois"
            },
            "exemple 2":{
                "description":"Cnp Assurance - Bpce Vie",
                "souscripteur":"M Alain DUPOND",
                "date_naissance_souscripteur":"12/05/1996",
                "assureur":"ASSURANCE GENERALE",
                "ville_naissance_souscripteur":"Belleville"
            }
        }

class Warranty(BaseModel):
    """
    Garantie d'un prêt (Hypothèque, PPD, Caution)
    """
    label:str=Field(default="")
    rang:str=Field(default="0")
    hauteur:str=Field(default="0.0")
    duree:str=Field(default="")
    duree_limitee:str=Field(default="")
    duree_unite:str=Field(default="")
    duree_limitee_unite:str=Field(default="")
    text:str=Field(default="")
    cout_approximatif:str=Field(default="")
    office_notarial:str=Field(default="")
    adresse_office_notarial:str=Field(default="")
    code_postal_office_notarial:str=Field(default="")
    ville_office_notarial:str=Field(default="")
    numero_pret:str=Field(default="")
    ref_cadastrales:str= Field(default="")
    adresse_immeuble_cadastre:str=Field("")
    code_poste_immeuble_cadastre:str=Field("")
    ville_immeuble_cadatre:str=Field("")
    text_adresse_immeuble_cadastre:str=Field("")
    class Config:
        json_schema_extra={
            "exemple":{
                "label":"Hypothèque",
                "rang":1,
                "hauteur":"130 000,00 EUR",
                "cout_approximatif":"1 365,00 EUR",
                "text":"Hypothèque à hauteur de 130 000.00 EUR de rang 1 .... ",
                "numero_pret":"08909399",
                "ref_cadastrales":"SECTION AB NUMEROS 123 ; 456 ; 78 et LOT 81"
                
            }
        }

class ObjetFinancement(BaseModel):
    """
    Objet du financement
    """
    titre:str=""
    nature:str=""
    usage:str=""
    description:str=""
    adresse:str=""
    code_postal:str=""
    ville:str=""

class ClausesParticulieres(BaseModel):
    """
    Clause(s) Particulière(s) rattachée(s) à un prêt
    """
    titre:str=Field("Aucune")
    numero_pret:str=Field("")
    text:str=Field("")
    class Config:
        json_schema_extra={
            "exemple":{
                "text":"L'Emprunteur peut, à tout moment, rembourser en totalité ou en partie le montant du présent prêt.....",
                "numero_pret":"08909399"
            }
        }

class Pret(BaseModel):
    """
    Pret
    """
    num_suivi:str=Field("")
    header_offre:str=Field("")
    header_ref:str=Field("")
    header_emprunteur:str=Field("")
    header_responsable_suivi:str=Field("")
    header_num_etude:str=Field("")
    date_emission_offre:str=Field("")
    objets_financement:List[ObjetFinancement]=[]
    preteur: Preteur = Preteur()
    emprunteurs:List[Emprunteur]=[]
    cautions:List[Emprunteur]=[]
    programme_financier:ProgrammeFinancier=ProgrammeFinancier()
    list_prets:List[CaracteristiquePret]=[]
    caracteristiques_prets:List[CaracteristiquesPret]=[]
    #domiciliation:Domiciliation=Domiciliation()
    amortissement_credit:Amortissement=Amortissement()
    # montant_total_du_emprunteurs:MontantTotalDuEmprunteur=MontantTotalDuEmprunteur()
    delegations_assurances:List[Assurance]=[]
    assurances:List[Assurance]=[]
    garanties:List[Warranty]=[]
    clauses_particulieres:List[ClausesParticulieres]=[]
    tableau_amortissement:lxfTable=lxfTable()
    class Config:        
        arbitrary_types_allowed = True
        json_schema_extra = {
            "example": {
                "description":"Achat immobilier et travaux maison individuelle ....",
                "usage": "Résidence principale emprunteur",
                "preteur":{
                    "est_personne":False,
                    "raison_sociale":"Banque Crédit Sécure",
                    "statut_organisation":"Société Coopérative",
                    "siren":"111 222 333",
                    "adresse":"140, boulevard des Capucines",
                    "code_postal":"01234",
                    "ville":"Bon Vivre sur Mer et Montagne"
                    },
                "emprunteurs":[
                    {
                    "est_personne":True,
                    "premons":"Marie Françoise",
                    "nom":"FRIDOMME",
                    "metier":"commerçante",
                    "situation_maritale":"divorcée",
                    "regime_maritale":"",
                    "adresse":"140, boulevard des Capucines",
                    "code_postal":"01234",
                    "ville":"Bon Vivre sur Mer et Montagne"
                    },
                    {
                    "est_personne":True,
                    "cilvilite":"M",
                    "prémon":"Jean Marc Antoine",
                    "nom":"LEMARCHAND",
                    "metier":"cadre fonction publique",
                    "situation_maritale":"marié",
                    "regime_maritale":"Séparation de biens",
                    "adresse":"140, boulevard des Capucines",
                    "code_postal":"01234",
                    "ville":"Bon Vivre sur Mer et Montagne"
                    }
                ],
                "programme_financier" : {
                                            "plan_financment":[
                                                {"nature":"apport",
                                                "montant":{
                                                    "valeur":125000.00,
                                                    "devise":"EUR"
                                                }
                                                },
                                                {"nature":"subvention",
                                                "montant":{
                                                    "valeur":0.00,
                                                    "devise":"EUR"
                                                }
                                                } ,
                                                {"nature":"Prêt(s) BPBFC sollicité(s)",
                                                "montant":{
                                                    "valeur":730000.00,
                                                    "devise":"EUR"
                                                }
                                                }                                       
                                            ],
                                            "montant_programe":{
                                                "valeur":855000.00,
                                                "devise":"EUR"
                                            }
                                        },
                "caracteristes_prets":[
                                    {
                                        "description":"Prêt Tout Habitat (N°08801143) : 730 000.00 sur 300 mois",
                                        "caracteristiques":[
                                            {
                                            "nature":"Pret tout Habitat",
                                            "numero":"08801143" ,
                                            "montant":{"valeur":730000.00,"devise":"EUR"},
                                            "duree_mois":300
                                            } 
                                        ]                                        
                                    }],
                "amortissement_credit":{
                                        "periodes":
                                        [
                                            {   "type_echeance":"constante",
                                                "duree_echeances":8,
                                                "periodicite_echeance":"mensuelle",
                                                "type_taux_debiteur":"fixe",
                                                "taux_debiteur_pourcentage":1.5,
                                                "montant_echeance_sans_assurance":{"valeur":2000,"devise":"EUR"}
                                            }
                                        ]
                                    },
                "montant_total_du_emprunteurs":{
                                                "montant_total_credit":{"valeur":730000.00,"devise":"EUR"},
                                                "cout_total_credit":{"valeur":197342.08,"devise":"EUR"},
                                                "montant_total_interets":{"valeur":147327.00,"devise":"EUR"},
                                                "montant_total_assurance_obligatoire":{"valeur":45150.54,"devise":"EUR"},
                                                "frais":[
                                                        {
                                                            "nature":"Frais prise de garantie (PPD)",
                                                            "montant":{"valeur":3808.51,"devise":"EUR"}
                                                        },
                                                        {
                                                            "nature":"Frais prise de garantie (Hypotheque)",
                                                            "montant":{"valeur":556.03,"devise":"EUR"}
                                                        },
                                                        {
                                                            "nature":"Frais de dossier",
                                                            "montant":{"valeur":500.00,"devise":"EUR"}
                                                        }
                                                ],
                                                "montant_total_du_emprunteur":{"valeur":927342.08,"devise":"EUR"}
                                            },
                "taeg":{
                        "taux_pourcentage":2.00,
                        "base_periode":"mensuelle"
                        },
                "delegations_assurances":[
                    {
                            "assurance":{
                            "description":"Assurance Déléguée Décés -PTIA I.T.",
                            "souscripteur":"M Alain DUPOND né le 01/01/2001 à MONCHEZMOI",
                            "hauteur_pourcentage":100.00,
                            "assureur":"ASSURANCE GENERALE",
                            "couverture":"Prêt Tout Habitat (N°01234567) : 730 000.00 EUR sur 300 mois"
                            }
                    }
                ],
                "domiciliation":{
                            "debiteur":"Emprunteur",
                            "compte":"compte n° 123456789",
                            "creancier":"BANQUE CREDIT"
                          }               
            }
        }