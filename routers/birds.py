from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database import get_session
from models.birds import Bird, BirdCreate
from repositories.birds import BirdRepository

router = APIRouter(prefix="/birds", tags=["Birds"])

def get_bird_repository(
    session: Annotated[Session, Depends(get_session)],
) -> BirdRepository:
    return BirdRepository(session)

@router.get("/", response_model=List[Bird], status_code=status.HTTP_200_OK)
async def get_birds(repo: Annotated[BirdRepository, Depends(get_bird_repository)]):
    """Retrieve all birds from the database.
    
    Returns:
        List[Bird]: A list of all birds.
    """
    return repo.get_all()

@router.post("/", response_model=Bird, status_code=status.HTTP_201_CREATED)
async def add_bird(bird: BirdCreate, repo: Annotated[BirdRepository, Depends(get_bird_repository)]):
    """Add a new bird to the database.
    
    Args:
        bird (BirdCreate): The bird data to create.
        
    Returns:
        Bird: The created bird.
        
    Raises:
        HTTPException: If the species does not exist.
    """
    return repo.insert(bird)