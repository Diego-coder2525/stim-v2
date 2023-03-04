from pydantic import BaseModel
from typing import Optional
class Game(BaseModel):
    id: Optional[str]
    name:str
    description:str
    price:int