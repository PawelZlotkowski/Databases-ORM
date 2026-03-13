from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from models.spieces import Species
from pydantic import Field as PydanticField

if TYPE_CHECKING:
    from models.birdspotting import BirdSpotting

class BirdBase(SQLModel):
    nickname: str
    ring_code: str
    age: int = PydanticField(ge=0)  # Age cannot be negative

class Bird(BirdBase, table=True):
    __tablename__ = "birds"
    id: Optional[int] = Field(default=None, primary_key=True)
    species_id: int = Field(foreign_key="species.id")
    species: Optional[Species] = Relationship(back_populates="birds")
    birdspottings: List["BirdSpotting"] = Relationship(back_populates="bird")

class BirdCreate(BirdBase):
    species_id: int

class BirdUpdate(SQLModel):
    nickname: Optional[str] = None
    ring_code: Optional[str] = None
    age: Optional[int] = PydanticField(default=None, ge=0)  # Age cannot be negative
    species_id: Optional[int] = None
