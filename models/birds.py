from typing import TYPE_CHECKING, List, Optional
from sqlmodel import Field, Relationship, SQLModel
from models.spieces import Species

if TYPE_CHECKING:
    from models.birdspotting import BirdSpotting

class BirdBase(SQLModel):
    nickname: str
    ring_code: str
    age: int

class Bird(BirdBase, table=True):
    __tablename__ = "birds"
    id: Optional[int] = Field(default=None, primary_key=True)
    species_id: int = Field(foreign_key="species.id")
    species: Optional[Species] = Relationship(back_populates="birds")
    birdspottings: List["BirdSpotting"] = Relationship(back_populates="bird")

class BirdCreate(BirdBase):
    species_id: int
