


import logging
from lxf.domain.keyWord import KeyWord
from lxf.services.measure_time import measure_time_async
from lxf.domain.keyswordsandphrases import KeysWordsAndPhrases, KeysWordsPhrases

from lxf.settings import SET_LOGGING_LEVEL

#logger
logger = logging.getLogger('Keys words')
fh = logging.FileHandler('./logs/keysword.log')
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)

@measure_time_async  
async def get_keys_words(self,text:str,isSorted:bool=False,threshold:float=0.1)->KeysWordsPhrases:
    """
    Get the keys words and the keys phrases from a free text
    """
    keysWordsPhrasesHelper:KeysWordsAndPhrases = KeysWordsAndPhrases(text)
    logger.debug(f"Threshold {threshold}")
    freq_mots= keysWordsPhrasesHelper.get_key_words(isSorted=isSorted, threshold=threshold)
    # convert data to KeysWordsPhrases object 
    result:KeysWordsPhrases = KeysWordsPhrases()
    for mot in freq_mots:
        kword:KeyWord = KeyWord()
        kword.word=mot
        #logger.debug(f"Word: {mot}")
        kword.freq=freq_mots[mot]
        #logger.debug(f"Freq Word: {kword.freq}")
        result.keysWords.append(kword)
    return result   