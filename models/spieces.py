from decimal import Decimal
from typing import Optional
from sqlmodel import Field, SQLModel

class SpeciesBase(SQLModel):
    name: str
    scientific_name: str
    family: str
    conservation_status: str
    wingspan_cm: Decimal

class Species(SpeciesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class SpeciesCreate(SpeciesBase):
    pass