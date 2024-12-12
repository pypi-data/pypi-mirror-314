
from typing import List
import os.path 
import re   
import pdfplumber 
from tqdm import tqdm

################# LXF ###############################
from lxf.domain.loan import Amortissement, Assurance,  CaracteristiquePret, CaracteristiquesPret, ClausesParticulieres, Domiciliation, ElementPlanFinancement, Emprunteur, Frais, Montant, MontantDivers, MontantTotalDuEmprunteur, ObjetFinancement, PeriodeAmortissement, Personne, Pret, Preteur, ProgrammeFinancier, TauxAnnuelEffectifGlobal, Warranty
from spacy.matcher import Matcher
from lxf.services.pdf import get_text_and_tables_from_pdf
from lxf.utilities.text_comparator import TextComparator, TextArrayComparator,EMPTY_STR,JOKER_STR
from lxf.domain.tables import dump_table, dump_table_by_index, lxfCell, lxfRow, lxfTable, search_table_by_text_array, search_table_by_text_array_in_all_rows
from lxf.services.try_safe import try_safe_execute, try_safe_execute_async
from lxf.settings import load_model
from lxf import settings 
from lxf.settings import enable_tqdm
################### Logging ############################
import logging
from lxf.settings import SET_LOGGING_LEVEL

logger = logging.getLogger('Loan Extractor')
fh = logging.FileHandler('./logs/loan_extractor.log')
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)
##################################################################################################


#regex
pattern_montant_devise = re.compile(r"(?P<montant>[0-9]+ ?[0-9]*((\.|,)[0-9]+)?) *(?P<devise>[a-zA-Z]*)",re.DOTALL)
pattern_preteur =re.compile(r"PRETEUR\n(?P<preteur>.*?)Ci-après dénommé",re.DOTALL)
pattern_emprunteurs = re.compile(r"EMPRUNTEUR.*?\n(?P<emprunteurs>.*?)Ci-après dénommé",re.DOTALL)
pattern_emprunteur_representation = re.compile(r"(?P<organisation>.*?) représenté\(?e?\)? par :?(?P<representants>.*)",re.DOTALL)
pattern_objet_financement=re.compile(r"OBJET DU FINANCEMENT\n(?P<objet>.*?)PROGRAMME FINANCIER",re.DOTALL)
pattern_objet_description_financement=re.compile(r"(^- (?P<objet_titre>.*?):(?P<objet_description>.*?)$)|((?P<description>.*?)^Usage *: *(?P<usage>.*?)$)",re.DOTALL|re.MULTILINE)
pattern_caracteristiques_pret_description=re.compile(r"CARACTERISTIQUES DU (PRET|CREDIT) PROPOSE\n(?P<caracteristiques_pret_propose>.*?)\nAMORTISSEMENT DU CREDIT\n",re.DOTALL|re.IGNORECASE)
pattern_caracteristiques_pret_jusquau_dernier_point=re.compile(r"CARACTERISTIQUES DU (PRET|CREDIT) PROPOSE(?P<caracteristiques_pret_propose>.*?)(DOMICILIATION|ASSURANCE\(S\))",re.DOTALL|re.MULTILINE|re.IGNORECASE)
pattern_taux_credit=re.compile(r"TAUX (ANNUEL )?EFFECTIF GLOBAL( \(TAEG\))?\n(?P<taux_teg>.*?)\n",re.DOTALL|re.IGNORECASE)
siren_pattern = re.compile(r"(?P<siren>[0-9]{3} ?[0-9]{3} ?[0-9]{3})",re.DOTALL)
date_pattern  = re.compile(r"(?P<date>[0-9]{2}\/[0-9]{2}\/[0-9]{4})",re.DOTALL)

pattern_num_suivi = re.compile(r"N° de suivi ?: ?(?P<num_suivi>[0-9]{6,10}[a-zA-Z]?)")
pattern_entite_num_suivi = re.compile(r"(?P<entite_suivi>.*)/ *?(?P<num_suivi>[0-9]{6,10}[a-zA-Z]?)")

pattern_short_header = re.compile(r"(?P<entite_suivi>.*\n) ?(?P<ref>[0-9]{5,10}[a-zA-Z]*) ?\/ ?(?P<responsable_suivi>(.*)\n)",re.MULTILINE)

pattern_header = re.compile(r"(?P<entite_suivi>.*)/ *?(?P<num_suivi>[0-9]{6,10})\n(?P<num_offre>[0-9]{6,10})\nN° Etude (?P<num_etude>[0-9]{6,10})\n(?P<responsable>.*)\n",re.MULTILINE)
pattern_header_particulier = re.compile(r"(?P<entite_suivi>.*)\n(?P<ref>[0-9A-Z]*) */* (?P<responsable>.*)\nN° de suivi *:? *(?P<num_suivi>[0-9]{6,10}[a-zA-Z]?)\n",re.MULTILINE)
pattern_num_etude = re.compile(r"N° Etude (?P<num_etude>[0-9]{6,10})")

pattern_date_offre = re.compile(r"(Offre émise par (?P<date_offre>.*?)ACCEPTATION DE L'OFFRE PAR L'EMPRUNTEUR)|(Edité le (?P<date_litteral_offre>.*?)\n)",re.DOTALL)
pattern_pragraphe_domiciliation = re.compile(r"DOMICILIATION(?P<domiciliation>.*)",re.DOTALL)
patterns_paragraphe_garanties=re.compile(r"GARANTIE\(S\)\n(?P<garanties>.*?)\n(CLAUSE\(S\)|TABLEAU D'AMORTISSEMENT)",re.DOTALL)
pattern_domiciliation_num_compte = re.compile(r"emprunteur.*autorise.*banque.*prélever.*échéance.*compte +(n|num)(°|:)? +(?P<num_compte>[0-9]+).*livres de(?P<debiteur>.*?\.*)\.",re.MULTILINE|re.IGNORECASE)

## CADASTRE 
regex = (r"(cadastré) ?:? (section)? ?(?P<section>[a-zA-Z]{1,}) (numeros|numéros|numero|numéro)? ?:? ?(?P<numeros>([0-9]{1,})+ ?[\/ ,;-]?(((et)?[\n"
	r"\"\/ ,;-]*[0-9]*))*)((lot )(?P<lot>[a-z0-9]*))?")

regex_adresse_immeuble_cadastre = r"(immeuble)? sise? (?P<adresse_immeuble_cadastre>.*)cadastré"

domiciliation_patterns=[
    {"ENT_TYPE":"QUALITE"},{"LEMMA":"autorise"},{"OP":"+"},
    {"LEMMA":"prélever"},{"OP":"+"},{"LEMMA":"échéance"},{"OP":"+"},
    {"ENT_TYPE":"NUM_COMPTE"},{"OP":"+"},{"ENT_TYPE":"ORG_RAISON_SOCIALE"}
]

#load Lexfluent spacy nlp
# Label defined in lex-fr.nlp 
label_garantie_assurance="GARANTIE_ASSURANCE"
label_personne="PERSONNE"
label_date_naissance="DATE_NAISSANCE"
label_ville="VILLE"
label_garantie_financiere="GARANTIE_FINANCIERE"
label_type_assurance="TYPE_ASSURANCE"
label_address="ADRESSE" 

nlp = load_model()
if nlp!=None :
    matcher = Matcher(nlp.vocab)
else:
    raise Exception("Loan_Extractor: NLP ne peut pas être None: matcher = Matcher(nlp.vocab) ")
#Taux 
# taux_definition_key="TAUX_DEFINITION"
# matcher.add(taux_definition_key,[taux_definition_patterns1,taux_definition_patterns2],greedy="FIRST")
# taux_definition_matcherkey = nlp.vocab.strings[taux_definition_key]

#Domiciliation
domiciliation_key="DOMICILIATION"
matcher.add(domiciliation_key,[domiciliation_patterns],greedy="FIRST")
domiciliation_key_matcherkey = nlp.vocab.strings[domiciliation_key]
#Garanties
pattern_garantie_office_notaire = re.compile(r"Notaire ?: ?\n?(?P<office_notarial>[a-zA-Z .'îÎ-]*)\n?,?(?P<adresse_office_notarial>[0-9a-zA-Z ,'-]*)\n?(Cette|La) garantie",re.DOTALL|re.IGNORECASE)
garanties_patterns1=[
    {"ENT_TYPE":"GARANTIE_FINANCIERE"}
    ,{"OP":"+"}
    ,{"lower":"coût"}
    ,{"lower":"approximatif"}
    ,{"OP":"+"}
    ,{"lower":"eur"}
]
garanties_patterns2=[
    {"ENT_TYPE":"GARANTIE_FINANCIERE"}
    ,{"OP":"+"}
    ,{"lower":"notaire"}
    ,{"OP":"+"} 
]
garanties_key="GARANTIES"
garanties_key_matcherkey=nlp.vocab.strings[garanties_key]

garantie_hauteur_pattern=[
    {"ENT_TYPE":"GARANTIE_FINANCIERE"},{"OP":"*"},{"lower":"à"},{"lower":"hauteur"},{"lower":"de"},{"ENT_TYPE":"MONTANT"}
]
garantie_hauteur_key="GARANTIE_HAUTEUR"
garantie_hauteur_matcherkey=nlp.vocab.strings[garantie_hauteur_key]
garantie_rang_pattern=[
    {"lower":"rang"},{"IS_DIGIT":True}
]
garantie_rang_key="GARANTIE_RANG"
garantie_rang_matcherkey=nlp.vocab.strings[garantie_rang_key]
garantie_cout_approximatif_pattern=[
    {"lower":"coût"},{"lower":"approximatif"},{"TEXT":":"},{"ENT_TYPE":"MONTANT"}
]
garantie_frais_commission_cautionnement_pattern=[
    {"lower":"frais"},{},{"lower":"commission"},{},{"lower":"cautionnement"},{"ORTH":":","OP":"?"},{"ENT_TYPE":"MONTANT"}
]
garantie_cout_approximatif_key="GARANTIE_COUT_APPROXIMATIF"
garantie_cout_approximatif_matcherkey= nlp.vocab.strings[garantie_cout_approximatif_key]

matcher_garantie =Matcher(nlp.vocab)
matcher_garantie.add(garanties_key,[garanties_patterns1,garanties_patterns2],greedy="FIRST")
matcher_garantie.add(garantie_hauteur_key,[garantie_hauteur_pattern],greedy="FIRST")
matcher_garantie.add(garantie_rang_key,[garantie_rang_pattern],greedy="FIRST")
matcher_garantie.add(garantie_cout_approximatif_key,[garantie_cout_approximatif_pattern],greedy="FIRST")
matcher_garantie.add(garantie_cout_approximatif_key,[garantie_frais_commission_cautionnement_pattern],greedy="FIRST") 

class assurance_type:
    type:str="Assurance"
    start:int=0
    end:int=0
    text=""

# routines utilities 
def sanitize_text(text:str)->str :
    temp_text=""
    last_char=" "
    try :
        if text==None or text == "" : return ""
        # remove extra space
        text=text.replace("–","-").replace("’","'").replace("\n"," ").replace("\"","'").replace('§','').strip()  
        for char in text:
            if char==" ":
                if not last_char== " ":
                    temp_text+=char
                last_char=char
            else:
                last_char=char
                temp_text+=char    
    except Exception as ex:
        logger.exception(f"Exception occured in sanitize_text: {ex}")
    return temp_text 

def sanitize_numero(text:str)->str:
    return text.replace("N","").replace("n","").replace("°","").replace("o","").strip()

def sanitize_ref_cadastrales(text:str)->str:
    regex = r"(cadastré) ?:?"
    subst=""
    # Vous pouvez spécifier manuellement le nombre de remplacements en changeant le 4e argument
    return re.sub(regex, subst, text, 0, re.MULTILINE | re.IGNORECASE)
    
def preprocess_code_postal_09999(text:str)->str :
    """
    Identifie les codes postaux du type 09999 qui peuvent être interprétés comme des noms et les transforme en :  . 09999   
    Cela force notre NLP a les identifiés comme des nombres ; c'est ce qu'on attend 
    """
    regex = r" 0[1-9][0-9]{3,3} "
    subst = " - \\g<0>"
    return re.sub(regex, subst, text, 0, re.MULTILINE)


def create_entete_amortissement(amortissement_entete)->lxfRow :
    result:lxfRow=lxfRow()
    for cel in amortissement_entete:
        amortissement_colonne:lxfCell=lxfCell()
        amortissement_colonne.value = cel
        result.cells.append(amortissement_colonne)
    return result

def is_table_header_same(table:lxfTable,amortissement_entete)->bool :
    result=False
    if table :
        if len(table.rows[0].cells)==len(amortissement_entete) :
            header_cptor=TextArrayComparator(amortissement_entete,nlp=settings.nlp_with_vectors)
            hdr_table_to_compare = [cell.value for cell in table.rows[0].cells]
            result=header_cptor.compare_to(hdr_table_to_compare)>=0.80
            hdr_table_to_compare=None
            hdr_to_compare=None
    return result 

def to_float(text:str)->float:
    # suppress blank chars and replace , by point : exemple 125 000,00  => 125000.00 
    text= text.replace(" ","").replace(",",".")
    try :
        return float(text)
    except Exception as e:
        logger.exception(f"to_float: Erreur conversion en float de : {text}\nException:{e}")
        return 0.0

def to_int(text:str)->int:
    # suppress blank chars and replace , by point : exemple 125 000  => 125000
    text= text.replace(" ","").replace(",",".")
    try :
        return int(text)
    except Exception as e:
        logger.exception(f"to_int Erreur conversion en int de : {text}\nException:{e}")
        return 0

def sanitize_address(adresse:str)->str:
    doc_adresse = nlp(adresse)
    adr=""
    # dont take  verbs "demeurer" or "situer" from the address text
    for token in doc_adresse :
        if token.lemma_!="demeurer" and token.lemma_!="situer":
            adr+=f"{token.text} "
    adr = adr.replace("est à","")
    return sanitize_text(adr)
 
def sanitize_date(date_str:str)->str:
    match_date = date_pattern.search(date_str)
    if not match_date == None:
        date_naissance=match_date.group("date")
        return date_naissance
    else :
        return date_str 
def sanitize_bas_de_page_ce(text)->str:
        # supression bas de page
        regex3= r"Réf\. :.{1,20} Page [0-9]{1,3} ?/ ?[0-9]{1,3}"
        subst3 =  "\\n"
        text = re.sub(regex3,subst3,text,0,re.MULTILINE|re.IGNORECASE|re.DOTALL)  
        return text

def sanitize_garanties_text(text)->str :
        """
        Sanitize paragraphe pour les garanties.
        on doit exclure certaines références à une garantie lorsqu'elle n'est pas pertinente dans le texte.
        le cas étant rare, on n'a trop de données pour un apprentissage. Par contre on peut facilement éliminer certains cas bien connus
        comme les cas ci-dessous :
            - appuyé d'une hypothèque 
            - à l'inscription d'une hypothèque
        """
        regex1 = r"appuyé[ \n]*d'une[ \n]*hypothèque"
        regex2 = r"à[ \n]*l'inscription[ \n]*d'[ \n]*hypothèque"
        
        subst1 ="appuyé d'une §hyphotèque§"
        subst2 ="à l'inscription d'une §hypothèque§"
        text = re.sub(regex1, subst1, text, 0, re.MULTILINE | re.IGNORECASE)
        text = re.sub(regex2, subst2, text, 0, re.MULTILINE | re.IGNORECASE)
        # supression bas de page
        text = sanitize_bas_de_page_ce(text)        
        return text 
def extract_duree_from_text(text:str):
    """
    Extrait la première durée et l'unite de temps trouvé dans le texte
    par exemple: 60 mois retourne le tuple  '60','mois
    si aucune durée de temps trouvée, retourne "",""
    """
    regex = r"(?P<duree>[0-9]+) (?P<unite>heure|minute|seconde|mois|trimestre|semestre|an|année)"
    duree=""
    unite=""
    matches = re.search(regex, text, re.MULTILINE | re.IGNORECASE)
    if matches!=None and matches.groups()!=None :
        duree = matches.group("duree")
        unite = matches.group("unite")
    return duree, unite

