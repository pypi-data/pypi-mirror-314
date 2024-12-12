import spacy
from spacy.lang.fr.stop_words import STOP_WORDS
from string import punctuation
import logging
from lxf.settings import SET_LOGGING_LEVEL

#logger
logger = logging.getLogger('Text Comparator')
fh = logging.FileHandler('./logs/text_comparator.log')
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)

chiffres ={"0","1","2","3","4","5","6","7","8","9"}
STOP_WORDS.update(chiffres)
symbols={"€","£","|","§","*"}
STOP_WORDS.update(symbols)
punctuations ={punct for punct in punctuation}
STOP_WORDS.update(punctuations)
EMPTY_STR="empty"
JOKER_STR="***"


class TextComparator :
    """
    Compare the internal text to text provide as parameter
                Comparation uses vectorization of token not in stop_word(spacy) and similarity beetwen text to be compared
    """
    def __init__(self,text:str,nlp=None):
        if nlp == None:
            #Lazzy loading
            logger.info("loading nlp")
            self.nlp_test=spacy.load("fr_core_news_lg")
        else : 
            self.nlp_test = nlp        
        self.internal_text=self.sanitize_text_and_clean_stop_words(text)
        # since we cannot compare by cosimilarity an empty string (=null vector), we decide to assign EMPTY_STR as empty string
        if self.internal_text=="" :            
            self.internal_text=EMPTY_STR
        self.internal_doc = self.nlp_test(self.internal_text)
        
    def sanitize_text_and_clean_stop_words(self,text):
        """
        Sanitize the text and retains only token not in STOP_WORDS
        """
        temp_text= self.sanitize_text(text.lower()) 
        retained_text=[word for word in temp_text.split() if word not in STOP_WORDS]
        return  " ".join(retained_text)      
        
    def get_nlp(self) :
        return self.nlp_test
    
    def get_text(self) :
        return self.internal_text 
                                     
    def sanitize_text(self,text:str)->str :
        temp_text=""
        last_char=" "
        # remove extra space
        text=text.replace('–','-').replace('’','\'').replace("\n"," ").strip()
        for char in text:
            if char==" ":
                if not last_char== " ":
                    temp_text+=char
                last_char=char
            else:
                last_char=char
                temp_text+=char
        return temp_text 
    
    def compare_to(self, text:str)->float :
        """
        Compare the internal text to text provide as parameter
            Comparation uses vectorization of token not in stop_word(spacy) and similarity beetwen text to be compared
        return : float value beetwen in -1 and 1 ; 100% means equal 
        """
        text_to_compare = self.sanitize_text_and_clean_stop_words(text)
        if text_to_compare==None :
            return 0.0 
        # since we cannot compare by cosimilarity an empty string (=null vector), we decide to assign EMPTY_STR as empty string
        if text_to_compare=="":
            text_to_compare=EMPTY_STR
        # if internal text is JOKER_STR so return 1 since JOKER replace any char
        elif self.internal_text==JOKER_STR :
            return 1.0
        doc_to_compare = self.nlp_test(text_to_compare)
        if doc_to_compare.has_vector :
            #logger.debug(f"Comparing  {text_to_compare} <= ? => {self.internal_text} ")
            result= self.internal_doc.similarity(doc_to_compare)
            if text_to_compare.startswith(self.internal_text) :
                # si le text à comparer commence par le text interne alors on retourne la valeur max entre 0.8 
                # et le résult du calcul de la cosimilarité
                return max(result,0.8)
            return result
        else :
            return 0.0 

class TextArrayComparator:
    """ 
    Compare array fo text using vectorization and cosimilarity 
    """
    def __init__(self,texts_array,nlp) :
        self.internal_docs=[ TextComparator(text,nlp=nlp) for text in texts_array]        
    
    def compare_to(self, texts_array,cell_limit=-1)->float :
        """
        cell_limit = -1 compare all cells
        otherwise only the first cell_limit cells 
        """
        if not len(texts_array) == len(self.internal_docs) :
            #logger.debug(f"empty texts array found")
            return 0.0
        sum=0.0
        if cell_limit==-1 :
            for i,cptor in enumerate(self.internal_docs) :
                sum+=cptor.compare_to(texts_array[i])
            lg=float(len(self.internal_docs))
        else:
            for i,cptor in enumerate(self.internal_docs[:cell_limit]) :
                sum+=cptor.compare_to(texts_array[i])
            lg=float(cell_limit)
        #logger.debug(f"similarity={sum}/{lg}={sum/lg}")
        return sum/lg