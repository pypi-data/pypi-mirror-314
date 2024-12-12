#{'class_name':class_predicted,'accuracy':accuracy,'predictions':predictions}
from pydantic import BaseModel,Field
from typing import List
class prediction(BaseModel):
	classification:str=Field(default="")
	accuracy:float=Field(default=0.0)	

class InferenceResult(BaseModel):
	best_classification:str=Field(default="Sorry no classification found")
	best_accuracy:float=Field(default=0.0)
	predictions:List[prediction]=Field(default=[])

class PageInferenceResult(BaseModel):
    page_number:int =Field(default=0)
    page_result:InferenceResult=InferenceResult()
    
class DocumentInferenceResults(BaseModel):
    document_filename:str=Field("pas de nom")
    pages_result:List[PageInferenceResult]=[]