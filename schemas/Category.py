from pydantic import BaseModel
from typing import Optional
class Category(BaseModel):
    id: Optional[str]
    name:str
    