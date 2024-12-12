import logging
import asyncio
import os
import sys



import lxf.settings as settings
settings.SET_LOGGING_LEVEL=logging.DEBUG
settings.enable_tqdm=False

from lxf.domain.loan import Pret
from lxf.extractors.finance import odp_extractor
from lxf.extractors.finance import iban_extractor

from lxf.services.try_safe import  try_safe_execute_async



###################################################################

logger = logging.getLogger('test_finance')
fh = logging.FileHandler('./logs/test_finance.log')
fh.setLevel(settings.SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(settings.SET_LOGGING_LEVEL)
logger.addHandler(fh)
#################################################################

async def do_test_odp(file_path:str)->Pret:
    result = await try_safe_execute_async(logger,odp_extractor.extract_data,file_path=file_path)
    return result
    
async def do_test_iban(file_path:str)->str :
    """
    """
    result = await try_safe_execute_async(logger,iban_extractor.extract_data,file_path=file_path)
    return result

if __name__ == "__main__":
    sys.stdout.reconfigure(line_buffering=True) 
    pdf_path = "data/ODP.pdf"
    # pret:Pret=  asyncio.run(do_test_odp(file_path=pdf_path))
    # if pret!=None:
    #     print(pret.emprunteurs)
    iban_pdf="data/rib pm.pdf"
    txt = asyncio.run(do_test_iban(file_path=iban_pdf))
    print(txt)
    
