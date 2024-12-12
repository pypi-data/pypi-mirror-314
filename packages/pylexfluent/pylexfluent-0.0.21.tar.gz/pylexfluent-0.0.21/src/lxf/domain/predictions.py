from typing import List, Optional

from pydantic import  BaseModel, Field


class Prediction(BaseModel) :
    Name:str=Field(default="")
    Confidence:float=Field(default=0.0)

class Predictions(BaseModel) :
  
    EntityId:str=Field(default="")
    Name:str=Field(default="")
    ModelName:str=Field(default="")
    PredictedAt:Optional[str]=Field(default="")
    BestPrediction:str=Field(default="")
    BestPredictionConfidence:float=Field(default=0.0)
    Results:List[Prediction]=[]