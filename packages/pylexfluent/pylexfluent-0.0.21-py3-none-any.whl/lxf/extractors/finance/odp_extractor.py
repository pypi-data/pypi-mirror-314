
import logging 


from lxf.extractors.finance.loans.loan_extractor import LoanDataExtractor
from lxf.services.try_safe import try_safe_execute_async

from lxf.settings import SET_LOGGING_LEVEL

###################################################################

logger = logging.getLogger('odp')
fh = logging.FileHandler('./logs/odp.log')
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)
#################################################################

async def extract_data(file_path:str)->str|None:
    """
    Extrait les données d'une offre de prêt 
    """
    logger.debug(f"Demande extraction de données pour {file_path}")
    loan:LoanDataExtractor= LoanDataExtractor(file_path)
    result= await try_safe_execute_async(logger,loan.extract_data)
    logger.debug(f"Extraction de données différent de None ? {result!=None}")
    return result
