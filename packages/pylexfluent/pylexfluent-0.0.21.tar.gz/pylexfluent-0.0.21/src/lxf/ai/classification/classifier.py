



import datetime
import logging
from lxf.ai.classification.multiclass.jupiter_model import MulticlassClassificationJupiterModel
from lxf.domain.keyWord import KeyWord
from lxf.domain.keyswordsandphrases import KeysWordsAndPhrases, KeysWordsPhrases
from lxf.domain.predictions import Predictions
from lxf.services.pdf import get_text_and_tables_from_pdf
from lxf.services.try_safe import try_safe_execute, try_safe_execute_async

from lxf.settings import SET_LOGGING_LEVEL

###################################################################

logger = logging.getLogger('test classifier')
fh = logging.FileHandler('./logs/test_classifier.log')
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)
#################################################################

async def get_classification(file_name) -> Predictions :
    """
    """
    result,_ = await try_safe_execute_async(logger,get_text_and_tables_from_pdf, filename=file_name,extract_tables=False)
    if result!=None :
        keysWordsPhrasesHelper:KeysWordsAndPhrases = KeysWordsAndPhrases(result)
        freq_mots= keysWordsPhrasesHelper.get_key_words(isSorted=True, threshold=0.1)
        # convert data to KeysWordsPhrases object 
        result:KeysWordsPhrases = KeysWordsPhrases()
        for mot in freq_mots:
            kword:KeyWord = KeyWord()
            kword.word=mot
            #logger.debug(f"Word: {mot}")
            kword.freq=freq_mots[mot]
            #logger.debug(f"Freq Word: {kword.freq}")
            result.keysWords.append(kword)
        if len(result.keysWords) > 0 :
            jupiter:MulticlassClassificationJupiterModel=MulticlassClassificationJupiterModel()
            pred:Predictions = await  try_safe_execute_async(logger,jupiter.inference,data=result,model_name="jupiter")
            return pred

        else :
            return None
            