def ce_sanitize_initiales_ref(text:str)->str :
    """
    """
    regex= r"(apposez|vos|initiales|réf|(page [0-9]{1,3} ?\/[0-9]+))|(F[0-9]+)|( {2,})"
    subst=""
    result = re.sub(regex, subst, text, 0, re.MULTILINE | re.IGNORECASE)
    return result 

def sanitize_raison_sociale(text:str)->str:
    """
    """
    return text.lower().replace("société dénommée","").replace("dénomination sociale :","").replace("dénomination sociale","").replace("dont le siège social","").replace("société","").replace("\n","").upper()

def sanitize_CRD_border_side_effect(text:str)->str:
    """"
    """
    regex = r"[0-9]{5}\n-\n[0-9]{4}DRC"
    subst="\n"
    result = re.sub(regex,subst,text,0,re.MULTILINE)
    return result

def sanitize_duplicate_blank(text:str)->str :
    """
    Elimine tous les blancs consécutifs en les remplaçant par un seul blanc
    """
    regex = r" {2,}"
    subst=" "
    return re.sub(regex, subst, text, 0, re.MULTILINE)

class LoanDataExtractor:
    """
    LoanDataExtrator is a class helper for extracting all loan data from a pdf file of type of Offre de Prêt Banque Populaire Franche-Conté
    """
    ### Cautions
    pattern_cautions = re.compile(r"CAUTION\(S\)(?P<cautions>.*?)Ci-après dénommée\(s\) \"La Caution\"",re.DOTALL|re.MULTILINE)
    
    ### Amortissement
    pattern_amortissement_credit=re.compile(r"AMORTISSEMENT DU CREDIT\n(?P<amortissement_credit>.*?)((MONTANT TOTAL)|(COUT DU CREDIT))",re.DOTALL)
    pattern_amortissement_credit_periodes_echeances=re.compile(r"(?P<periode>Période n° *(?P<num_periode>[0-9]{1,2}?) *: *(?P<type_periode>.*?)(?P<rat_periode>Durée.*?)(-|§))|(?P<echeance>- Echéance\(s\) constante\(s\)(?P<rat_echeance>.*?)$)", re.DOTALL)
    pattern_amortissement_credit_Duree_taux=re.compile(r"Durée *: *(?P<duree>.*?)Taux.*?: *(?P<taux>.*?)%\.?(?P<rat>.*)",re.DOTALL)
    pattern_amortissement_credit_montant_echeance = re.compile(r"(?P<montant_label>Montant .*?échéance.*?): *(?P<montant_echeance>.*?)\.\n",re.DOTALL)
    
    ### Assurances
    pattern_assurances = re.compile(r"ASSURANCE\(S\)\n(?P<assurances>.*?)GARANTIE\(S\)",re.DOTALL)
    multi_delegation_assurance_pattern = re.compile(r"(Délégation .*)?(Délégation .*)§",re.DOTALL)
    delegation_assurance_pattern=re.compile(r"Délégation.*?bénéfice.*?l'assurance(?P<delegation>.*?)souscrite par(?P<souscripteur>[A-Z\- ].*?)(né\(e\)(?P<nom_naissance>[A-Z\- ].*?)le.*?(?P<date_naissance>.*?) à (?P<ville_naissance>.*?))? à hauteur de(?P<hauteur>.*?)%(.*?risques \"(?P<risques>.*?)\")?(.*? auprès de(?P<assureur>.*?)\.)?.*?en couverture.*?:\n?(?P<couverture>.*?)\.?",re.DOTALL)
    assurance_paragraphe_pattern=re.compile(r"Assurance groupe ?« ?(?P<assurance_groupe>.*?) ?»(?P<assurance_paragraphe>.*)",re.DOTALL)
    assurance_paragraphe_pattern_souscrite_par = re.compile(r"Assurance groupe (?P<assurance_groupe>.*?) souscrite par (?P<assurance_paragraphe>.*)",re.DOTALL)
    assurance_pattern=re.compile(r"souscrite par(?P<souscripteur>[A-Z\- ].*?)né\(e\)(?P<nom_naissance>[A-Z\- ].*?)le.*?(?P<date_naissance>.*?) à (?P<ville_naissance>.*?)\..*?Compagnie d'assurance ?: ?(?P<assureur>.*?).?Type ?: ?(?P<type_assureur>.*?).?Quotité de prêt assuré ?: ?(?P<quotite_pret>.*?)%.?Garanties \(\*\) ?: ?(?P<garanties>.*)Options choisies \((.*)\) :(?P<options_choisies>.*)",re.DOTALL)
    assurance_pattern_2 =re.compile(r"souscrite par(?P<souscripteur>[A-Z\- ].*?)né\(e\)(?P<nom_naissance>[A-Z\- ].*?)le.*?(?P<date_naissance>.*?) à (?P<ville_naissance>.*?) en couverture des risques(?P<garanties>.*?)\..*?en couverture de :(?P<couverture>.*?)\.(?P<description>.*?)\.",re.DOTALL)   
    assurance_pattern_3=re.compile(r"Cette assurance est souscrite en couverture de ?: ?-? ?(?P<couverture>.*mois)",re.DOTALL|re.MULTILINE)
    assurance_pattern_4=re.compile(r"souscrite par(?P<souscripteur>[A-Z\- ].*?)né\(e\)(?P<nom_naissance>[A-Z\- ].*?)le.*?(?P<date_naissance>.*?) à (?P<ville_naissance>.*?)\..*?Compagnie d'assurance ?: ?(?P<assureur>.*?).?Type ?: ?(?P<type_assureur>.*?).?Quotité de prêt assuré ?: ?(?P<quotite_pret>.*?)%.?Garanties \(\*\) ?: ?(?P<garanties>.*?\.)",re.DOTALL|re.MULTILINE)
   
    ### Caracterisitiques Prêts
    pattern_caracteristiques_paragraphe = re.compile(r"CARACTERISTIQUES DU (?P<type>PRET|CREDIT) PROPOSE?(?P<caracteristiques_pret_propose>.*?)(ASSURANCE\(S\))",re.DOTALL|re.MULTILINE)
    pattern_caracteristiques_avec_reste_traiter = re.compile(r"(CARACTERISTIQUES DU (PRET|CREDIT) PROPOSE)(?P<caracteristiques>.*?)(CARACTERISTIQUES DU (PRET|CREDIT) PROPOSE)(?P<reste_traiter>.*)",re.DOTALL| re.MULTILINE)
    pattern_caracteristiques_un_pret = re.compile(r"(CARACTERISTIQUES DU (PRET|CREDIT) PROPOSE)(?P<caracteristiques>.*)",re.DOTALL|re.MULTILINE)
    pattern_clauses_particulieres_paragraphe = re.compile(r"CLAUSE\(S\) PARTICULIERE\(S\)(?P<clauses_particulieres_paragraphe>.*?)(CONDITIONS GENERALES\n|TABLEAU D'AMORTISSEMENT)",re.DOTALL|re.MULTILINE)
    
    ### Clauses particulieres
    pattern_clauses_particulieres_reste_traiter = re.compile(r"CLAUSE\(S\) PARTICULIERE\(S\)(?P<rattachement>.*?\n)(?P<clauses_particulieres>.*?)CLAUSE\(S\) PARTICULIERE\(S\)(?P<reste_traiter>.*)",re.DOTALL|re.MULTILINE)
    pattern_clauses_particulieres_seules = re.compile(r"CLAUSE\(S\) PARTICULIERE\(S\)(?P<rattachement>.*?\n)(?P<clauses_particulieres>.*)",re.DOTALL|re.MULTILINE)
    pattern_jusquau_dernier_point=re.compile(r"(?P<clauses_particulieres_jusquau_dernier_point>.*\.)",re.DOTALL|re.MULTILINE)
    
                     
    def __init__(self,filename:str) -> None:
        """
        Ctor         
        filename : the file name of Offre de Prêt Banque Populaire Franche-Conté
        """
        if os.path.exists(filename) :
            self.filename=filename
        else :
            raise NameError(f"{filename} non trouvé")

    async def extract_preteur(self,text:str)->Preteur:
        """
        Extract the data of 'Preteur'
        text : text extracted from a pdf of type : Offre de Prêt Banque Populaire Franche-Conté
        return: Preteur
        """ 
        match_preteur = pattern_preteur.search(text)
        if match_preteur==None or match_preteur.groups()==None or match_preteur.group("preteur")==None : return None
        doc_preteur = nlp(sanitize_duplicate_blank(match_preteur.group("preteur").replace("\n"," ")))
        preteur:Preteur=Preteur()
        for ent in doc_preteur.ents :
            if ent.label_ == "ORG_RAISON_SOCIALE" and preteur.raison_sociale=="":
                preteur.raison_sociale = ent.text
                preteur.est_personne=False
            elif ent.label_ == "ORG_STATUT" : 
                preteur.statut_organisation = ent.text
                preteur.est_personne=False
            elif ent.label_=="ADRESSE" :
                if not(ent.text in preteur.adresse):
                    preteur.adresse+=sanitize_address(ent.text)
            elif ent.label_ =="CODE_POSTAL":
                preteur.code_postal = ent.text
            elif ent.label_ =="VILLE":
                preteur.ville = ent.text
            elif ent.label_ =="ORG_IMMATRICULATION":
                match_siren = siren_pattern.search(ent.text)
                if not match_siren == None :
                    preteur.siren = match_siren.group("siren")
        return preteur

    async def get_emprunteurs_from_text(self,text:str)->List[Emprunteur] :
        """
        
        """
        #logger.debug(f"text = {text}")
        personnes:List[Emprunteur]=[]
        text = preprocess_code_postal_09999(text)
        doc = nlp(text)
        current_personne=Emprunteur()
        #logger.debug(f"Raison sociale : {current_personne.raison_sociale} civilite ={current_personne.civilite}")
        for ent in doc.ents:
            if ent.label_ == "ORG_RAISON_SOCIALE":  
                #logger.debug("Raison sociale")
                if not current_personne.raison_sociale=="" or not current_personne.civilite=="":
                     #logger.debug("Add new raison sociale")
                     personnes.append(current_personne)  
                     # Create a new one personne    
                     current_personne=Emprunteur()            
                current_personne.raison_sociale = sanitize_raison_sociale(ent.text)
                current_personne.est_personne=False
            elif ent.label_ == "ORG_STATUT" : 
                current_personne.statut_organisation = ent.text
                current_personne.est_personne=False
            elif ent.label_ =="ORG_IMMATRICULATION":
                match_siren = siren_pattern.search(ent.text)
                if not match_siren == None :
                    current_personne.siren = match_siren.group("siren")            
            if ent.label_ =="CIVILITE":
                #logger.debug("Civilite")
                if not current_personne.raison_sociale==""  or not current_personne.civilite=="":
                    personnes.append(current_personne)
                    # Create a new one personne   
                    current_personne=Emprunteur()
                current_personne.civilite=ent.text
                current_personne.est_personne=True
            elif ent.label_ =="ADRESSE":
                if not(ent.text in current_personne.adresse):
                    current_personne.adresse+=sanitize_address(ent.text)
            elif ent.label_ =="CODE_POSTAL":
                current_personne.code_postal=ent.text
            elif ent.label_ == "VILLE":
                current_personne.ville = ent.text
            elif ent.label_ == "PERSONNE" and current_personne.nom=='':
                current_personne.nom=ent.text
            elif ent.label_ =="SITUATION_MARITALE" :
                current_personne.situation_maritale = ent.text
            elif ent.label_ =="REGIME_MATRIMONIAL" :
                current_personne.regime_matrimoniale = ent.text
            elif ent.label_ == "DATE_NAISSANCE" : 
                current_personne.date_naissance=sanitize_date(ent.text)
            elif ent.label_ == "METIER":
                current_personne.metier=ent.text
        personnes.append(current_personne)
        return personnes
        
    async def extract_emprunteurs(self,text:str) :
        """
        Extract the list of emprunteurs 
        text: text from the pdf of type Offre de Prêt Banque Populaire Franche-Conté
        return : List of Emprunteurs
        """ 
        emprunteurs:List[Emprunteur]=[]
        match_emprunteurs=pattern_emprunteurs.search(text)
        if match_emprunteurs==None or match_emprunteurs.groups==None or match_emprunteurs.group("emprunteurs") == None :
            return emprunteurs
        paragraph_emprunteurs = match_emprunteurs.group("emprunteurs")
        # try to find delegation 
        match_representation = pattern_emprunteur_representation.search(sanitize_text(paragraph_emprunteurs))
        if match_representation==None :
            ## Représentant is not in paragrapha_emprunteurs
            ## Let's try to find it just after 
            _, end = match_emprunteurs.span()
            following_text = text[end:end+500].split(".")[0]
            if following_text!=None or following_text!='':
                match_representation = pattern_emprunteur_representation.search(sanitize_text(following_text))
                if match_representation!=None :
                    personnes = await try_safe_execute_async(logger, func=self.get_emprunteurs_from_text,text=paragraph_emprunteurs)
                    emprunteur = personnes[0]
                    representants = await try_safe_execute_async(logger,func=self.get_emprunteurs_from_text,text=following_text)
                    if representants!=None : 
                        emprunteur.represente_par = representants
                    emprunteurs.append(emprunteur)
        else :
            organisation_txt = match_representation.group("organisation")
            representants_txt = match_representation.group("representants")
            pers = await try_safe_execute_async(logger,func=self.get_emprunteurs_from_text,text=organisation_txt)
            if not pers == None and len(pers)>=1:
                emprunteur:Emprunteur = pers[0]

                representants = await try_safe_execute_async(logger,func=self.get_emprunteurs_from_text,text=representants_txt)
                if not representants==None : 
                    emprunteur.represente_par = representants
                emprunteurs.append(emprunteur)
        
        if emprunteurs==[] :
            ## None delegation has been found
            emprunteurs = await try_safe_execute_async(logger, func=self.get_emprunteurs_from_text,text=paragraph_emprunteurs)
        return emprunteurs
 
    async def extract_cautions(self,text:str) ->List[Emprunteur] :
        """
        Extract Caution(s)
        """
        groupe_cautions="cautions"
        match_cautions = self.pattern_cautions.search(text)
        cautions:List[Emprunteur]=[]
        if match_cautions !=None :
            cautions_paragraph_text =match_cautions.group(groupe_cautions)
            cautions = await try_safe_execute_async(logger,self.get_emprunteurs_from_text,text=cautions_paragraph_text)
        return cautions
        
    async def extract_objectives_data(self, text:str)->List[ObjetFinancement]:
        """
        Extract the list of purpose of the loan : Description, Usage, Adresse du bien, Code Postal du bien, Ville du bien
        text : the extracted text from a pdf of type Offre de Prêt Banque Populaire Franche-Conté
        return : List of ObjetFinancement
        """
        match_objet_financement = pattern_objet_financement.search(text)
        if match_objet_financement==None or match_objet_financement.groups()==None or match_objet_financement.group("objet")==None : return []
        objet_financement = match_objet_financement.group("objet")+"\n" # addin \n required in order to get the last one object
        #logger.debug(f"text objets financement => {objet_financement}")
        matches = pattern_objet_description_financement.finditer(objet_financement)
        if matches == None : return []
        objets_financement:List[ObjetFinancement]=[]
        for match in matches :
            objet_financement:ObjetFinancement = ObjetFinancement()
            b_found:bool=False
            description = match.group("description")
            usage = match.group("usage")  
            objet_titre = match.group("objet_titre")
            objet_description = match.group("objet_description")

            if not (description==None or description.strip()=="") : # when no shape titre:description is found 
                #logger.debug(f"group description: <{description}>")
                doc = nlp(description)
                # find the nature  
                for ent in doc.ents:
                    if ent.label_=="NATURE_FINANCEMENT":
                        objet_financement.nature = objet_financement.nature +" "+ent.text 
                doc=None
                objet_financement.titre="Objet financement"
                objet_financement.description=try_safe_execute(logger,func=sanitize_text,text=description)
                objet_financement.usage=try_safe_execute(logger,func=sanitize_text,text=usage)
                b_found=True
            elif not (objet_titre == None or objet_titre.split()=="" or objet_description==None or objet_description.split()=="") :
                #logger.debug(f"Titre {objet_titre} Description {objet_description}")
                objet_financement.titre = try_safe_execute(logger,func=sanitize_text,text=objet_titre)
                # objet_financement.nature = try_safe_execute(logger,func=sanitize_text,text=objet_titre)
                objet_financement.description = try_safe_execute(logger,func=sanitize_text,text=objet_description)
                doc = nlp(objet_titre)
                # find the nature 
                for ent in doc.ents:
                    if ent.label_=="NATURE_FINANCEMENT":
                        objet_financement.nature = objet_financement.nature +" "+ent.text 
                doc=None                
                b_found=True
            #logger.debug(f"Objet Financement => {objet_financement.titre} : {objet_financement.description}") 
            if b_found :   
                # some cases required a space at the end to get the right entities 
                doc_description = nlp(objet_financement.description+" ")
                #logger.debug(f"Objet financement Description : {objet_financement.description}")
                for ent in doc_description.ents:
                    if ent.label_=="ADRESSE" :
                        objet_financement.adresse += sanitize_address(ent.text)
                    elif ent.label_=="CODE_POSTAL":
                        #logger.debug(f"Objet Financement Code Postal: {ent.text}")
                        objet_financement.code_postal = ent.text
                    elif ent.label_ =="VILLE":
                        #logger.debug(f"Objet Financement Ville: {ent.text}")
                        objet_financement.ville = ent.text
                    elif ent.label_ =="LOC":
                        #logger.debug(f"Objet Financement Localité: {ent.text}")
                        objet_financement.adresse = ent.text                     
                objets_financement.append(objet_financement)
        return objets_financement

    async def extract_programme_financier(self,tables)->ProgrammeFinancier:
        """
        Extract all data about the financial program 
        tables : all tables extracted from the documents
        return : ProgrammeFinancier instantiated class
        """
        if tables==[] or tables==None : 
            #logger.debug("extract_programme_financier: tables is empty")
            return None
        prg_financier:ProgrammeFinancier=None
        #check t1 is as expected 
        #table 1
        t1_cptor=TextArrayComparator(["Nature","Montant","Devises"],nlp=settings.nlp_with_vectors)
        candidates_tables:List[lxfTable]=search_table_by_text_array(t1_cptor,tables) 
        t1_ok:bool=candidates_tables!=None and len(candidates_tables)>0   

        if t1_ok==False : 
            logger.warning("extract_programme_financier: Table 1 l'entête est incorrecte")
            dump_table(tables[0])
        else :
            #plan de financement
            if prg_financier==None: prg_financier=ProgrammeFinancier()
            for t in candidates_tables :
                for i in range(1,len(t.rows) ) :
                    row:lxfRow=t.rows[i]
                    elt_plan_financier:ElementPlanFinancement=ElementPlanFinancement()
                    elt_plan_financier.nature = row.cells[0].value
                    amount:Montant=Montant()
                    amount.valeur=to_float(row.cells[1].value)
                    amount.devise=row.cells[2].value
                    elt_plan_financier.montant=amount
                    prg_financier.plan_financement.append(elt_plan_financier)  
        t2_cptor=TextArrayComparator(["Montant du programme","",""],nlp=settings.nlp_with_vectors)
        candidates_tables = search_table_by_text_array(t2_cptor,tables,1) 
        
        if candidates_tables!=None and len(candidates_tables)>0 :
            t2:lxfTable = candidates_tables[0]
            row:lxfRow = t2.rows[0]
            if prg_financier==None: prg_financier=ProgrammeFinancier()
            # Montant du programme 
            amount:Montant=Montant()
            amount.valeur=to_float(row.cells[1].value)
            amount.devise=row.cells[2].value
            prg_financier.montant_programme=amount
        return prg_financier

    async def extract_amortissement_pret(self,text:str)->Amortissement:
        """
        """
        amortissement:Amortissement=Amortissement()
        match_amortissement_credit= self.pattern_amortissement_credit.search(text)
        #logger.debug(f"Amortissement : {match_amortissement_credit}")
        if match_amortissement_credit == None : return amortissement 
        amortissement_credit = match_amortissement_credit.group("amortissement_credit")
        periodes_text = amortissement_credit +"§" # tip for marking the end of text required the regex rule 
        if periodes_text == None : return amortissement
        #logger.debug(f"Amortissement periodes : {periodes_text}")
        matches_periodes_echeances = self.pattern_amortissement_credit_periodes_echeances.finditer(periodes_text)
        for m in matches_periodes_echeances:
            periode:PeriodeAmortissement=PeriodeAmortissement()
            rat:str=""
            #logger.debug(f"Ammortissement groups {m.groups()}")
            if not m.group("periode") == None :
                num_periode = m.group("num_periode")
                #logger.debug(f"Amortissement N° période : {num_periode}")
                periode.numero =int(num_periode)    
                periode.type_echeance =sanitize_text(m.group("type_periode") )
                rat=m.group("rat_periode")                
            elif not m.group("echeance")==None:
                periode.numero=1
                #logger.debug(f"Amortissement Echéance Periode N°1")
                periode.type_echeance="Echéance(s) constante(s)"
                rat=m.group("rat_echeance")
            duree_taux = self.pattern_amortissement_credit_Duree_taux.search(rat)
            if not (duree_taux == None or duree_taux.groups==None ):
                periode.duree_echeances =sanitize_text(duree_taux.group("duree"))
                periode.taux_debiteur_pourcentage = to_float(duree_taux.group("taux").replace("%.","").replace(",","."))
                rat = duree_taux.group("rat")+".\n" # add a carriage return in order to treat the last line as the end of the last paragraph
                # rat = rat.replace(".\n",".§\n") # insert a Mark § for selecting all the paragraph about the echeance 
                #logger.debug(f"Amortissement reste à faire montant échéances {rat}")
                montant_echeance_matches = self.pattern_amortissement_credit_montant_echeance.finditer(rat)
                for montant_echeance in montant_echeance_matches :
                    mnt:MontantDivers=MontantDivers()
                    mnt.nature = montant_echeance.group("montant_label")
                    mnt_echeance = montant_echeance.group("montant_echeance")
                    mnt.txt_montant = sanitize_text(mnt_echeance)
                    doc = nlp(mnt_echeance)
                    for ent in doc.ents :
                        if ent.label_=="MONTANT" :   
                            mnt.montant=Montant()        
                            amount_currency = pattern_montant_devise.search(ent.text)    
                            if amount_currency !=None and amount_currency.group("montant")!=None:                              
                                mnt.montant.valeur = to_float(amount_currency.group("montant"))
                            if amount_currency !=None and amount_currency.group("devise")!=None:
                                mnt.montant.devise=amount_currency.group("devise")
                            break
                    periode.montant_echeances.append(mnt)
            amortissement.periodes.append(periode)
        return amortissement

    async def extract_caracteristiques_pret(self, text:str,tables)->CaracteristiquesPret:
        """
        Extract specific data for the loan
        text : extracted text from document
        return : Caracteristique instantiated class
        """
        caract:CaracteristiquesPret=CaracteristiquesPret()
        # Extract domicialiation 
        caract.domiciliation = await try_safe_execute_async(logger,self.extract_domiciliation,text=text)
        # list of loans
        # extract loan(s) description from Text
        match_caracterisitiques_pret_propose=pattern_caracteristiques_pret_description.search(text)
        if match_caracterisitiques_pret_propose==None or match_caracterisitiques_pret_propose.group("caracteristiques_pret_propose")==None:
            logger.warning("extract_caractisitiques: Description du pret proposé non trouvé")
        else :
            caract.description = sanitize_text(match_caracterisitiques_pret_propose.group("caracteristiques_pret_propose"))
            doc = nlp(caract.description)
            for ent in doc.ents :
                if ent.label_=="NUMERO":
                    caract.numero_pret = ent.text.replace("N","").replace("n","").replace("°","").strip() 
                elif ent.label_=="MONTANT":
                    caract.montant = ent.text
                    txt = ent.text.lower().replace("eur","").strip()
                    caract.montant_total_du_emprunteurs = await try_safe_execute_async(logger,self.extract_montant_total_du_par_emprunteur,montant_credit=txt,tables=tables)
            doc=None
        pattern_jusquau_dernier_point = re.compile(r"(CARACTERISTIQUES DU (PRET|CREDIT) PROPOSE)(?P<jusquau_dernier_point>.*\.)",re.DOTALL|re.MULTILINE)
        jusquau_dernier_point_match = pattern_jusquau_dernier_point.search(text)
        if jusquau_dernier_point_match !=None:
            jusquau_dernier_point=jusquau_dernier_point_match.group("jusquau_dernier_point")
            if jusquau_dernier_point!=None and jusquau_dernier_point!="":
                caract.taux= await try_safe_execute_async(logger,self.extract_taux,text=jusquau_dernier_point)
                doc = nlp(jusquau_dernier_point)
                for ent in doc.ents:
                    if ent.label_=="TAUX_BANCAIRE_IS_MODULABLE":
                        caract.is_modulable=True
                doc=None   
                if caract.domiciliation != None and caract.domiciliation.compte.strip()=="":
                    # 
                    search_num_compte =re.compile(r"Emprunteur *demande.*?Banque.*?échéances.*?prêt.*?perçues.*?compte *n° ?(?P<compte_domicialiation>[0-9]*)",re.IGNORECASE|re.DOTALL)
                    match = search_num_compte.search(jusquau_dernier_point)
                    if match!=None :
                        caract.domiciliation.compte = match.group("compte_domicialiation")      
        if caract!=None :
            # Extract Période d'amortissement
            amortissements:Amortissement = await try_safe_execute_async(logger,self.extract_amortissement_pret,text=text)
            if amortissements!=None:
                caract.periodes_amortissement= amortissements.periodes
        return caract
    
    async def traitement_recursif_caracteristiques_pret(self,text:str,tables,caracteristiques_prets:List[CaracteristiquePret])->List[CaracteristiquePret]:
        match_avec_reste_traiter = self.pattern_caracteristiques_avec_reste_traiter.search(text)
        if match_avec_reste_traiter==None :
            # il n'y a ou il ne reste qu'un seul
            match_un_pret=self.pattern_caracteristiques_un_pret.search(text)
            if match_un_pret != None :
                text_un_pret = match_un_pret.group("caracteristiques")
                if text_un_pret!=None and text_un_pret.strip()!="":
                    # on doit ajouter le texte supprimer par la regEx
                    text_un_pret = "CARACTERISTIQUES DU PRET PROPOSE\n"+text_un_pret
                    caract:CaracteristiquesPret = await try_safe_execute_async(logger,self.extract_caracteristiques_pret,text=text_un_pret,tables=tables)
                    if caract !=None :                            
                        caracteristiques_prets.append(caract)
            return caracteristiques_prets
        else :
            text_current_pret = match_avec_reste_traiter.group("caracteristiques")
            rat = match_avec_reste_traiter.group("reste_traiter")
            if text_current_pret!=None and text_current_pret.strip()!="":
                text_current_pret = "CARACTERISTIQUES DU PRET PROPOSE\n"+text_current_pret
                caract = await try_safe_execute_async(logger,self.extract_caracteristiques_pret,text=text_current_pret,tables=tables)
                if caract != None :
                    caracteristiques_prets.append(caract)
            if rat!=None and rat.strip()!="":
                rat = "CARACTERISTIQUES DU PRET PROPOSE\n"+rat
                return await try_safe_execute_async(logger,self.traitement_recursif_caracteristiques_pret,text=rat,caracteristiques_prets=caracteristiques_prets,tables=tables)
            return caracteristiques_prets

    async def extract_list_prets(sefl,tables)->List[CaracteristiquePret]:
        """
        Extrait la liste des prêts depuis le tableau CARACTERISTIQUES DU OU DES PRETS
        """
        if tables==None or tables==[] : 
            logger.warning("extract_caractéristiques: tables cannot be None or empty")
            return []

        #table 3
        # check table matches the expected value 
        # first line must be :
        # Nature du prêt    N° de prêt  Montant Devise  Durée en mois        
        t3_cptor=TextArrayComparator(["Nature du prêt","N° de prêt","Montant","Devise","Durée en mois"],nlp=settings.nlp_with_vectors)   
        candidates_tables:List[lxfTable]=search_table_by_text_array(t3_cptor,tables) 

        table_ok:bool = candidates_tables!=None and candidates_tables[0]!=None
        table = candidates_tables[0]
        if not table_ok :
            logger.warning("extract_caracteristiques: La table des caractéristiques du ou des prêts n'a pas été trouvée")
            return []
        else :
            list_prets:List[CaracteristiquePret]=[]
            # list of loans
            for i in range(1,len(table.rows)):
                row = table.rows[i]                        
                c:CaracteristiquePret=CaracteristiquePret()
                c.nature = row.cells[0].value
                c.numero = row.cells[1].value      
                amount:Montant=Montant()                  
                amount.valeur = to_float(row.cells[2].value)
                amount.devise = row.cells[3].value
                c.montant=amount
                duree = row.cells[4].value.lower().replace("mois","").replace("trimestres","")
                c.duree_mois = int(duree)
                list_prets.append(c)
            return list_prets
      
    async def extract_caracteristiques_prets(self, text:str,tables)->List[CaracteristiquePret]:
        """
        Return the list of loan specificities 
        """
        ### Patterns strategy

        caracteristiques:List[CaracteristiquesPret]=[]
        paragraphe_prets_matches = self.pattern_caracteristiques_paragraphe.search(text)
        if paragraphe_prets_matches!=None :
            caracteristiques_prets_text = paragraphe_prets_matches.group("caracteristiques_pret_propose")
            if caracteristiques_prets_text!=None and caracteristiques_prets_text.strip()!="":
                caracteristiques_prets_text = "CARACTERISTIQUES DU PRET PROPOSE\n"+caracteristiques_prets_text
                caracteristiques = await try_safe_execute_async(logger, self.traitement_recursif_caracteristiques_pret, text=caracteristiques_prets_text,caracteristiques_prets=caracteristiques,tables=tables)                    
        return caracteristiques
        
    async def extract_montant_total_du_par_emprunteur(self,montant_credit:str, tables) -> MontantTotalDuEmprunteur:
        """
        Extract total amount due by the loaner
        """
        if tables==None or tables==[]:
            logger.exception("extract_montant_total_du_par_emprunteur: Tables ne peut pas être None ou vide")
            return None
        montant_total:MontantTotalDuEmprunteur=MontantTotalDuEmprunteur()
        
        # check if table respect the format: 
        #                               Montant     Devise
        #   Montant total du crédit     XXXX.XX     EUR
        table_comparateur=TextArrayComparator(["Montant","Devise"],nlp=settings.nlp_with_vectors)
        candidate_tables = search_table_by_text_array(table_comparateur,tables)
        t4_ok:bool= candidate_tables!=None and len(candidate_tables)>0
        if not t4_ok :
            table_comparateur=TextArrayComparator([EMPTY_STR,"Montant","Devise"],nlp=settings.nlp_with_vectors)
            candidate_tables = search_table_by_text_array(table_comparateur,tables)
            t4_ok:bool= candidate_tables!=None and len(candidate_tables)>0
        if not t4_ok :
            logger.error("extract_montant_total_du_par_emprunteur: Table non trouvée")
            return None
        else :
            txt_comparateur:TextComparator= TextComparator(montant_credit,nlp=settings.nlp_with_vectors)
            for candidate in candidate_tables:
                t4:lxfTable=candidate 
                montant_total_credit_row:lxfRow=t4.rows[1]  
                if txt_comparateur.compare_to(montant_total_credit_row.cells[-2].value) >0.8 :                
                    total=0
                    # Montant total crédit
                    montant_total.montant_total_credit = Montant()
                    montant_total.montant_total_credit.valeur=to_float(montant_total_credit_row.cells[-2].value) # l'avant dernière cellule = Montant
                    montant_total.montant_total_credit.devise = montant_total_credit_row.cells[-1].value   # la dernière cellule = Devise
                    # il faut parcourir toutes les lignes du tableau pour reconnaitre les frais des autres coût comme par exemple les intérêts
                    total+=montant_total.montant_total_credit.valeur
                    txt_cptor_total_credit = TextComparator(text="Coût total du crédit pour l'emprunteur",nlp=settings.nlp_with_vectors)
                    txt_cptor_interets=TextComparator(text="Montant total des intérêts",nlp=settings.nlp_with_vectors)
                    txt_cptor_assurance = TextComparator("Montant total assurance emprunteur obligatoire",nlp=settings.nlp_with_vectors)

                    for i in range(2,len(t4.rows)) :
                        row:lxfRow=t4.rows[i]
                        label = row.cells[0].value
                        if row.cells[1].value.strip()!="" and not (txt_cptor_total_credit.compare_to(label) >=0.70):
                            total+=to_float(row.cells[1].value)
                        # les frais sont reconnaissables car le libellé commence par Frais                    
                        if label.startswith("Frais") :
                            # Frais 
                            frais:Frais=Frais()
                            frais.nature = row.cells[0].value
                            frais.montant=Montant()
                            frais.montant.valeur=to_float(row.cells[1].value)                            
                            frais.montant.devise=row.cells[2].value
                            montant_total.frais.append(frais)
                            
                        elif txt_cptor_interets.compare_to(label)>=0.70 :
                                # Montant total des intérêts
                                montant_total.montant_total_interets = Montant()
                                montant_total.montant_total_interets.valeur=to_float(row.cells[1].value)
                                montant_total.montant_total_interets.devise=row.cells[2].value
                                
                        elif txt_cptor_assurance.compare_to(label)>=0.70 :
                                # Montant total assurances
                                montant_total.montant_total_assurance_obligatoire= Montant()
                                montant_total.montant_total_assurance_obligatoire.valeur = to_float(row.cells[1].value)
                                montant_total.montant_total_assurance_obligatoire.devise = row.cells[2].value
                                
                        elif txt_cptor_total_credit.compare_to(label) >=0.70 :
                            # Cout total crédit   
                            montant_total.cout_total_credit=Montant()
                            montant_total.cout_total_credit.valeur=to_float(row.cells[1].value)
                            montant_total.cout_total_credit.devise=row.cells[2].value
                            
                        elif not (label==None or label.strip()==""):
                            # autre montant 
                            #logger.debug(f"Montant Label: {label}")
                            montant_divers:MontantDivers=MontantDivers()
                            montant_divers.nature = label
                            montant_divers.montant.valeur = to_float(row.cells[1].value)
                            montant_divers.montant.devise = row.cells[2].value
                            montant_total.montants_divers.append(montant_divers)
                            
                    t5:lxfTable=None
                    t5_cptor=TextArrayComparator(["Montant total dû par l'Emprunteur *","",""],nlp=settings.nlp_with_vectors)   
                    candidate_tables = search_table_by_text_array(t5_cptor, tables,limit=1)
                    if candidate_tables!=None and len(candidate_tables)>0 : 
                        # rechercher la table dont le montant total est quasiment égal au total calculé précédemment à 100 près 
                        for t in candidate_tables:
                            s= to_float(t.rows[0].cells[1].value)
                            if abs(total-s)<=100.0 :
                                t5=t
                                break
                    else :
                        t5_cptor=TextArrayComparator(["COUT TOTAL",JOKER_STR,JOKER_STR],nlp=settings.nlp_with_vectors)   
                        candidate_tables = search_table_by_text_array(t5_cptor, tables,limit=1)
                        if candidate_tables!=None and len(candidate_tables)>0:
                            # rechercher la table dont le montant total est quasiment égal au total calculé précédemment à 100 près 
                            for t in candidate_tables:
                                s= to_float(t.rows[0].cells[1].value)
                                if abs(total-s)<=100.0 :
                                    t5=t
                                    break
                    if t5!=None :
                        montant_total_du_emprunteur_row:lxfRow=t5.rows[0]        
                        montant_total.montant_total_du_emprunteur=Montant()
                        montant_total.montant_total_du_emprunteur.valeur=to_float(montant_total_du_emprunteur_row.cells[1].value)
                        montant_total.montant_total_du_emprunteur.devise=montant_total_du_emprunteur_row.cells[2].value            
        return montant_total

    async def extract_taux(self,text:str)-> TauxAnnuelEffectifGlobal:
        """
        """
        regex = r"taux *effectif *global.*à (?P<TEG>[0-9]{1,2}((\.|,)[0-9]+)?) *%.*taux *de *(?P<TAUX>[0-9]{1,2}((\.|,)[0-9]+)) *%"
        taux:TauxAnnuelEffectifGlobal=TauxAnnuelEffectifGlobal()
        doc = nlp(text)
        for ent in doc.ents:            
            if ent.label_=="TAUX_BANCAIRE":        
                taux.description = ent.text              
                # read 30 more tokens
                suite = str(doc[ent.end:ent.end+30])
                full_sentence=ent.text+suite
                # find TEG and monthly rate
                matches = re.search(regex, full_sentence, re.DOTALL)
                if matches!=None and len(matches.groups())>0:
                    teg=matches.group("TEG")
                    taux.taux_pourcentage = to_float(teg)
                    monthly_rate=matches.group("TAUX")    
                    taux.taux_periode = to_float(monthly_rate)
                    # get the all description including the monthly rate 
                    taux.description = full_sentence.split(".")[0]
                else :
                    tx=nlp(ent.text.lower().replace("taux","taux_"))
                    for ent_tx in tx.ents:
                        if ent_tx.label_=="POURCENTAGE" :
                            taux.taux_pourcentage = to_float(ent_tx.text.replace("%","").replace(",","."))
                        elif ent_tx.label_=="PERIODE":
                            taux.base_periode=ent_tx.text
            elif ent.label_=="TAUX_BANCAIRE_TITRE":
                taux.titre = ent.text
            elif ent.label_=="TAUX_BANCAIRE_SIGLE" :
                taux.sigle = ent.text 
        doc=None
        return taux
    
    async def extract_short_header(self,text:str):
        """
        Extract the short header f
        return : header_ref,header_emprunteur, header_responsable_suivi
        """
        header_emprunteur=""
        header_responsable_suivi=""
        header_ref=""        
        match_header = pattern_short_header.search(text)
        if not(match_header==None or match_header.groups()==None) :
                header_ref = sanitize_text(match_header.group("ref"))
                header_emprunteur = sanitize_text(match_header.group("entite_suivi"))
                header_responsable_suivi = sanitize_text(match_header.group("responsable_suivi"))     
        return header_ref, header_emprunteur,header_responsable_suivi   
    async def extract_header_pro(self,text:str) :
        """
        Extract the header for a professional loan
        return : header_emprunteur, num_suivi,header_offre, header_num_etude,header_responsable_suivi
        """
        header_emprunteur=""
        num_suivi="" 
        header_offre="" 
        header_num_etude=""
        header_responsable_suivi=""
        match_header = pattern_header.search(text)
        if not( match_header == None or match_header.groups()==None or match_header.group("num_suivi")==None) :
            num_suivi = sanitize_text(match_header.group("num_suivi"))
            header_offre=sanitize_text(match_header.group("num_offre"))
            header_emprunteur = sanitize_text(match_header.group("entite_suivi"))
            header_num_etude = sanitize_text(match_header.group("num_etude"))
            header_responsable_suivi = sanitize_text(match_header.group("responsable"))

        return header_emprunteur, num_suivi,header_offre, header_num_etude,header_responsable_suivi

    async def extract_header_particulier(self,text:str):
        """
        """ 
        header_emprunteur=""
        num_suivi="" 
        header_ref="" 
        header_num_etude=""
        header_responsable_suivi=""
        match_header = pattern_header_particulier.search(text)
        if not( match_header == None or match_header.groups()==None or match_header.group("num_suivi")==None) :
            num_suivi = sanitize_text(match_header.group("num_suivi"))
            header_ref=sanitize_text(match_header.group("ref"))
            header_emprunteur = sanitize_text(match_header.group("entite_suivi"))
            header_responsable_suivi = sanitize_text(match_header.group("responsable"))
        return header_emprunteur, num_suivi,header_ref, header_num_etude,header_responsable_suivi        

    async def extract_num_suivi(self,text:str)->str:
        """
        Extract the follow up number for the loan ie: N° de suivi 
        return the followup number (999999)
        """
        num_text=""
        match_num_suivi = pattern_num_suivi.search(text)
        if not (match_num_suivi == None or match_num_suivi.groups()==None or match_num_suivi.group("num_suivi")==None):            
            num_text = sanitize_text(match_num_suivi.group("num_suivi"))
            #logger.debug(f"N° suivi {num_text}")
        else :
            text = sanitize_CRD_border_side_effect(text)
            match_num_suivi = pattern_entite_num_suivi.search(text)
            if not (match_num_suivi == None or match_num_suivi.groups()==None or match_num_suivi.group("num_suivi")==None):            
                num_text = sanitize_text(match_num_suivi.group("num_suivi"))
                #logger.debug(f"N° suivi {num_text}")
        return num_text

    async def extract_date_offre(self,text:str)->str:
        """
        Extract the date of the loan offer
        return the date if found 
        """
        date:str=""        
        match_offre_date = pattern_date_offre.search(text)
        if match_offre_date==None or match_offre_date.groups()==None or (match_offre_date.group("date_offre")==None and match_offre_date.group("date_litteral_offre")==None): return ""
        if match_offre_date.group("date_offre")!=None :
            offre_date_text = sanitize_text(match_offre_date.group("date_offre"))
        if match_offre_date.group("date_litteral_offre")!=None :
            offre_date_text = sanitize_text(match_offre_date.group("date_litteral_offre"))
        #logger.debug(f"Texte de date de l'offre détecté:\n{offre_date_text}")
        if not offre_date_text==None:
            doc=nlp(offre_date_text)
            for ent in doc.ents:
                if ent.label_=="DATE": 
                    date =sanitize_date(ent.text)
                    break
                if ent.label_=="LITTERAL_DATE":
                    date = ent.text
                    break
        return date

    def get_tables_assurance(self,tables) :        
        #table Quotité du prêt
        hdr_insurance_table = ["Quotité du prêt assurée","Quotité assurance obligatoire","Quotité assurance facultative"]
        hdr_cptor= TextArrayComparator(hdr_insurance_table,nlp=settings.nlp_with_vectors)
        insurances_tables = search_table_by_text_array(hdr_cptor=hdr_cptor,tables=tables) 
        if insurances_tables!=None and  insurances_tables!=[] :
            return insurances_tables
        # Table Prêt(s) assuré(s)
        hdr_insurance_table = ["Prêt(s) assuré(s)","Capitaux assurés","Montant de la prime mensuelle","Coût de l'assurance","Dont coût d'assurance obligatoire"]
        hdr_cptor= TextArrayComparator(hdr_insurance_table,nlp=settings.nlp_with_vectors)
        insurances_tables = search_table_by_text_array(hdr_cptor=hdr_cptor,tables=tables) 
        if insurances_tables!=None and  insurances_tables !=[] : 
            return insurances_tables
        return None
      
    async def extract_assurrances_nlp(self, text)->List[assurance_type]:
        startswith_stop_words="sous réserve"
        doc=nlp(text)
        start=0
        end=0
        type=""
        assurances:List[assurance_type]=[]
        for ent in doc.ents:
            if ent.label_==label_type_assurance :
                end=ent.start
                txt = str(doc[start:end])
                if txt.replace("\n","").replace("-","").strip()!="":
                    if not txt.startswith(startswith_stop_words) :
                        assu_type:assurance_type=assurance_type()
                        assu_type.type = type
                        assu_type.start=start
                        assu_type.end=end
                        assu_type.text=sanitize_text(txt)
                        assurances.append(assu_type)
                    else :
                        if len(assurances)>0 :
                            assurances[-1].text+=assurances[-1].type+" "+txt                       
                start =ent.end
                type=ent.text
            last_ent=ent

        end=len(doc)
        txt = str(doc[start:end])
        if txt.strip()!="" and not txt.startswith(startswith_stop_words):
            assu_type:assurance_type=assurance_type()
            assu_type.type = type
            assu_type.start=start
            assu_type.end=end
            assu_type.text=sanitize_text(txt)
            assurances.append(assu_type)   
        elif txt.startswith(startswith_stop_words):
            assurances[-1].text+=assurances[-1].type+" "+txt 
        doc =None
        return assurances
    
    async def extract_assurances_new(self,text,tables)->List[Assurance] :
        """
        Extract all assurances
        """
        exclusion_list=["assurance groupe","assurance externe"]
        souscrite_par="souscrite par"
        delegation="délégation"
        assurance_externe_titre="ASSURANCE EXTERNE"
        assurance_groupe_titre="ASSURANCE GROUPE"
        groupe_nom_naissance="nom_naissance"
        groupe_assureur ="assureur"
        groupe_hauteur ="hauteur"
        groupe_couverture="couverture"
        groupe_assurance_paragraphe="assurance_paragraphe"
        groupe_assurance_groupe="assurance_groupe"
        groupe_quotite_pret="quotite_pret"
        groupe_options_choisies="options_choisies"
        groupe_souscripteur ="souscripteur"
        groupe_date_naissance="date_naissance"
        groupe_ville_naissance="ville_naissance"
        groupe_assurances="assurances"
        assurances:List[Assurance]=[]
        match_assurances = self.pattern_assurances.search(text)
        if match_assurances == None : return assurances
        match_assurances_text = sanitize_text(match_assurances.group(groupe_assurances))
        assurances_type:List[assurance_type] = await try_safe_execute_async(logger,self.extract_assurrances_nlp,text=match_assurances_text)
        if len(assurances_type)>0:
            tables_assurances = self.get_tables_assurance(tables)
            nb_assurance_found=0
            for assu_type in assurances_type:
                # tips skip the empty record
                if assu_type.text.lower() in exclusion_list: continue
                nb_assurance_found+=1
                text = assu_type.type +" " + assu_type.text
                assurance:Assurance=Assurance()
                assurance.type_assureur=assu_type.type
                assurance.description = text.replace(assurance_externe_titre,"").replace(assurance_groupe_titre,"")
                if assu_type.type.lower().startswith(delegation):
                    assurance.delegation=assu_type.type
                    m = self.delegation_assurance_pattern.search(text )
                    if m!=None :
                        assurance.nom_naissance_souscripteur =sanitize_text(m.group(groupe_nom_naissance))          
                        assurance.assureur = sanitize_text(m.group(groupe_assureur))
                        assurance.hauteur_pourcentage=to_float(m.group(groupe_hauteur))
                        assurance.couverture =sanitize_text(m.group(groupe_couverture))
                    match_assurance3 = self.assurance_pattern_3.search(text)
                    if match_assurance3 != None :
                        assurance.couverture = sanitize_text(match_assurance3.group(groupe_couverture))
                else :
                    match_assurance_paragraphe= self.assurance_paragraphe_pattern.search(text)
                    match_assurance_paragraphe_souscrite_par= self.assurance_paragraphe_pattern_souscrite_par.search(text)
                    assurance_paragraph_text=""
                    if match_assurance_paragraphe != None : 
                        assurance_paragraph_text =sanitize_text(match_assurance_paragraphe.group(groupe_assurance_paragraphe))
                        assurance.assureur_group =sanitize_text(match_assurance_paragraphe.group(groupe_assurance_groupe))
                    elif match_assurance_paragraphe_souscrite_par!=None :
                        assurance_paragraph_text = souscrite_par +  sanitize_text(match_assurance_paragraphe_souscrite_par.group(groupe_assurance_paragraphe))
                        assurance.assureur_group = sanitize_text(match_assurance_paragraphe_souscrite_par.group(groupe_assurance_groupe))
                    if assurance_paragraph_text.strip() !="" :
                        match_assurance  = self.assurance_pattern.search(assurance_paragraph_text)
                        match_assurance2 = self.assurance_pattern_2.search(assurance_paragraph_text)
                        match_assurance3 = self.assurance_pattern_3.search(assurance_paragraph_text)
                        match_assurance4 = self.assurance_pattern_4.search(assurance_paragraph_text)
                        if match_assurance != None:
                            assurance.souscripteur = sanitize_text(match_assurance.group(groupe_souscripteur))
                            assurance.nom_naissance_souscripteur = sanitize_text(match_assurance.group(groupe_nom_naissance))
                            assurance.date_naissance_souscripteur = sanitize_date(match_assurance.group(groupe_date_naissance))
                            assurance.ville_naissance_souscripteur = sanitize_text(match_assurance.group(groupe_ville_naissance))
                            assurance.assureur = sanitize_text(match_assurance.group(groupe_assureur))
                            assurance.quotite_pret_assure = sanitize_text(match_assurance.group(groupe_quotite_pret))
                            if not match_assurance.group(groupe_options_choisies) == None :
                                assurance.options_choisies =sanitize_text(match_assurance.group(groupe_options_choisies))
                        if  match_assurance2 != None :
                            assurance.souscripteur = sanitize_text(match_assurance2.group(groupe_souscripteur))
                            assurance.nom_naissance_souscripteur = sanitize_text(match_assurance2.group(groupe_nom_naissance))
                            assurance.date_naissance_souscripteur = sanitize_date(match_assurance2.group(groupe_date_naissance))
                            assurance.ville_naissance_souscripteur = sanitize_text(match_assurance2.group(groupe_ville_naissance))
                            assurance.nom_naissance_souscripteur = sanitize_text(match_assurance2.group(groupe_nom_naissance))
                            assurance.couverture = sanitize_text(match_assurance2.group(groupe_couverture))
                        if match_assurance3 !=None :
                            assurance.couverture = sanitize_text(match_assurance3.group(groupe_couverture))
                        if match_assurance4 !=None :
                            assurance.souscripteur = sanitize_text(match_assurance4.group(groupe_souscripteur))
                            assurance.nom_naissance_souscripteur = sanitize_text(match_assurance4.group(groupe_nom_naissance))
                            assurance.date_naissance_souscripteur = sanitize_date(match_assurance4.group(groupe_date_naissance))
                            assurance.ville_naissance_souscripteur = sanitize_text(match_assurance4.group(groupe_ville_naissance))
                            assurance.assureur = sanitize_text(match_assurance4.group(groupe_assureur))
                            assurance.quotite_pret_assure = sanitize_text(match_assurance4.group(groupe_quotite_pret))
                #Extract the more globals properties 
                doc = nlp(text)
                garanties=""
                for ent in doc.ents :
                    if ent.label_==label_garantie_assurance:
                        if not(ent.text in garanties):
                            if garanties=="":
                                garanties = sanitize_text(ent.text)
                            else:
                                garanties+=sanitize_text(", "+ent.text)     
                    elif ent.label_==label_personne and assurance.souscripteur.strip()=="":
                        assurance.souscripteur = ent.text
                    elif ent.label_==label_date_naissance and assurance.date_naissance_souscripteur.strip()=="":
                        assurance.date_naissance_souscripteur=sanitize_date(ent.text)
                    elif ent.label_==label_ville and assurance.ville_naissance_souscripteur.strip()=="": # assume it's Ville de naissance
                        assurance.ville_naissance_souscripteur=ent.text
                    elif ent.label_==label_address:
                        # if found address add it before city
                        assurance.ville_naissance_souscripteur = ent.text +" "+ assurance.ville_naissance_souscripteur
                doc=None
                if garanties!="":
                    assurance.garanties = garanties
                assurances.append(assurance)  
                # search for tables 
                if tables_assurances !=None and len(tables_assurances)>=nb_assurance_found:
                    table:lxfTable = tables_assurances[nb_assurance_found-1]
                    if table != None :
                        assurance.tableau_prets = table
        return assurances        
    
    async def extract_delegations_assurances(self,text,tables)->List[Assurance]:
        """
        extract the list of delegated insurances
        return the delegated insurances list if found , None else
        """
        assurances:List[Assurance]=[]
        match_assurances = self.pattern_assurances.search(text)
        if match_assurances == None : return assurances
        match_assurances_text = sanitize_text(match_assurances.group("assurances")) 
                
        
        #logger.debug(f"Match delegations assurances : {match_assurances_text}")
        delegations = match_assurances_text.split("Délégation")        
        # matches_delegations_assurances = self.multi_delegation_assurance_pattern.search(match_assurances_text)
        if delegations == None: return assurances
        tables_assurances = self.get_tables_assurance(tables)
        nb_assurance_found=0
        for delegation_assurance_found in delegations:
            if delegation_assurance_found.strip()=="-" :
                continue
            #delegation_assurance_found = matches_delegations_assurances.group(index)
            delegation_assurance_found = "Délégation"+delegation_assurance_found
            #logger.debug(f"Delegation Assurance found : {delegation_assurance_found}")
            m = self.delegation_assurance_pattern.search(delegation_assurance_found )
            if m!=None :
                nb_assurance_found+=1 
                assurance:Assurance=Assurance()
                assurance.description = m.string            
                assurance.delegation= m.group("delegation")
                assurance.souscripteur = m.group("souscripteur")
                assurance.nom_naissance_souscripteur = m.group("nom_naissance")
                assurance.date_naissance_souscripteur=m.group("date_naissance")
                assurance.ville_naissance_souscripteur = m.group("ville_naissance")            
                assurance.garanties = m.group("risques")
                assurance.assureur = m.group("assureur")
                assurance.hauteur_pourcentage=to_float(m.group("hauteur"))
                assurance.couverture = m.group("couverture")  
                # Check for Garanties,Ville Naissance, Date Naissance or Souscripteur by NER 
                doc = nlp(delegation_assurance_found)
                garanties=""
                type_assureur="" 
                for ent in doc.ents :
                    if ent.label_=="GARANTIE_ASSURANCE":
                        if not(ent.text in garanties):
                            if garanties=="":
                                garanties = sanitize_text(ent.text)
                            else:
                                garanties+=sanitize_text(", "+ent.text)     
                    elif ent.label_=="PERSONNE":
                        assurance.souscripteur = ent.text
                    elif ent.label_=="DATE_NAISSANCE":
                        assurance.date_naissance_souscripteur=sanitize_date(ent.text)
                    elif ent.label_=="VILLE" : # assume it's Ville de naissance
                        assurance.ville_naissance_souscripteur=ent.text
                    elif ent.label_=="TYPE_ASSURANCE" :
                        if not(ent.text in type_assureur) :
                            type_assureur+=ent.text
                doc=None
                if garanties!="":
                    assurance.garanties = garanties
                if type_assureur!="":
                    assurance.type_assureur = type_assureur
                assurances.append(assurance)   
                # search for tables 
                if tables_assurances !=None and len(tables_assurances)>=nb_assurance_found:
                    table:lxfTable = tables_assurances[nb_assurance_found-1]
                    if table != None :
                        assurance.tableau_prets = table
        return assurances 

    async def extract_assurances(self,text,tables)->List[Assurance]:
        """
        extract the list of insurances
        return the  insurances list if found , [] else
        """
        assurances:List[Assurance]=[]
        match_assurances = self.pattern_assurances.search(text)
        match_assurances_text = sanitize_text(match_assurances.group("assurances"))
        ##logger.debug(f"Match assurances : {match_assurances_text}")
        matches_assurance_paragraphe_pattern=[]
        if "- Assurance groupe " in match_assurances_text :
            matches_assurance_paragraphe_pattern = match_assurances_text.split("- Assurance groupe")#self.assurance_paragraphe_pattern.finditer( match_assurances_text)
            assurance_pattern_group = self.assurance_paragraphe_pattern
        elif "Assurance groupe "in match_assurances_text:
                matches_assurance_paragraphe_pattern.append(match_assurances_text)
                assurance_pattern_group = self.assurance_paragraphe_pattern_souscrite_par
        if matches_assurance_paragraphe_pattern == [] : 
            #logger.warning(f"Pas de correspondance assurance pour {match_assurances_text}")
            return assurances
        # get insurances tables for once 
        tables_assurance = self.get_tables_assurance(tables)
        ##logger.debug(f"Assurance matches {matches_assurance_paragraphe_pattern}")  
        nb_assurance_found=0
        for i,assurance_groupe in enumerate(matches_assurance_paragraphe_pattern):
            if assurance_groupe!=None and assurance_groupe.strip()!="" :
                assurance_groupe="- Assurance groupe"+assurance_groupe
                ##logger.debug(f"Assurance groupe:\n{assurance_groupe}")
                m = assurance_pattern_group.search( assurance_groupe)
                if m!=None :
                    nb_assurance_found+=1 
                    ##logger.debug(f"Match Assurance: {m.string}")
                    assurance:Assurance=Assurance()
                    assurance.description=m.string
                    assurance.assureur_group =sanitize_text(m.group("assurance_groupe"))
                    assurance_paragraph_text = sanitize_text(m.group("assurance_paragraphe"))
                    ##logger.debug(f"Assurance paragraphe : {assurance_paragraph_text}")
                    match_assurance = self.assurance_pattern.search(assurance_paragraph_text)
                    match_assurance2 = self.assurance_pattern_2.search(assurance_paragraph_text)
                    if not (match_assurance == None):
                        ##logger.debug(f"Match assurance: {match_assurance.string}")
                        assurance.souscripteur = match_assurance.group("souscripteur").replace("\n"," ")
                        assurance.nom_naissance_souscripteur = match_assurance.group("nom_naissance").replace("\n"," ")
                        assurance.date_naissance_souscripteur=match_assurance.group("date_naissance").replace("\n"," ")
                        assurance.ville_naissance_souscripteur = match_assurance.group("ville_naissance").replace("\n"," ")
                        assurance.assureur = match_assurance.group("assureur").replace("\n"," ")
                        assurance.type_assureur = match_assurance.group("type_assureur").replace('\n',' ')
                        assurance.quotite_pret_assure = match_assurance.group("quotite_pret").replace("\n"," ")
                        assurance.garanties = match_assurance.group("garanties").replace("\n"," ")
                        if not match_assurance.group("options_choisies") == None :
                            assurance.options_choisies = match_assurance.group("options_choisies").replace("\n"," ")                            
                    elif  not match_assurance2==None :
                        # #logger.debug(f"Match assurance2: {match_assurance.string}")
                        assurance.souscripteur = match_assurance2.group("souscripteur")
                        assurance.nom_naissance_souscripteur = match_assurance2.group("nom_naissance")
                        assurance.date_naissance_souscripteur = match_assurance2.group("date_naissance")
                        assurance.ville_naissance_souscripteur = match_assurance2.group("ville_naissance")
                        assurance.garanties = match_assurance2.group("garanties")
                        assurance.couverture = match_assurance2.group("couverture")
                        #assurance.description = match_assurance2.group("description")
                    # Check for Garanties,Ville Naissance, Date Naissance or Souscripteur by NER 
                    doc = nlp(m.string)
                    garanties=""
                    type_assureur=""
                    for ent in doc.ents :
                        if ent.label_=="GARANTIE_ASSURANCE":
                            if not(ent.text in garanties):
                                if garanties=="":
                                    garanties = sanitize_text(ent.text)
                                else:
                                    garanties+=sanitize_text(", "+ent.text)
                        elif ent.label_=="PERSONNE":
                            assurance.souscripteur = ent.text
                        elif ent.label_=="DATE_NAISSANCE":
                            assurance.date_naissance_souscripteur=sanitize_date(ent.text)
                        elif ent.label_=="VILLE" : # assume it's Ville de naissance
                            assurance.ville_naissance_souscripteur=ent.text
                        elif ent.label_=="TYPE_ASSURANCE" :
                            if not(ent.text in type_assureur) :
                                type_assureur+=ent.text
                    if garanties!="":
                        assurance.garanties = garanties
                    if type_assureur!="":
                        assurance.type_assureur = type_assureur
                    doc=None
                    # search for tables 
                    if tables_assurance !=None and len(tables_assurance)>=nb_assurance_found:
                        table:lxfTable = tables_assurance[nb_assurance_found-1]
                        if table != None :
                            assurance.tableau_prets = table
                    assurances.append(assurance)
        return assurances 

    async def extract_tableau_ammortissements(self,tables=[])->lxfTable:
        """
        """
        tableau_amortissement:lxfTable=lxfTable()
        amortissement_entete=["TERME","INTERETS","ASSURANCES","COMMISSIONS","AMORTISSEMENTS","MONTANT ECHEANCE","CAPITAL RESTANT DU","ELEMENTS CAPITALISES","SOMMES TOTALES RESTANT DUES"]      
        hdr_cptor=TextArrayComparator(amortissement_entete,nlp=settings.nlp_with_vectors)
        # Retourne une liste de tables correspondante aux entêtes fournies
        tables_found = search_table_by_text_array(hdr_cptor=hdr_cptor,tables=tables)
        if tables_found!=None and len(tables_found)> 0 :
            # on ne prend que la première table touvée
            tableau_amortissement = tables_found[0]
        else :
            logger.warning(f"Aucun tableau d'ammortissement n'a pu être trouvé avec l'entête similaire à :\n{';'.join(amortissement_entete)}")
        return tableau_amortissement
 
    async def extract_domiciliation(self, text)->Domiciliation:
        """
        Extract the domiciliation data
        return Domiciliation
        """
        domiciliation:Domiciliation=Domiciliation()
        match_paragraph_domiciliation = pattern_pragraphe_domiciliation.search(text)
        if match_paragraph_domiciliation ==None :
            return domiciliation
        match_paragraph_domiciliation_text = sanitize_text(match_paragraph_domiciliation.group("domiciliation"))        
        doc = nlp(match_paragraph_domiciliation_text)
        matches = matcher(doc)        
        matches.sort(key = lambda x: x[1])
        for match in matches:
            if match[0]==domiciliation_key_matcherkey :
                domiciliation_trouvee=str(doc[match[1]:match[2]])
                doc_domiciliation=nlp(domiciliation_trouvee)
                for ent in doc_domiciliation.ents :
                    if ent.label_== "QUALITE" :
                        domiciliation.debiteur = ent.text
                    elif ent.label_ == "NUM_COMPTE" : 
                        domiciliation.compte = ent.text
                    elif ent.label_ == "ORG_RAISON_SOCIALE" :
                        domiciliation.creancier = ent.text
        result = pattern_domiciliation_num_compte.search(match_paragraph_domiciliation_text)
        if result!=None:
            num_compte=result.group("num_compte")
            if num_compte!=None: domiciliation.compte=num_compte
            debiteur=result.group("debiteur")
            if debiteur!=None : domiciliation.debiteur=debiteur
        return domiciliation

    async def extract_garanties(self,text)->List[Warranty]:
        match_paragraphe_garanties= patterns_paragraphe_garanties.search(text)
        if match_paragraphe_garanties==None : return []
        match_paragraphe_garanties_text = match_paragraphe_garanties.group("garanties") #sanitize_text(match_paragraphe_garanties.group("garanties"))
        #logger.debug(f"Garanties paragraphe trouvé {match_paragraphe_garanties_text}")
        match_paragraphe_garanties_text = sanitize_garanties_text(match_paragraphe_garanties_text)
        doc_garanties=nlp(match_paragraphe_garanties_text)
        matches = matcher_garantie(doc_garanties)
        #logger.debug(f"Garanties matches {matches}")
        warranties:List[Warranty]=[]
        for match in matches:
            if match[0]==garanties_key_matcherkey :
                # Garantie Financiere
                start = match[1]
                end = match[2]
                garantie_trouvee=str(doc_garanties[start:end])
                # NLP for the warranties found 
                dd = nlp(garantie_trouvee)
                dd_start = 0
                #logger.debug(f"Garantie trouvée:\n{garantie_trouvee}")
                previous_warranty=None
                # Spliting the warranties inside an array of warranty 
                for ent in dd.ents :

                    if ent.label_=="GARANTIE_FINANCIERE" :
                        dd_end = ent.start-1
                        warranty:Warranty=Warranty()
                        warranty.label=str(ent.text)                           
                        warranties.append(warranty)  
                        if previous_warranty!=None :
                            previous_warranty.text=sanitize_text(f"{previous_warranty.label} {str(dd[dd_start:dd_end])}" )
          
                        previous_warranty=warranty
                        dd_start =ent.end

 
                if previous_warranty!=None : 
                    previous_warranty.text = sanitize_text(f"{previous_warranty.label} {str(dd[dd_start:])}")
                    # looking for DUREE and DUREE_LIMITE ; we must work on sanitize text 
                    if previous_warranty.text!=None :
                        ddd = nlp(previous_warranty.text)
                        for ent in ddd.ents :
                            if ent.label_=="DUREE" :
                                duree, unite = extract_duree_from_text(ent.text)
                                if duree!="" :
                                    previous_warranty.duree= duree
                                    previous_warranty.duree_unite=unite
                                else :
                                    previous_warranty.duree=ent.text
                            if ent.label_=="DUREE_LIMITEE":
                                duree,unite = extract_duree_from_text(ent.text)
                                if duree!="" :
                                    previous_warranty.duree_limitee=duree
                                    previous_warranty.duree_limitee_unite = unite
                                else :
                                    previous_warranty.duree_limitee=ent.text
                                
                dd=None 
                # Display the array of warranties  
                for warranty in warranties :
                    warranty.text = preprocess_code_postal_09999(warranty.text)
                    doc_garantie = nlp(warranty.text)
                    for ent in doc_garantie.ents:
                        if ent.label_=="NUMERO" :
                            num=str(ent.text) 
                            warranty.numero_pret = sanitize_numero(num)
                        elif ent.label_ =="CADASTRE" :
                            warranty.ref_cadastrales = sanitize_ref_cadastrales(str(ent.text))
                    
                    # looking for cadastre building address
                    matches = re.finditer(regex_adresse_immeuble_cadastre, warranty.text, re.IGNORECASE | re.MULTILINE)
                    for match in matches:
                        if match.groups!=None :
                            adresse_imeuble_cadastre = match.group("adresse_immeuble_cadastre")
                            if adresse_imeuble_cadastre!=None :
                                warranty.text_adresse_immeuble_cadastre = adresse_imeuble_cadastre
                                doc_adresse_immeuble_cadastre = nlp(adresse_imeuble_cadastre)
                                for ent in doc_adresse_immeuble_cadastre.ents:
                                    if ent.label_=="ADRESSE":
                                        warranty.adresse_immeuble_cadastre = ent.text
                                    elif ent.label_=="CODE_POSTAL":
                                        warranty.code_poste_immeuble_cadastre = ent.text
                                    elif ent.label_ =="VILLE":
                                        warranty.ville_immeuble_cadatre = ent.text
                                
                    matches_garantie = matcher_garantie(doc_garantie)
                    for match in matches_garantie:

                        if match[0]==garantie_hauteur_matcherkey:
                            # Extract Hauteur
                            for ent in doc_garantie.ents:

                                if ent.label_ =="MONTANT":
                                    warranty.hauteur=ent.text 
                                    break
                        elif match[0]==garantie_rang_matcherkey:
                            # Extract Rang
                            warranty.rang = str(doc_garantie[match[2]-1:match[2]])
                        elif match[0]==garantie_cout_approximatif_matcherkey:  
                            for ent in doc_garantie.ents:
                                if ent.label_ =="MONTANT" and ent.start==match[2]-1:
                                    warranty.cout_approximatif =ent.text 
                                    break                   
                
                        # Get Office Name and address
                        m = pattern_garantie_office_notaire.search(warranty.text)
                        # sanitize the text at this point since we won't need FF and CR information 
                        warranty.text = sanitize_text(warranty.text)
                        if not (m==None or m.groups()==None) :
                            warranty.office_notarial = m.group("office_notarial")
                            adr = m.group("adresse_office_notarial")
                            adr = adr.replace(',',', ')
                            doc = nlp(adr) 
                            for ent in doc.ents :
                                if ent.label_=="ADRESSE" :
                                    warranty.adresse_office_notarial = sanitize_address(ent.text)
                                elif ent.label_=="CODE_POSTAL":
                                    warranty.code_postal_office_notarial=ent.text
                                elif ent.label_=="VILLE":
                                    warranty.ville_office_notarial=ent.text
   

        return warranties        
    
    async def traitement_recursif_clauses_particuliers(self, text:str,clauses:List[ClausesParticulieres])->List[ClausesParticulieres]:
        match_avec_reste_traiter = self.pattern_clauses_particulieres_reste_traiter.search(text)
        if match_avec_reste_traiter==None :
            current_clauses:ClausesParticulieres = ClausesParticulieres()
            current_clauses.titre="Clause(s) Particulières (s)"
            match_clauses_seules = self.pattern_clauses_particulieres_seules.search(text)
            if match_clauses_seules !=None :
                txt = match_clauses_seules.group("clauses_particulieres")
                match_jusquau_dernier_point =self.pattern_jusquau_dernier_point.search(txt)
                if match_jusquau_dernier_point!=None:
                    txt_clauses = match_jusquau_dernier_point.group("clauses_particulieres_jusquau_dernier_point")
                    # keep the paragraph mark as § = \n\n
                    txt_clauses = txt_clauses.replace("\n\n","§")
                    current_clauses.text = sanitize_text(txt_clauses)
                else :
                    txt = txt.replace("\n\n","§")
                    current_clauses.text = sanitize_text(txt)
                rattachement = match_clauses_seules.group("rattachement")
                if rattachement !=None and rattachement!="" :
                    current_clauses.titre =current_clauses.titre+rattachement.replace('\n','')
                    doc = nlp(rattachement)
                    for ent in doc.ents :
                        if ent.label_=="NUMERO" :
                            current_clauses.numero_pret = sanitize_numero(ent.text)
                            break
                    doc=None
                clauses.append(current_clauses)            
            return clauses
        else :
            txt = match_avec_reste_traiter.group("clauses_particulieres")
            rattachement = match_avec_reste_traiter.group("rattachement")
            rat = match_avec_reste_traiter.group("reste_traiter") 
            if txt !=None and txt.strip()!="":
                current_clauses:ClausesParticulieres = ClausesParticulieres()
                current_clauses.titre="Clause(s) Particulière(s)"
                match_jusquau_dernier_point =self.pattern_jusquau_dernier_point.search(txt)
                if match_jusquau_dernier_point!=None:
                    txt_clauses = match_jusquau_dernier_point.group("clauses_particulieres_jusquau_dernier_point")
                    # keep the paragraph mark as § = \n\n
                    txt_clauses = txt_clauses.replace("\n\n","§")
                    current_clauses.text = sanitize_text(txt_clauses)
                else :
                    txt = txt.replace("\n\n","§")
                    current_clauses.text = sanitize_text(txt)
                if rattachement !=None and rattachement!="" :
                    current_clauses.titre =current_clauses.titre+rattachement.replace('\n','')
                    doc = nlp(rattachement)
                    for ent in doc.ents :
                        if ent.label_=="NUMERO" :
                            current_clauses.numero_pret = sanitize_numero(ent.text)
                            break
                    doc=None
                clauses.append(current_clauses)
            if rat!=None :
                rat = "CLAUSE(S) PARTICULIERE(S)"+rat
                return await try_safe_execute_async(logger,self.traitement_recursif_clauses_particuliers,text=rat,clauses=clauses)
            else :
                return clauses        
    
    async def extract_clauses_particulieres(self,text)->List[ClausesParticulieres]:
        clauses:List[ClausesParticulieres]=[]
        clauses_paragraph_found = self.pattern_clauses_particulieres_paragraphe.search(text)
        if clauses_paragraph_found!=None:            
            txt = "CLAUSE(S) PARTICULIERE(S)"+clauses_paragraph_found.group("clauses_particulieres_paragraphe")
            return await try_safe_execute_async(logger,self.traitement_recursif_clauses_particuliers,text=txt,clauses=clauses)
        return clauses
    
    async def bpop_extract(self,text:str,found_tables, pret:Pret)-> Pret:
        """
        Data extraction based on BPOP template
        """
        # Extract the header 
        # Short header 
        pret.header_ref,pret.header_emprunteur, pret.header_responsable_suivi = await try_safe_execute_async(logger,self.extract_short_header,text=text)
        if (pret.header_ref=='') :
           # Pro  
            pret.header_emprunteur, pret.num_suivi,pret.header_offre, pret.header_num_etude,pret.header_responsable_suivi = await try_safe_execute_async(logger,self.extract_header_pro,text=text)
            if pret.num_suivi=="" :
                # Header Particulier
                pret.header_emprunteur, pret.num_suivi,pret.header_ref, pret.header_num_etude,pret.header_responsable_suivi = await try_safe_execute_async(logger,self.extract_header_particulier,text=text)
        if pret.num_suivi=="":
            # Pro or Particulier Extraction failed so try just simple extraction 
            # Get the follow up number 
            pret.num_suivi  = await try_safe_execute_async(logger,self.extract_num_suivi,text=text) 
        # Get date of the loan offer
        pret.date_emission_offre = await try_safe_execute_async(logger,self.extract_date_offre,text=text)          
        #Get the caution(s)
        pret.cautions = await try_safe_execute_async(logger,self.extract_cautions,text=text  )
        #Get the financial purpose  : List of ( Titre, Description , Adresse, Code Postal & Ville )
        pret.objets_financement = await try_safe_execute_async(logger, self.extract_objectives_data,text=text)
        # extract data of financial program from the tables found in pdf document 
        pret.programme_financier = await try_safe_execute_async(logger,self.extract_programme_financier,tables=found_tables)          
        # extract specifics data 
        pret.list_prets = await try_safe_execute_async(logger,self.extract_list_prets,tables=found_tables)
        pret.caracteristiques_prets = await try_safe_execute_async(logger,self.extract_caracteristiques_prets,text=text,tables=found_tables)
        #extract insurances
        pret.assurances = await try_safe_execute_async(logger,self.extract_assurances_new,text=text,tables=found_tables)
        pret.garanties = await try_safe_execute_async(logger,self.extract_garanties,text=text)
        pret.clauses_particulieres = await try_safe_execute_async(logger,self.extract_clauses_particulieres,text=text)
        pret.tableau_amortissement = await try_safe_execute_async(logger,self.extract_tableau_ammortissements,tables=found_tables)
        return pret
   
    async def ce_extract_header(self,text):
        """
        """
        search_header = re.compile(r"CREDITS (?P<header_offre>[a-z0-9 ]*(OFFRE DE CREDIT\(S\) IMMOBILIER\(S\)|CONTRAT DE PRÊT))(Offre)?.*Téléphone ?(?P<telephone>[0-9]+)?.*\n?Suivi par\n?(?P<suivi_par>.*)\n?Référence \n?(?P<reference>[a-z][0-9]{7}-[0-9]/[0-9]{7})",re.IGNORECASE| re.DOTALL)
        # the header is readable from the first page, so just take th 500 first characteres
        short_text = text[:500]

        header_responsable_suivi=None
        header_offre=None
        header_ref=None
        match = search_header.search( short_text)
        if match!=None  :
            header_offre = match.group("header_offre")
            header_responsable_suivi=match.group("suivi_par").replace("\n","")
            header_ref = match.group("reference")
        search_date_offre=re.compile(r"Date (de l'offre|d'édition) :? ?(?P<date_offre>[0-9]{1,2}/[0-9]{1,2}/[0-9]{4})",re.DOTALL|re.IGNORECASE)
        header_date_offre=None
        match = search_date_offre.search( short_text)
        if match!=None :
            header_date_offre = match.group("date_offre")
        return header_offre, header_responsable_suivi, header_ref, header_date_offre
   
    async def ce_extract_loan_object(self,text:str)->List[ObjetFinancement] :
        """
        Extract the loan objective from a CE template loan 
        Return the list of ObjetFinancements
        """
        objets_financement:List[ObjetFinancement]=[]
        search_loan_object = re.compile(r"objet (des|du) prêts?(?P<paragraphe_objet>.*?)Caractéristiques (des|du) prêts?",re.DOTALL|re.IGNORECASE)
        match = search_loan_object.search(text)
        if match !=None :
            paragraphe_objet=match.group("paragraphe_objet")
            clean_txt = ce_sanitize_initiales_ref(paragraphe_objet)
            b_usage_availlable:bool=False
            if clean_txt!=None and clean_txt!='':
                search_objet_avec_usage = re.compile(r"financer ?:?\n?(?P<objet>[^\n]*)\n(?P<adresse>.*)(- (?P<usage>.*))Coût",re.IGNORECASE|re.DOTALL)
                match_objet = search_objet_avec_usage.search(clean_txt)
                b_usage_availlable = match_objet!=None 
                if match_objet==None :
                    search_objet_sans_usage = re.compile(r"à financer ?:?\n?(?P<objet>[^\n]*)\n(?P<adresse>.*)Coût",re.DOTALL|re.IGNORECASE)
                    match_objet = search_objet_sans_usage.search(clean_txt)
                if match_objet!=None :
                    objet_financement=ObjetFinancement()
                    objet_financement.description=clean_txt
                    objet_financement.titre = match_objet.group("objet")
                    objet_financement.nature = match_objet.group("objet")
                    if b_usage_availlable:
                        objet_financement.usage = match_objet.group("usage")
                    adresse = match_objet.group("adresse")
                    doc = nlp(adresse)
                    for ent in doc.ents:
                        ## get the first entity from each LABEL
                        if ent.label_=="ADRESSE" and objet_financement.adresse=='':
                            objet_financement.adresse = ent.text
                        if ent.label_ =="VILLE" and objet_financement.ville=='':
                            objet_financement.ville = ent.text 
                        if ent.label_=="CODE_POSTAL" and objet_financement.code_postal=='' :
                            objet_financement.code_postal = ent.text 
                    objets_financement.append(objet_financement)
        return objets_financement

    async def ce_extract_cautions(self,text:str)->List[Emprunteur]:
        """
        Extract caution from text
        """
        search_caution = re.compile(r"caution\(s\)\n?(?P<caution>.*)ci-après dénommé\(e\)\(s\) \"La caution\"",re.DOTALL|re.IGNORECASE)
        match_caution = search_caution.search(text)
        cautions:List[Emprunteur]=[]
        if match_caution!=None:
            caution_paragraph = match_caution.group("caution")
            doc = nlp(caution_paragraph)
            current_caution:Emprunteur=None
            for ent in doc.ents:
                if ent.label_=="CIVILITE" :
                    if current_caution!=None : cautions.append(current_caution)
                    current_caution = Emprunteur()
                    current_caution.civilite=ent.text
                if ent.label_=="PERSONNE" : 
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.est_personne=True
                    current_caution.nom = ent.text
                if ent.label_=="DATE" or ent.label_=="DATE_NAISSANCE":
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.date_naissance=ent.text
                if ent.label_=="VILLE" :
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.ville = ent.text
                if ent.label_=="SITUATION_MARITALE" :
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.situation_maritale=ent.text
                if ent.label_=="ADRESSE" :
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.adresse=ent.text
                if ent.label_=="CODE_POSTAL" :
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.code_postal=ent.text
                if ent.label_=="METIER":
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.metier=ent.text
                if ent.label_=="ORG_RAISON_SOCIALE" : 
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.est_personne=False
                    current_caution.raison_sociale = ent.text
                if ent.label_=="ORG_STATUT" :
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.est_personne=False
                    current_caution.statut_organisation = ent.text
                if ent.label_=="ORG_IMMATRICULATION":
                    if current_caution==None : current_caution=Emprunteur()
                    current_caution.est_personne=False
                    current_caution.siret = ent.text
            if current_caution!=None : 
                cautions.append(current_caution)
        return cautions

    async def ce_extract_caracteristiques_prets_pret(self,loan_text:str,loan_table:lxfTable, loan_caract:CaracteristiquesPret)->CaracteristiquesPret:
        """
        extract loan characteristiques from the loan_text 
        """
        search_montant_total = re.compile(r"montant total du crédit : (?P<montant_total>.*)\n",re.IGNORECASE)
        match = search_montant_total.search(loan_text)
        if match!=None:
            loan_caract.montant = match.group("montant_total")
            # Montant total crédit
            search_montant_total_txt = re.compile(r"(?P<montant>[0-9 ,\.]+)")
            match = search_montant_total_txt.search(loan_caract.montant)
            if match!=None : 
                loan_caract.montant_total_du_emprunteurs.montant_total_credit.valeur=to_float(match.group("montant"))
            # TAEG
            search_taeg=re.compile(r"taeg ?: (?P<taeg>[0-9,]*) ?%",re.IGNORECASE)
            match = search_taeg.search(loan_text)
            if match!=None :
                loan_caract.taux.titre="TAEG"
                loan_caract.taux.taux_pourcentage=to_float(match.group("taeg"))
                loan_caract.taux.sigle="TAEG"
                loan_caract.taux.description="Taux annuel effectif global"
            # TEG
            search_teg=re.compile(r"teg ?: (?P<teg>[0-9,]*) ?%",re.IGNORECASE)
            match = search_teg.search(loan_text)
            if match!=None :
                loan_caract.taux.titre="TEG"
                loan_caract.taux.taux_pourcentage=to_float(match.group("teg"))
                loan_caract.taux.sigle="TEG"
                loan_caract.taux.description="Taux effectif global"            
            # Durée de la période
            search_duree_periode=re.compile(r"durée de période ?: *(?P<periode>[a-z]+)",re.IGNORECASE)
            match = search_duree_periode.search(loan_text)
            if match!=None :
                loan_caract.taux.base_periode=match.group("periode")
            # Taux de la période
            search_taux_periode = re.compile(r"taux de période ?: *(?P<taux>[0-9,]*) ?%",re.IGNORECASE)
            match = search_taux_periode.search(loan_text)
            if match !=None :
                loan_caract.taux.taux_periode=to_float(match.group("taux"))
            # Montant total des intérêts 
            search_montant_total_interets = re.compile(r"Montant total des intérêts : *(?P<montant>[0-9, ]+)EUR",re.IGNORECASE)
            match = search_montant_total_interets.search(loan_text)
            if match!=None:
                loan_caract.montant_total_du_emprunteurs.montant_total_interets.valeur=to_float(match.group("montant"))
            # Coût total crédit 
            search_cout_total_credit = re.compile(r"Coût total .*: *(?P<montant>[0-9 ,]+)EUR",re.IGNORECASE)
            match = search_cout_total_credit.search(loan_text)
            if match!=None :
                loan_caract.montant_total_du_emprunteurs.cout_total_credit.valeur=to_float(match.group("montant"))
            # Frais divers
            regex = r"(?P<nature>Frais de .*: ?(\(évaluation\)| *))(?P<frais>[0-9 ,]*)EUR"
            matches = re.finditer(regex, loan_text, re.IGNORECASE)
            for matchNum, match in enumerate(matches, start=1): 
                frais:Frais=Frais()
                frais.nature = match.group("nature").replace(":","")
                frais.montant.valeur = to_float(match.group("frais"))
                loan_caract.montant_total_du_emprunteurs.frais.append(frais)
            # Montant part assurance emprunteur obligatoire 
            search_montant_assurances = re.compile(r"Montant part assurance emprunteur *(?P<montant>[0-9, ]+)EUR",re.IGNORECASE)
            match = search_montant_assurances.search(loan_text)
            if match!=None:
                loan_caract.montant_total_du_emprunteurs.montant_total_assurance_obligatoire.valeur=to_float(match.group("montant"))
            # Docimiciliation 
            search_domiciliation_pret = re.compile(r"modalites de remboursement :.*?\n?-? ?(?P<domiciliation_libelle>.*?) ?: ?(?P<domicialiation_compte>.*?)\n",re.IGNORECASE|re.DOTALL)
            match = search_domiciliation_pret.search(loan_text)
            if match!=None:
                loan_caract.domiciliation.compte=match.group("domicialiation_compte").strip()
                loan_caract.domiciliation.debiteur= match.group("domiciliation_libelle")

        # Exploit les périodes d'amortissement
        
        if loan_table!=None and len(loan_table.rows)>0 :

            # find the 99,999 % pattern
            search_pourcentage= re.compile(r"(?P<pourcentage>[0-9]{1,3},[0-9]{1,3}) *%",re.DOTALL)
            search_assurance_accessoire = re.compile(r"(?P<assurance>[0-9]{1,3},[0-9]{1,3})(.*?)\n? ?(?P<accessoire>[0-9]{1,3},[0-9]{1,3})",re.IGNORECASE|re.DOTALL)
            search_montant = re.compile(r"(?P<montant>[0-9]{1,3},[0-9]{1,3})",re.DOTALL|re.IGNORECASE)
            last_line_index = len(loan_table.rows) -1
            for row_index,row in enumerate(loan_table.rows) :
                if row_index >1 and row_index<last_line_index:
                    try:
                        # skipping the headers and the last line
                        period:PeriodeAmortissement= PeriodeAmortissement()
                        lg=len(row.cells)
                        ## il faut se repérer par la fin car la première colonne peut être fusionnée avec la 2 ième colonne dans certains cas 
                        ## La premiere colonne peut parfois ne pas être prise en compte quand 2 lignes sont fusionnées:

                        ##     col 0=lg-8                  1=lg-7 2=lg-6    3=lg-5  4=lg-4  5=lg-3   6=lg-2 7=lg-1  
                        #  Amortissement     |  0,000 %  | 119 | mensuelle | 119 | 757.80  | *    | *     |
                        # Echéance constante |   fixe    |     |     05    |     |         | 0.00 | *     |                    
                        #                    | ----------|-----|-----------|-----|---------|------|-------|
                        #  0=lg-7    1=lg-6   2=lg-5   3=lg-2   4=lg-3   5=lg-2   6=lg-1 
                        #  0.000%   | 1   | mensuelle |   1   | 757.80  | *      |   *   |
                        #  Fixe     |     |     05    |       |  757.80 | *      |   *   |
                        #  ---------|-----|-----------|------ |---------|--------|------ |
                        #        
                        if lg>=8 :                        
                            period.type_echeance = row.cells[lg-8].value.strip()
                        else :
                            period.type_echeance =""
                        match=search_pourcentage.search(row.cells[lg-7].value.strip())
                        if match!=None :
                            period.taux_debiteur_pourcentage = to_float(match.group("pourcentage"))

                        period.duree_echeances = row.cells[lg-6].value.strip()
                        period.periodicite_echeance = row.cells[lg-5].value.strip()                    
                        montant_brut = row.cells[lg-3].value.strip()
                        match =search_montant.search(montant_brut)
                        if match!=None :
                            period.montant_echeances.append(MontantDivers(txt_montant="Montant en EUR",montant=Montant(valeur=to_float(match.group("montant")))))
                        else :
                            period.montant_echeances.append(MontantDivers(txt_montant=montant_brut))

                        match = search_assurance_accessoire.search(row.cells[lg-2].value.strip())
                        if match !=None :
                            period.assurance = Montant(valeur=to_float(match.group("assurance")))
                            period.accessoire = Montant(valeur=to_float(match.group("accessoire")))
                        
                        montant_total = row.cells[lg-1].value.strip()
                        match =search_montant.search(montant_total)
                        if match!=None :
                            period.montant_echeances.append(MontantDivers(txt_montant="Echéance Ass/Acc. Inclus (En EUR)",montant=Montant(valeur=to_float(match.group("montant")))))
                        else :
                            period.montant_echeances.append(MontantDivers(txt_montant=montant_total))                    
                        regex=r"[0-9]{1,3},[0-9]{1,3} *%"
                        period.type_taux_debiteur =  re.sub(regex, "", row.cells[lg-7].value.strip(), 1, re.IGNORECASE | re.DOTALL).strip()

                        loan_caract.periodes_amortissement.append(period)
                    except Exception as ex:
                        logger.exception(f"Exception pendant la recherche des périodes d'amortissement pour les prêts CAISSE D'EPARGNE pour la ligne {row_index} ")

        return loan_caract

    async def ce_extract_caracteristiques_prets(self,text:str,found_tables):
        """
        Extract all characteristiques loan for each loan
        """
        caracteristiques_prets:List[CaracteristiquesPret]=[]
        legacy_list_prets:List[CaracteristiquePret]=[]
        regex = r"Caractéristiques (du|des) prêts?(?P<prets>.*?)\n?ASSURANCES"
        matches = re.search(regex, text,  re.DOTALL)
        if matches!=None :
            paragraphe_prets = sanitize_bas_de_page_ce(matches.group("prets"))
            ## It can have multiple loans inside this paragraphe 
            regex = r"\n(?P<titre>.*) : Référence (?P<reference>[0-9a-z]+)\n"
            matches = re.finditer(regex, paragraphe_prets, re.IGNORECASE)
            sections=[]
            # find all loans an get their description 
            for index,match in enumerate(matches,start=1):
                sections.append(match.start())
                sections.append(match.end())
                current_caracteristiques_pret = CaracteristiquesPret()
                current_caracteristiques_pret.description=match.group("titre")
                current_caracteristiques_pret.numero_pret=match.group("reference")
                caracteristiques_prets.append(current_caracteristiques_pret)
            # Adding the last one with the end of paragraphe 
            # Header of loan 1 : Start1 End1
            # Header of loan 2 : Start2 End2
            # Header of loan 3 ! Start3 End3
            # Etc ...
            # therefore the text of each loan is located at :
            # Text Loan1 : End1 - Start2
            # Text Loan2 : End2 - Start3
            # Text Loan3 : End3 - Len(paragraphe_prets)
            # Adding the end of last loan
            sections.append(len(paragraphe_prets))
            # sections is an array = start1 end1 star2 end2 start3 end3 len_paragraphe_pret 
            # now sections contains all the start and end charactere of each loan 
            # lookup the loan tables 
            loan_table:lxfTable=lxfTable()
            loan_table_header=["Phases Type d’échéance","Taux débiteur Nature du taux","Durée (mois)","Echéance hors assurance et accessoires","Assurances Accessoires (En EUR)","Echéance Ass/Acc. Inclus (En EUR)"]      
            hdr_cptor=TextArrayComparator(loan_table_header,nlp=settings.nlp_with_vectors)
            # Retourne une liste de tables correspondante aux entêtes fournies
            loan_tables_found = search_table_by_text_array(hdr_cptor=hdr_cptor,tables=found_tables)
            # we want to iterate on tuples from sections array: 
            #                    Loantext1 = (section[1],sections[2]) 
            #                    loantext2 = (sections[3],sections[4]) 
            #                    loantext3 = (sections[5],sections[6]) 
            #                    etc ...
            loan_index=-1
            nb_tables_found= len(loan_tables_found)
            for index in range(1,len(sections),2) :
                start = sections[index]
                end = sections[index+1]
                ## we have the section start , end tag, let's extract all other required characteristiques
                loan_index+=1
                loan_txt=paragraphe_prets[start:end]
                if nb_tables_found>0 and loan_index< nb_tables_found :
                    # on  la  table touvée à l'index souhaité
                    loan_table = loan_tables_found[loan_index]
                else :
                    logger.error(f"Table caractéristiques du prêt {caracteristiques_prets[loan_index]} non trouvée")
                caracteristiques_prets[loan_index] = await try_safe_execute_async(logger,self.ce_extract_caracteristiques_prets_pret,loan_text=loan_txt,loan_table=loan_table,loan_caract=caracteristiques_prets[loan_index])
                loan:CaracteristiquePret=CaracteristiquePret()
                loan.nature = caracteristiques_prets[loan_index].description
                loan.montant.valeur = to_float(caracteristiques_prets[loan_index].montant.lower().replace("eur",""))
                loan.numero = caracteristiques_prets[loan_index].numero_pret
                ## lookup for the duration in row Durée total
                if loan_table!=None :
                    # the information is inline row[0]="Durée totale", Cell[2]
                    txt_comparator = TextComparator("Durée totale (hors préfinancement)", nlp=settings.nlp_with_vectors)
                    for row in loan_table.rows:
                        txt = row.cells[0].value
                        if txt_comparator.compare_to(txt)>0.8 :
                            # found the right line
                            loan.duree_mois=to_int(row.cells[2].value)

                legacy_list_prets.append(loan)
        

        return caracteristiques_prets, legacy_list_prets
    
    async def ce_extract_programme_financier(self,text:str)->ProgrammeFinancier:
        """
        Extraction du programme financier
        """
        prg:ProgrammeFinancier=ProgrammeFinancier()
        search_programme = re.compile(r"Coût total de l’opération ?:(?P<cout_operation>[0-9, ]*)EUR\n? ?Apport personnel ?:(?P<apport>[0-9, ]*)EUR\n? ?Crédit total demandé ?:(?P<cout_total>[0-9, ]*)EUR",re.IGNORECASE)
        # search only on first 5000 characters
        match = search_programme.search(text[:5000])
        if match !=None :

            # Crédit total demandé
            plan:ElementPlanFinancement=ElementPlanFinancement()
            plan.nature = "Crédit total demandé"
            plan.montant.valeur=to_float(match.group("cout_total")) 
            prg.plan_financement.append(plan)
            plan = ElementPlanFinancement()
            plan.nature="Apport personnel"
            plan.montant.valeur=to_float(match.group("apport"))
            prg.plan_financement.append(plan)
            plan = ElementPlanFinancement()
            plan.nature="Coût total de l'opération"
            plan.montant.valeur=to_float(match.group("cout_operation"))
            prg.plan_financement.append(plan)
            return prg
        return prg

    async def ce_extract_garanties(self,text,found_tables)->List[Warranty]:
        search_garanties = re.compile(r"GARANTIES(?P<garanties>.*?)CONDITIONS GENERALES", re.DOTALL)
        match_paragraphe_garanties= search_garanties.search(text)
        if match_paragraphe_garanties==None : return []
        match_paragraphe_garanties_text = match_paragraphe_garanties.group("garanties") #sanitize_text(match_paragraphe_garanties.group("garanties"))
        #logger.debug(f"Garanties paragraphe trouvé {match_paragraphe_garanties_text}")
        match_paragraphe_garanties_text = sanitize_garanties_text(match_paragraphe_garanties_text)
        doc_garanties=nlp(match_paragraphe_garanties_text)
        matches = matcher_garantie(doc_garanties)
        #logger.debug(f"Garanties matches {matches}")
        warranties:List[Warranty]=[] 
        for match in matches:
            if match[0]==garanties_key_matcherkey :
                # Garantie Financiere
                start = match[1]
                end = match[2]
                garantie_trouvee=str(doc_garanties[start:end])
                # dirty trick add a space before Hypo ... :( 
                # increasing NER results
                garantie_trouvee = garantie_trouvee.replace("Hypo"," Hypo")                 
                # NLP for the warranties found 
                dd = nlp(garantie_trouvee)
                dd_start = 0
                #logger.debug(f"Garantie trouvée:\n{garantie_trouvee}")
                previous_warranty=None
                # Spliting the warranties inside an array of warranty 
                for ent in dd.ents :

                    if ent.label_=="GARANTIE_FINANCIERE" :
                        dd_end = ent.start-1
                        warranty:Warranty=Warranty()
                        warranty.label=str(ent.text)                           
                        warranties.append(warranty)  
                        if previous_warranty!=None :
                            previous_warranty.text=sanitize_text(f"{previous_warranty.label} {str(dd[dd_start:dd_end])}" )
          
                        previous_warranty=warranty
                        dd_start =ent.end


                if previous_warranty!=None : 
                    previous_warranty.text = sanitize_text(f"{previous_warranty.label} {str(dd[dd_start:])}")
                    # looking for DUREE and DUREE_LIMITE ; we must work on sanitize text 
                    if previous_warranty.text!=None :
                        ddd = nlp(previous_warranty.text)
                        for ent in ddd.ents :
                            if ent.label_=="DUREE" :
                                duree, unite = extract_duree_from_text(ent.text)
                                if duree!="" :
                                    previous_warranty.duree= duree
                                    previous_warranty.duree_unite=unite
                                else :
                                    previous_warranty.duree=ent.text
                            if ent.label_=="DUREE_LIMITEE":
                                duree,unite = extract_duree_from_text(ent.text)
                                if duree!="" :
                                    previous_warranty.duree_limitee=duree
                                    previous_warranty.duree_limitee_unite = unite
                                else :
                                    previous_warranty.duree_limitee=ent.text
                                
                dd=None 
                # Display the array of warranties  
                ref_candidate_table_index=-1
                credits_candidate_table_index=-1
                for warranty in warranties :
                    warranty.text = preprocess_code_postal_09999(warranty.text)
                    doc_garantie = nlp(warranty.text)
                    for ent in doc_garantie.ents:
                        if ent.label_=="NUMERO" :
                            num=str(ent.text) 
                            warranty.numero_pret = sanitize_numero(num)
                        elif ent.label_ =="CADASTRE" :
                            warranty.ref_cadastrales = sanitize_ref_cadastrales(str(ent.text))
                            table_header_tofind=[ent.text]      
                            tac:TextArrayComparator=TextArrayComparator(table_header_tofind,nlp=settings.nlp_with_vectors)
                            tables_found, found_at_indexes = search_table_by_text_array_in_all_rows(hdr_cptor=tac,tables=found_tables,limit=1,threshold=0.6)
                            if tables_found!=None and found_at_indexes!=None and len(tables_found)>0 and len(found_at_indexes)>0:
                                # select the table and the index according to num_waranty
                                ref_candidate_table_index+=1
                                if ref_candidate_table_index<=len(found_at_indexes) :
                                    table_found=None 
                                    try :
                                        index=found_at_indexes[ref_candidate_table_index]
                                    except Exception as ex:
                                        logger.exception(ex)
                                        break
                                    # On prend la référence trouvée
                                    warranty.ref_cadastrales = sanitize_ref_cadastrales(tables_found[ref_candidate_table_index].rows[index].cells[0].value)
                                    numero_pret=tables_found[ref_candidate_table_index].rows[index+3].cells[0].value
                                    if numero_pret in warranty.text :
                                            # we've just found the right table since it contains the loan reference
                                            # cointained in the cell of Crédit in the current table t
                                            try :
                                                table_found=tables_found[ref_candidate_table_index]                                        
                                            except Exception as ex:
                                                logger.exception(ex)
                                                break
                                            row_index=index

                                if table_found!=None and row_index>-1 :
                                    # adresse is at line row_index+1
                                    row_idx=row_index+1
                                    adresse = table_found.rows[row_idx].cells[0].value
                                    warranty.text_adresse_immeuble_cadastre=adresse
                                    adresse_doc= nlp(adresse)
                                    for ent in adresse_doc.ents:                            
                                        if ent.label_=="ADRESSE" :
                                            warranty.adresse_immeuble_cadastre = ent.text
                                        elif ent.label_=="CODE_POSTAL":
                                            warranty.code_poste_immeuble_cadastre=ent.text
                                        elif ent.label_=="VILLE":
                                            warranty.ville_immeuble_cadatre =ent.text
                                    # Référence prêt et Quotité ou montant
                                    # the line below the cadastre we should be:
                                    # Crédit  | Quotité ou montant (1)
                                    row_idx+=1
                                    cell_credit = table_found.rows[row_idx].cells[0].value
                                    txt_cpr = TextArrayComparator("Crédit",nlp=settings.nlp_with_vectors)
                                    if txt_cpr.compare_to(cell_credit)>0.75 :
                                        # the line below " Crédit | Quotité ou Montant" line
                                        # contains the ref loan and the value in EUR or in %
                                        # Il faut se souvenir qu'on a trouvé une ligne credit dans un tableau
                                        # avec une référence cadastrale. Il ne faudra plus lire ce tableau
                                        # pour cela on doit incrémenter l'index credits_candidate_index de 1
                                        credits_candidate_table_index+=1                                        
                                        row_idx+=1
                                        warranty.numero_pret = table_found.rows[row_idx].cells[0].value
                                        warranty.hauteur = table_found.rows[row_idx].cells[1].value
                                        # Il peut y avoir plusieurs prêts pour une même garantie
                                        # dans ce cas on ajoute les valeurs trouvées séparées par une virgule
                                        lg = len(table_found.rows)
                                        for i in range(row_idx+1,lg) :
                                            warranty.numero_pret +=" ; "+ table_found.rows[i].cells[0].value
                                            warranty.hauteur +=" ; " + table_found.rows[i].cells[1].value                                             
                                        
                    # C'est une garantie indépendante de la Ref Cadastrale ; ie elle est vide 
                    if warranty.ref_cadastrales=="" or warranty.ref_cadastrales==None or warranty.hauteur =="0.0":
                        # Gérer Tableau uniquement avec Credit Quotité ou Montant
                        table_header_tofind = ["Crédit","Quotité ou Montant"]
                        tac:TextArrayComparator=TextArrayComparator(table_header_tofind,nlp=settings.nlp_with_vectors)
                        tables_found, found_at_indexes = search_table_by_text_array_in_all_rows(hdr_cptor=tac,tables=found_tables)
                        if tables_found !=None :
                            # Tables trouvées
                            credits_candidate_table_index+=1
                            try :
                                index=found_at_indexes[credits_candidate_table_index]+1
                                warranty.numero_pret=tables_found[credits_candidate_table_index].rows[index].cells[0].value
                                warranty.hauteur = tables_found[credits_candidate_table_index].rows[index].cells[1].value
                                # Il peut y avoir plusieurs prêts pour une même garantie
                                # dans ce cas on ajoute les valeurs trouvées séparées par une virgule                                
                                lg = len(tables_found[credits_candidate_table_index].rows)
                                for i in range (index+1,lg) :
                                    warranty.numero_pret += " ;" +tables_found[credits_candidate_table_index].rows[i].cells[0].value
                                    warranty.hauteur += " ; " +tables_found[credits_candidate_table_index].rows[i].cells[1].value                                    
                            except :
                                pass


                    matches_garantie = matcher_garantie(doc_garantie)
                    for match in matches_garantie:

                        if match[0]==garantie_hauteur_matcherkey:
                            # Extract Hauteur
                            for ent in doc_garantie.ents:

                                if ent.label_ =="MONTANT":
                                    warranty.hauteur=ent.text 
                                    break
                        elif match[0]==garantie_rang_matcherkey:
                            # Extract Rang
                            warranty.rang = str(doc_garantie[match[2]-1:match[2]])
                        elif match[0]==garantie_cout_approximatif_matcherkey:  
                            for ent in doc_garantie.ents:
                                if ent.label_ =="MONTANT" and ent.start==match[2]-1:
                                    warranty.cout_approximatif =ent.text 
                                    break                   
                
                        # Get Office Name and address
                        m = pattern_garantie_office_notaire.search(warranty.text)
                        # sanitize the text at this point since we won't need FF and CR information 
                        warranty.text = sanitize_text(warranty.text)
                        if not (m==None or m.groups()==None) :
                            warranty.office_notarial = m.group("office_notarial")
                            adr = m.group("adresse_office_notarial")
                            adr = adr.replace(',',', ')
                            doc = nlp(adr) 
                            for ent in doc.ents :
                                if ent.label_=="ADRESSE" :
                                    warranty.adresse_office_notarial = sanitize_address(ent.text)
                                elif ent.label_=="CODE_POSTAL":
                                    warranty.code_postal_office_notarial=ent.text
                                elif ent.label_=="VILLE":
                                    warranty.ville_office_notarial=ent.text
   

        return warranties        
 
    async def ce_extract_insurances(self,text,found_tables)->List[Assurance]:
        """
        Insurances extraction based on Caisse d'Epargne template
        """
        class CaptureTypeAssurance:
            """
            """
            type_assurance:str=""
            paragraphe_type_assurance:str=""
 
        class CaptureAssurancesPersonne :
            """
            Class for capturing text insurances for a PERSON
            """
            souscripteur:str=""
            paragraph_insurances_person:str=""
            types_assurance:List[CaptureTypeAssurance]=None
 
        ###########
        search_insurances = re.compile(r"\nASSURANCES\n(?P<insurances>.*?)\nGARANTIES\n",re.MULTILINE|re.DOTALL)
        match = search_insurances.search(sanitize_bas_de_page_ce(text))
        insurances:List[Assurance]=[]
        ap:List[CaptureAssurancesPersonne]=[]
        if match!=None :
            # Get insurances paragraph
            insurances_paragraph = match.group("insurances")
            doc = nlp(insurances_paragraph)
            # Step 1 : Capture all Souscripteurs and paragraph's insurance of each souscripteur 
            capture_assurance_person:CaptureAssurancesPersonne=None
            current_insurance_paragraphe_text=""
            current_insurance_paragraphe_start=-1
            current_insurance_paragraphe_end  =-1
            for ent in doc.ents:
                if ent.label_=="PERSONNE" : 
                    # check if there is a '-' before this entity
                    range = 15
                    text_before_PERSONNE = insurances_paragraph[max(ent.start_char-range,0):ent.start_char]
                    if '-' in text_before_PERSONNE :
                        # that's ok, this a new PERSONNE
                        # check if there was a previous PERSONNE found
                        if current_insurance_paragraphe_start!=-1 and current_insurance_paragraphe_end==-1 and capture_assurance_person!=None:
                            ## There was a previous PERSONNE and a current insurance
                            # capture the insurance paragraphe for this previous PERSONNE
                            current_insurance_paragraphe_end=ent.start_char
                            current_insurance_paragraphe_text = insurances_paragraph[current_insurance_paragraphe_start:current_insurance_paragraphe_end]
                            ## set this text in description temporaly 
                            capture_assurance_person.paragraph_insurances_person = current_insurance_paragraphe_text
                            # add it to the lis
                            ap.append(capture_assurance_person)
                            capture_assurance_person=None

                        if capture_assurance_person==None :
                            # Create a new capture
                            capture_assurance_person=CaptureAssurancesPersonne()
                        capture_assurance_person.souscripteur = ent.text
                        current_insurance_paragraphe_start = ent.start_char
                        current_insurance_paragraphe_end=-1 
                        current_insurance_paragraphe_text=""
            doc=None
            # check if there was a previous PERSONNE found
            if current_insurance_paragraphe_start!=-1 and current_insurance_paragraphe_end==-1 and capture_assurance_person!=None:
                ## There was a previous PERSONNE and a current insurance
                # capture the insurance paragraphe for this previous PERSONNE
                current_insurance_paragraphe_end=ent.end_char
                current_insurance_paragraphe_text = insurances_paragraph[current_insurance_paragraphe_start:]
                ## set this text in description temporaly 
                capture_assurance_person.paragraph_insurances_person = current_insurance_paragraphe_text
                # add it to the lis
                ap.append(capture_assurance_person)
                capture_assurance_person=None
            # Step 2 : Grab details of each insurance 
            for index ,capture_assurance_person in enumerate(ap) :
                # Step 2.1 : Grab all garanties and type 
                current_insurance_paragraphe_text = capture_assurance_person.paragraph_insurances_person
                doc = nlp(current_insurance_paragraphe_text)
                start=-1
                end=-1
                current_capture_type_assurance:CaptureTypeAssurance=None
                for ent in doc.ents:
                    if ent.label_=="TYPE_ASSURANCE" :
                        if current_capture_type_assurance == None :
                            current_capture_type_assurance=CaptureTypeAssurance()
                        else :
                            # this is a new insurance type, add the previous to list and create a new one 
                            end=ent.start_char
                            current_capture_type_assurance.paragraphe_type_assurance = current_insurance_paragraphe_text[start:end]
                            if capture_assurance_person.types_assurance==None :
                                capture_assurance_person.types_assurance=[]                           
                            capture_assurance_person.types_assurance.append(current_capture_type_assurance)
                            current_capture_type_assurance=CaptureTypeAssurance()
                            end=-1
                        # update the new insurance type 
                        current_capture_type_assurance.type_assurance = ent.text                                              
                        start=ent.end_char
                end=max(end,len(current_insurance_paragraphe_text))
                if current_capture_type_assurance !=None and start!=-1:
                    if capture_assurance_person.types_assurance==None :
                        capture_assurance_person.types_assurance=[]
 
                    current_capture_type_assurance.paragraphe_type_assurance=current_insurance_paragraphe_text[start:end]
                    capture_assurance_person.types_assurance.append(current_capture_type_assurance)
                doc=None
            # Step 2.2 : Get Tables  Pret assuré | Capitaux assurés | Montant de la prime | 
            header_to_find =["Prêt(s) assuré(s)","Capitaux assurés","Montant de la prime", "Coût de l’assurance","Dont coût d’assurance obligatoire"]
            loan_insurance_type_tables:List[lxfTable]=[]
            hdr_cptor=TextArrayComparator(header_to_find,nlp=settings.nlp_with_vectors)
            # Retourne une liste de tables correspondante aux entêtes fournies
            loan_insurance_type_tables = search_table_by_text_array(hdr_cptor=hdr_cptor,tables=found_tables)        
            nb_types_assurance=0
            # Step 2.3 : Get Assureur, ref et quotité
            for  capture_assurance_person in ap:                
                for capture_type_assurance in capture_assurance_person.types_assurance :
                    nb_types_assurance+=1
                    insurance:Assurance=Assurance()
                    insurance.souscripteur = capture_assurance_person.souscripteur
                    type_assurance_paragraph_text = capture_type_assurance.paragraphe_type_assurance
                    insurance.description = sanitize_bas_de_page_ce(f"{capture_type_assurance.type_assurance.strip()}:\n{capture_type_assurance.paragraphe_type_assurance.strip()}")
                    # Step 2.3.1: Get all garanties
                    doc = nlp(type_assurance_paragraph_text)
                    for ent in doc.ents:
                        if ent.label_=="GARANTIE_ASSURANCE" :
                            if insurance.garanties=="" or insurance.garanties==None :
                                insurance.garanties=ent.text
                            else :
                                insurance.garanties += f", {ent.text}"
                    doc=None
                    if insurance.garanties=="" or insurance.garanties==None :
                        insurance.garanties=capture_type_assurance.type_assurance
                    # Step 2.3.2: Search assureur, quotité et référence 
                    has_reference=True
                    search_additionnal_info = re.compile(r"Compagnie.*?:(?P<assureur>.*?)Référence.*?:(?P<reference>.*?)Quotité.*?:(?P<quotite>.*?)Garanties",re.IGNORECASE|re.DOTALL)
                    match = search_additionnal_info.search(type_assurance_paragraph_text)
                    if match==None :
                        # Sometimes there is no reference 
                        search_additionnal_info = re.compile(r"Compagnie.*?:(?P<assureur>.*?)Quotité.*?:(?P<quotite>.*?)Garanties",re.IGNORECASE|re.DOTALL)
                        match = search_additionnal_info.search(type_assurance_paragraph_text)
                        has_reference=False
                    if match!=None : 
                        insurance.assureur = match.group("assureur").replace("\n","")
                        if has_reference :
                            insurance.reference = match.group("reference").replace("\n","")
                        insurance.quotite_pret_assure = match.group("quotite").replace("\n","")
                    # step 2.3.3: Explore the table:
                    #  Pret assuré | Capitaux assurés | Montant de la prime |
                    # there is 1 table for each type assurance
                    if loan_insurance_type_tables!=None and len(loan_insurance_type_tables)>=nb_types_assurance :
                        insurance_type_table = loan_insurance_type_tables[nb_types_assurance-1]
                        if insurance_type_table !=None :
                            insurance.tableau_prets = insurance_type_table                    
                    insurances.append(insurance)
        return insurances

    async def ce_extract(self,text:str, found_tables, pret:Pret)-> Pret :
        """
        Data extraction based on Caisse d'Epargne template
        """
        logger.warning("Caisse d'Epargne extraction Not completly implemented")
        # Get Header information
        header_offre, header_responsable_suivi , header_ref, header_date_offre = await try_safe_execute_async(logger,self.ce_extract_header,text=text)
        if header_offre!=None : pret.header_offre=header_offre
        if header_responsable_suivi!=None : pret.header_responsable_suivi=header_responsable_suivi
        if header_ref!=None : pret.header_ref=header_ref
        if header_date_offre!=None : pret.date_emission_offre=header_date_offre
        # Get CAUTION 
        pret.cautions = await try_safe_execute_async(logger,self.ce_extract_cautions,text=text)
        # Get Programme financier
        pret.programme_financier = await try_safe_execute_async(logger,self.ce_extract_programme_financier,text=text)
        # Get Objet financement
        pret.objets_financement = await try_safe_execute_async(logger, self.ce_extract_loan_object,text=text)
        # Get Loans characteristiques
        pret.caracteristiques_prets, pret.list_prets = await try_safe_execute_async(logger,self.ce_extract_caracteristiques_prets,text=text, found_tables=found_tables) 
        # Get Waranties
        pret.garanties = await try_safe_execute_async(logger,self.ce_extract_garanties,text=text,found_tables=found_tables)
        # Get Insurances
        pret.assurances = await try_safe_execute_async(logger, self.ce_extract_insurances,text=text, found_tables=found_tables)
        return pret

    async def extract_data(self) ->Pret :
        """
        Extract all data about the loan provide as PDF file name in the Ctor
        return : Pret object
        """
        
        pret:Pret=Pret()
        found_tables=List[lxfTable]
        text,found_tables = await try_safe_execute_async(logger,get_text_and_tables_from_pdf,filename=self.filename)
        if text == None : return None   

        # Get the data for 'Preteur'
        pret.preteur = await try_safe_execute_async(logger,self.extract_preteur,text=text)            

        #Get the data for the list of 'Emprunteur'   
        pret.emprunteurs= await  try_safe_execute_async(logger,self.extract_emprunteurs,text=text)    

        if "epargne" in pret.preteur.raison_sociale.lower() or "caisse" in pret.preteur.raison_sociale.lower() :
            return await self.ce_extract(text,found_tables=found_tables,pret=pret) 
        else :
            return await self.bpop_extract(text, found_tables=found_tables,pret=pret)
        
