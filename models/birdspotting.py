from datetime import datetime
from typing import Optional
from sqlmodel import Field, Relationship, SQLModel
from models.birds import Bird, BirdBase

class BirdSpottingBase(SQLModel):
    bird_id: int
    spotted_at: datetime
    location: str
    observer_name: str
    notes: Optional[str] = None

class BirdSpotting(BirdSpottingBase, table=True):
    __tablename__ = "birdspotting"
    id: Optional[int] = Field(default=None, primary_key=True)
    bird_id: int = Field(foreign_key="birds.id")
    bird: Optional[Bird] = Relationship(back_populates="birdspottings")


class BirdSpottingCreate(BirdSpottingBase):
    pass

class BirdSpottingUpdate(SQLModel):
    bird_id: Optional[int] = None
    spotted_at: Optional[datetime] = None
    location: Optional[str] = None
    observer_name: Optional[str] = None
    notes: Optional[str] = None


class BirdInBirdSpottingResponse(BirdBase):
    id: int
    species_id: int


class BirdSpottingResponse(BirdSpottingBase):
    id: int
    bird: BirdInBirdSpottingResponse
