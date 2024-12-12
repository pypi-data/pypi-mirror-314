from pydantic import BaseModel,Field

class KeyPhrase(BaseModel):
	phrase:str=Field(default="")
	score:float=Field(default=0.0)
	class Config:   
		arbitrary_types_allowed = True     
		json_schema_extra = {
			"example": {
				"phrase":'Achat immobilier et travaux Maison individuelle 3, chemin barenjoux 71960 MILLY LAMARTINE',
				"score":0.65
			}
		}