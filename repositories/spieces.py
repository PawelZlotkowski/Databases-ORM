from sqlmodel import Session, select
from models.spieces import Species, SpeciesCreate, SpeciesUpdate
from fastapi import HTTPException

class SpeciesRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self):
        statement = select(Species)
        items = self.session.exec(statement).all()
        return items

    def get_one(self, species_id: int):
        statement = select(Species).where(Species.id == species_id)
        item = self.session.exec(statement).first()
        if not item:
            raise HTTPException(status_code=404, detail="Species not found")
        return item

    def get_by_conservation_status(self, conservation_status: str):
        statement = select(Species).where(Species.conservation_status == conservation_status)
        items = self.session.exec(statement).all()
        return items

    def get_with_birds(self, species_id: int):
        from sqlalchemy.orm import selectinload
        statement = select(Species).where(Species.id == species_id).options(selectinload(Species.birds))
        item = self.session.exec(statement).first()
        if not item:
            raise HTTPException(status_code=404, detail="Species not found")
        return item

    def insert(self, payload: SpeciesCreate):
        item = Species.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item

    def update(self, species_id: int, payload: SpeciesUpdate):
        species = self.get_one(species_id)
        update_data = payload.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(species, key, value)
        self.session.add(species)
        self.session.commit()
        self.session.refresh(species)
        return species

    def delete(self, species_id: int):
        species = self.get_one(species_id)
        self.session.delete(species)
        self.session.commit()
        return {"message": "Species deleted successfully"}