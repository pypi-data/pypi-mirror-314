

import logging
import re
from typing import List

from tqdm import tqdm
from lxf.settings import enable_tqdm
from lxf.domain.tables import lxfCell, lxfRow, lxfTable
from lxf.settings import SET_LOGGING_LEVEL

#logger
logger = logging.getLogger('PDF services')
fh = logging.FileHandler('./logs/pdf_services.log')
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)

import pdfplumber


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

def prune_text(text):

    def replace_cid(match):
        ascii_num = int(match.group(1))
        try:
            return chr(ascii_num)
        except:
            return ''  # In case of conversion failure, return empty string

    # Regular expression to find all (cid:x) patterns
    cid_pattern = re.compile(r'\(cid:(\d+)\)')
    pruned_text = re.sub(cid_pattern, replace_cid, text)
    return pruned_text

async def get_text_from_pdf(filename:str) :
    """
    Extrait le texte contenu dans un pdf
    filename: le nom du fichier pdf
    """
    with pdfplumber.open(filename,laparams={"detect_vertical": False}) as pdf:
        text =''
        for page in pdf.pages :
            words = page.extract_words(x_tolerance=1,y_tolerance=1, use_text_flow=True, line_dir="ltr")       
            if not words==None :
                for word in words:
                    text = text + " "+word['text']          
        pdf.close()
        return sanitize_text(text)

async def get_text_and_tables_from_pdf(filename:str,extract_tables:bool=True) :
    """
    Extrait tout le text et toutes les tables contenues dans un pdf
    filename: le nom du fichier pdf
    return: text , lxfPages 
    """
    DEFAULT_SNAP_TOLERANCE = 3
    DEFAULT_JOIN_TOLERANCE = 3
    DEFAULT_MIN_WORDS_VERTICAL = 3
    DEFAULT_MIN_WORDS_HORIZONTAL = 1
    DEFAULT_TABLE_SETTINGS = {
    "vertical_strategy": "lines",
    "horizontal_strategy": "lines",
    "explicit_vertical_lines": [],
    "explicit_horizontal_lines": [],
    "snap_tolerance": DEFAULT_SNAP_TOLERANCE,
    "join_tolerance": DEFAULT_JOIN_TOLERANCE,
    "edge_min_length": 3,
    "min_words_vertical": DEFAULT_MIN_WORDS_VERTICAL,
    "min_words_horizontal": DEFAULT_MIN_WORDS_HORIZONTAL,
    #"keep_blank_chars": False,
    "text_tolerance": 3,
    "text_x_tolerance": 3,
    "text_y_tolerance": 3,
    "intersection_tolerance": 3,
    "intersection_x_tolerance": 3,
    "intersection_y_tolerance": 3,
    }
    settings = dict(DEFAULT_TABLE_SETTINGS)
    settings["text_tolerance"]=1
    settings["text_x_tolerance"]=1
    settings["text_y_tolerance"]=1
 

    with pdfplumber.open(filename) as pdf:
        found_tables:List[lxfTable]=[]
        index_table=0
        text=""
        unicode_dash=re.compile(r'\xad')
        for page_number, page in tqdm(enumerate(pdf.pages,start=1),desc=f"{filename}: Lecture page en cours ",disable= not enable_tqdm):
            #Get Text
            t = page.extract_text(x_tolerance=1,y_tolerance=1)       
            if not t==None :
                if 'cid' in t :
                    t = prune_text(t)
                # Gérer les cas où les tirets sont en unicode \xad 
                if '\xad' in t :
                    t=re.sub(unicode_dash,'-',t)                    
                text = text + t   
            #Get Tables within the current page
            tables=None
            if extract_tables :
                tables = page.extract_tables(settings)
                if not tables==None and not len(tables)==0:  
                    for table in tables:
                        index_table+=1                    
                        lxf_table=lxfTable()
                        lxf_table.page_number = page_number
                        #lxf_table.number = index_table
                        for row in table :
                            if not row== None:
                                lxf_row=lxfRow()
                                for cell in row :
                                    if not (cell == None or cell==" "):
                                        lxf_cell=lxfCell()
                                        if 'cid' in cell :
                                            cell = prune_text(cell)
                                        lxf_cell.value =sanitize_text(cell).replace("\n"," ")
                                        lxf_row.cells.append(lxf_cell)                                        
                                lxf_table.rows.append(lxf_row)                                                         
                        found_tables.append(lxf_table)
        pdf.close()
        return text, found_tables