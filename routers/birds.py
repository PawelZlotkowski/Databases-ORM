from typing import List, Annotated
from fastapi import APIRouter, Depends
from sqlmodel import Session
from database import get_session
from models.birds import Bird, BirdCreate
from repositories.birds import BirdRepository

router = APIRouter(prefix="/birds", tags=["Birds"])

def get_bird_repository(
    session: Annotated[Session, Depends(get_session)],
) -> BirdRepository:
    return BirdRepository(session)

@router.get("/", response_model=List[Bird])
async def get_birds(repo: Annotated[BirdRepository, Depends(get_bird_repository)]):
    return repo.get_all()

@router.post("/", response_model=Bird)
async def add_bird(bird: BirdCreate, repo: Annotated[BirdRepository, Depends(get_bird_repository)]):
    return repo.insert(bird)