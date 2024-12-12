
import logging
from typing import List
from lxf.settings import SET_LOGGING_LEVEL


from pydantic import BaseModel,Field

from lxf.utilities.text_comparator import TextArrayComparator




logger = logging.getLogger('Tables utilities')
fh = logging.FileHandler('./logs/tables.log')
fh.setLevel(SET_LOGGING_LEVEL)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
logger.setLevel(SET_LOGGING_LEVEL)
logger.addHandler(fh)


class lxfCell(BaseModel):
    value:str=Field(default="")
    class Config:
        arbitrary_types_allowed = True

        
class lxfRow(BaseModel):
    cells:List[lxfCell]=[]
    class Config:
        arbitrary_types_allowed = True



class lxfTable(BaseModel):
    rows:List[lxfRow]=[]
    has_header:bool=Field(default=True)
    page_number:int=Field(default=0)
    class Config:
        arbitrary_types_allowed = True



class lxfTables(BaseModel):
    tables:List[lxfTable]=[]
    class Config:
        arbitrary_types_allowed = True

        
class lxfPage(BaseModel) :
    tables:List[lxfTables]=[]
    class Config:
        arbitrary_types_allowed = True

    
class lxfPages(BaseModel):
    pages:List[lxfPage]=[]
    class Config:
        arbitrary_types_allowed = True


def dump_table_by_index(num_table:int,tables=[]):
    if tables==[] : return
    t:lxfTable= tables[num_table-1]
    dump_table(t)

def dump_table(table:lxfTable):

    for r in table.rows:
        ligne=""
        logger.debug(f"r = {r}")
        for c in r.cells:
            ligne = ligne +"\t" + c.value
        logger.debug(ligne)
    logger.debug(f"=== Fin Table")

def search_table_by_text_array(hdr_cptor:TextArrayComparator,tables=[],limit=-1)->List[lxfTable]:
    found_tables = []
    if not hdr_cptor == None:
        ##logger.debug(f"Cell limit: {limit}")
        for t in tables : 
            #check first row of each table
            first_row_as_array = [c.value for c in t.rows[0].cells]
            if hdr_cptor.compare_to(first_row_as_array,cell_limit=limit) >= 0.70 :
                #if matchs append the table
                found_tables.append(t)
    return found_tables

def search_table_by_text_array_in_all_rows(hdr_cptor:TextArrayComparator,tables=[],limit=-1, threshold:float=0.7):
    """
    Seach in all rows of each tables
    Return tables with a row matching and the row index (0 base index)
    """
    found_tables = []
    found_indexes=[]
    if not hdr_cptor == None:
        ##logger.debug(f"Cell limit: {limit}")
        for t in tables : 
            for index,row in enumerate(t.rows) :
                #check row of each table
                row_as_array = [c.value for c in row.cells]
                if hdr_cptor.compare_to(row_as_array,cell_limit=limit) >= threshold :
                    #if matchs return found table and row index
                    found=True
                    found_tables.append(t)
                    found_indexes.append(index)
                    # exit rows loop
                    break            
    return found_tables, found_indexes
