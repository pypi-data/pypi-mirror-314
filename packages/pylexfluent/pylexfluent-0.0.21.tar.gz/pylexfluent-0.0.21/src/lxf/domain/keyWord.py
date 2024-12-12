from pydantic import BaseModel,Field

class KeyWord(BaseModel):
	word:str=Field(default="")
	freq:float=Field(default=0.0)
	class Config:        
		json_schema_extra = {
			"example": {
				"word":'facturation',
				"freq":0.35
			}
		}