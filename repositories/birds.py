from sqlmodel import Session, select
from models.birds import Bird, BirdCreate, BirdUpdate
from models.spieces import Species
from fastapi import HTTPException

class BirdRepository:
    def __init__(self, session: Session):
        self.session = session

    def get_all(self):
        statement = select(Bird)
        items = self.session.exec(statement).all()
        return items

    def get_one(self, bird_id: int):
        statement = select(Bird).where(Bird.id == bird_id)
        item = self.session.exec(statement).first()
        if not item:
            raise HTTPException(status_code=404, detail="Bird not found")
        return item

    def get_by_species(self, species_id: int):
        statement = select(Bird).where(Bird.species_id == species_id)
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

    def update(self, bird_id: int, payload: BirdUpdate):
        bird = self.get_one(bird_id)
        # Check if the species exists when updating species_id
        if payload.species_id is not None:
            species = self.session.exec(select(Species).where(Species.id == payload.species_id)).first()
            if not species:
                raise HTTPException(status_code=404, detail="Species does not exist")
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(bird, key, value)
        self.session.add(bird)
        self.session.commit()
        self.session.refresh(bird)
        return bird

    def delete(self, bird_id: int):
        bird = self.get_one(bird_id)
        self.session.delete(bird)
        self.session.commit()
        return {"message": "Bird deleted successfully"}
