from typing import List, Annotated
from fastapi import APIRouter, Depends, status
from sqlmodel import Session
from database import get_session
from models.birdspotting import BirdSpottingCreate, BirdSpottingResponse
from repositories.birdspotting import BirdSpottingRepository

router = APIRouter(prefix="/birdspotting", tags=["Bird Spotting"])

def get_birdspotting_repository(
    session: Annotated[Session, Depends(get_session)],
) -> BirdSpottingRepository:
    return BirdSpottingRepository(session)

@router.get("/", response_model=List[BirdSpottingResponse], status_code=status.HTTP_200_OK)
async def get_birdspottings(repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]):
    """Retrieve all bird spottings from the database.
    
    Returns:
        List[BirdSpottingResponse]: A list of all bird spottings.
    """
    return repo.get_all()

@router.get("/{birdspotting_id}", response_model=BirdSpottingResponse, status_code=status.HTTP_200_OK)
async def get_birdspotting_by_id(birdspotting_id: int, repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]):
    """Retrieve a specific bird spotting by its ID.
    
    Args:
        birdspotting_id (int): The ID of the bird spotting to retrieve.
        
    Returns:
        BirdSpottingResponse: The requested bird spotting.
        
    Raises:
        HTTPException: If the bird spotting is not found.
    """
    return repo.get_one(birdspotting_id)

@router.post("/", response_model=BirdSpottingResponse, status_code=status.HTTP_201_CREATED)
async def add_birdspotting(birdspotting: BirdSpottingCreate, repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]):
    """Add a new bird spotting to the database.
    
    Args:
        birdspotting (BirdSpottingCreate): The bird spotting data to create.
        
    Returns:
        BirdSpottingResponse: The created bird spotting.
        
    Raises:
        HTTPException: If the bird does not exist.
    """
    return repo.insert(birdspotting)

