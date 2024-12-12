
import logging
import os
from lxf.settings import SET_LOGGING_LEVEL

#logger
logger = logging.getLogger('OCR PDF ')
fh = logging.FileHandler('ocr_pdf.log')
from lxf.settings import SET_LOGGING_LEVEL
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)


import ocrmypdf

from lxf.services.measure_time import measure_time


#ocrmypdf.Verbosity(0) # Suppress most messages
#ocrmypdf.configure_logging(verbosity=0, progress_bar_friendly= False)

class OcrPdf :
    """
    Ocerize a PDF File
    """

    def do_ocr(self,input_pdf, output_pdf):
        # if (maxPagesLimit>0) :
            
        ocr_result = ocrmypdf.ocr(input_pdf,
                          output_pdf,
                          output_type='pdf',
                          skip_text=True,
                          force_ocr=False,
                          keep_temporary_files=False,
                          clean=True,language="fra+eng",
                          progress_bar=False,
                          deskew=False,
                          author="Lexia by Lexfluent",
                          keywords="OCR")
        return ocr_result
    


    def do_ocr_directory(self,directory_source:str,directory_dest:str):
        for root, dirs, files in os.walk(directory_source):
            if files!=[] :
                category='_'.join(root.split('/')[-3:]).replace(' ','-')
                logger.debug(f"Category: {category}")
                for f in files :  
                    if '.pdf' in f:   
                        input_pdf = root+'/'+f
                        output_ocred_pdf = directory_dest+"/"+category+'_'+f 
                        # if file exists in ocr directory skip it 
                        if os.path.exists(output_ocred_pdf) == False : 
                            result = self.do_ocr(input_pdf,output_ocred_pdf)
                            logger.debug(f"OCR Result for {f}: {result} ")