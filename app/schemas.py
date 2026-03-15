from pydantic import BaseModel, Field
from typing import List, Dict

class Powerplant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: float
    pmax: float

class Fuels(BaseModel):
    gas: float = Field(..., alias="gas(euro/MWh)")
    kerosine: float = Field(..., alias="kerosine(euro/MWh)")
    co2: float = Field(..., alias="co2(euro/ton)")
    wind: float = Field(..., alias="wind(%)")

class Payload(BaseModel):
    load: float
    fuels: Fuels
    powerplants: List[Powerplant]

class ProductionResponse(BaseModel):
    name: str
    p: float