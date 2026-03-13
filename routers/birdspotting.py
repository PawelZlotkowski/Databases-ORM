from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session
from database import get_session
from models.birdspotting import BirdSpottingCreate, BirdSpottingResponse, BirdSpottingUpdate
from repositories.birdspotting import BirdSpottingRepository

router = APIRouter(prefix="/birdspotting", tags=["Bird Spotting"])

def get_birdspotting_repository(
    session: Annotated[Session, Depends(get_session)],
) -> BirdSpottingRepository:
    return BirdSpottingRepository(session)

@router.get("/", response_model=List[BirdSpottingResponse], status_code=status.HTTP_200_OK)
async def get_birdspottings(
    repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)],
    observer_name: Optional[str] = Query(None, description="Filter bird spottings by observer name")
):
    """Retrieve all bird spottings from the database with optional filtering.
    
    Args:
        observer_name (Optional[str]): Filter bird spottings by observer name
        
    Returns:
        List[BirdSpottingResponse]: A list of bird spottings matching the criteria.
    """
    if observer_name:
        return repo.get_by_observer(observer_name)
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

@router.put("/{birdspotting_id}", response_model=BirdSpottingResponse, status_code=status.HTTP_200_OK)
async def update_birdspotting(birdspotting_id: int, birdspotting: BirdSpottingUpdate, repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]):
    """Update a bird spotting by its ID.
    
    Args:
        birdspotting_id (int): The ID of the bird spotting to update.
        birdspotting (BirdSpottingUpdate): The bird spotting data to update.
        
    Returns:
        BirdSpottingResponse: The updated bird spotting.
        
    Raises:
        HTTPException: If the bird spotting is not found or bird does not exist.
    """
    return repo.update(birdspotting_id, birdspotting)

@router.delete("/{birdspotting_id}", status_code=status.HTTP_200_OK)
async def delete_birdspotting(birdspotting_id: int, repo: Annotated[BirdSpottingRepository, Depends(get_birdspotting_repository)]):
    """Delete a bird spotting by its ID.
    
    Args:
        birdspotting_id (int): The ID of the bird spotting to delete.
        
    Returns:
        dict: Confirmation message.
        
    Raises:
        HTTPException: If the bird spotting is not found.
    """
    return repo.delete(birdspotting_id)

