import  unicodedata
import logging
from lxf.settings import SET_LOGGING_LEVEL

#logger
logger = logging.getLogger('Text Utilities')
fh = logging.FileHandler('./logs/text_utils.log')
from lxf.settings import SET_LOGGING_LEVEL
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)

def strip_accents(text):
    """
    Strip accents from input String.

    :param text: The input string.
    :type text: String.

    :returns: The processed String.
    :rtype: String.
    """
    # try:
    #     text = unicode(text, 'utf-8')
    # except (TypeError, NameError): # unicode is a default on python 3 
    #     pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    return str(text)

accents=['é','è','ù','ô','û','ï','ë','à']
def has_accents(text:str)->bool:
    return any([w in accents for w in text])

def to_lower_without_accent(text:str)->str :
    text=text.lower()
    if has_accents(text) : 
        return strip_accents(text)
    return text