from sqlmodel import Session, select
from models.birds import Bird, BirdCreate
from models.spieces import Species
from fastapi import HTTPException

class BirdRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Bird)
        items = self.session.exec(statement).all()
        return items

    def insert(self, payload: BirdCreate):
        # Check if the species exists
        species = self.session.exec(select(Species).where(Species.id == payload.species_id)).first()
        if not species:
            raise HTTPException(status_code=404, detail="Species does not exist")
        item = Bird.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item
