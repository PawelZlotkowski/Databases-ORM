from sqlmodel import Session, select
from models.spieces import Species, SpeciesCreate

class SpeciesRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def get_all(self):
        statement = select(Species)
        items = self.session.exec(statement).all()
        return items

    def insert(self, payload: SpeciesCreate):
        item = Species.model_validate(payload)
        self.session.add(item)
        self.session.commit()
        self.session.refresh(item)
        return item