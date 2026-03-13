from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session
from database import get_session
from models.birds import Bird, BirdCreate, BirdUpdate
from repositories.birds import BirdRepository

router = APIRouter(prefix="/birds", tags=["Birds"])

def get_bird_repository(
    session: Annotated[Session, Depends(get_session)],
) -> BirdRepository:
    return BirdRepository(session)

@router.get("/", response_model=List[Bird], status_code=status.HTTP_200_OK)
async def get_birds(
    repo: Annotated[BirdRepository, Depends(get_bird_repository)],
    species_id: Optional[int] = Query(None, description="Filter birds by species ID"),
    skip: int = Query(0, description="Number of items to skip for pagination"),
    limit: int = Query(100, description="Maximum number of items to return")
):
    """Retrieve all birds from the database with optional filtering and pagination.
    
    Args:
        species_id (Optional[int]): Filter birds by species ID
        skip (int): Number of items to skip for pagination
        limit (int): Maximum number of items to return
        
    Returns:
        List[Bird]: A list of birds matching the criteria.
    """
    if species_id:
        return repo.get_by_species(species_id)[skip:skip+limit]
    return repo.get_all()[skip:skip+limit]

@router.get("/{bird_id}", response_model=Bird, status_code=status.HTTP_200_OK)
async def get_bird(bird_id: int, repo: Annotated[BirdRepository, Depends(get_bird_repository)]):
    """Retrieve a specific bird by its ID.
    
    Args:
        bird_id (int): The ID of the bird to retrieve.
        
    Returns:
        Bird: The requested bird.
        
    Raises:
        HTTPException: If the bird is not found.
    """
    return repo.get_one(bird_id)

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

@router.put("/{bird_id}", response_model=Bird, status_code=status.HTTP_200_OK)
async def update_bird(bird_id: int, bird: BirdUpdate, repo: Annotated[BirdRepository, Depends(get_bird_repository)]):
    """Update a bird by its ID.
    
    Args:
        bird_id (int): The ID of the bird to update.
        bird (BirdUpdate): The bird data to update.
        
    Returns:
        Bird: The updated bird.
        
    Raises:
        HTTPException: If the bird is not found or species does not exist.
    """
    return repo.update(bird_id, bird)

@router.delete("/{bird_id}", status_code=status.HTTP_200_OK)
async def delete_bird(bird_id: int, repo: Annotated[BirdRepository, Depends(get_bird_repository)]):
    """Delete a bird by its ID.
    
    Args:
        bird_id (int): The ID of the bird to delete.
        
    Returns:
        dict: Confirmation message.
        
    Raises:
        HTTPException: If the bird is not found.
    """
    return repo.delete(bird_id)