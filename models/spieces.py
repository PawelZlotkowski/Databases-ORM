from decimal import Decimal
from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from models.birds import Bird

class SpeciesBase(SQLModel):
    name: str
    scientific_name: str
    family: str
    conservation_status: str
    wingspan_cm: Decimal

class Species(SpeciesBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    birds: List["Bird"] = Relationship(back_populates="species")

class SpeciesCreate(SpeciesBase):
    pass

class SpeciesUpdate(SQLModel):
    name: Optional[str] = None
    scientific_name: Optional[str] = None
    family: Optional[str] = None
    conservation_status: Optional[str] = None
    wingspan_cm: Optional[Decimal] = None