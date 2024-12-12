from typing import List,Optional
from xml.dom.minidom import Entity
from pydantic import BaseModel,Field

class Iban(BaseModel) :
    text:str=Field(default="")

    

#Response model (used if Candidates have been found in the request sent to the API)
class IbanCandidate(BaseModel):
    iban: Optional[str] = None
    bic: Optional[str] = None
    branch: Optional[str] = None
    bank: Optional[str] = None
    address: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip: Optional[str] = None
    phone: Optional[str] = None
    fax: Optional[str] = None
    www: Optional[str] = None
    email: Optional[str] = None
    country: Optional[str] = None
    country_iso: Optional[str] = None
    account: Optional[str] = None
    bank_code: Optional[str] = None
    branch_code: Optional[str] = None
    found: Optional[str] = None
    validation: bool = Field(default=False)
    error_msg:str=Field(default="")