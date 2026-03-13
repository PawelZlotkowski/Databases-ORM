from fastapi import HTTPException
from sqlalchemy.orm import selectinload
from sqlmodel import Session, select
from models.birds import Bird
from models.birdspotting import BirdSpotting, BirdSpottingCreate
from typing import List

class BirdSpottingRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[BirdSpotting]:
        statement = select(BirdSpotting).options(selectinload(BirdSpotting.bird))
        items = self.session.exec(statement).all()
        return items

    def get_one(self, birdspotting_id: int) -> BirdSpotting:
        statement = (
            select(BirdSpotting)
            .where(BirdSpotting.id == birdspotting_id)
            .options(selectinload(BirdSpotting.bird))
        )
        item = self.session.exec(statement).first()
        if not item:
            raise HTTPException(status_code=404, detail="BirdSpotting not found")
        return item

    def insert(self, payload: BirdSpottingCreate) -> BirdSpotting:
        # Check if the bird exists
        bird = self.session.exec(select(Bird).where(Bird.id == payload.bird_id)).first()
        if not bird:
            raise HTTPException(status_code=404, detail="Bird does not exist")
        item = BirdSpotting.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return self.get_one(item.id)
