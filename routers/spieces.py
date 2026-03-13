from typing import List, Annotated, Optional
from fastapi import APIRouter, Depends, status, Query
from sqlmodel import Session
from database import get_session
from models.spieces import Species, SpeciesCreate, SpeciesUpdate
from repositories.spieces import SpeciesRepository

router = APIRouter(prefix="/species", tags=["Species"])

def get_species_repository(
    session: Annotated[Session, Depends(get_session)],
) -> SpeciesRepository:
    return SpeciesRepository(session)

@router.get("/", response_model=List[Species], status_code=status.HTTP_200_OK)
async def get_species(
    repo: Annotated[SpeciesRepository, Depends(get_species_repository)],
    conservation_status: Optional[str] = Query(None, description="Filter species by conservation status")
):
    """Retrieve all species from the database with optional filtering.
    
    Args:
        conservation_status (Optional[str]): Filter species by conservation status
        
    Returns:
        List[Species]: A list of species matching the criteria.
    """
    if conservation_status:
        return repo.get_by_conservation_status(conservation_status)
    return repo.get_all()

@router.get("/{species_id}", response_model=Species, status_code=status.HTTP_200_OK)
async def get_species_by_id(species_id: int, repo: Annotated[SpeciesRepository, Depends(get_species_repository)]):
    """Retrieve a specific species by its ID.
    
    Args:
        species_id (int): The ID of the species to retrieve.
        
    Returns:
        Species: The requested species.
        
    Raises:
        HTTPException: If the species is not found.
    """
    return repo.get_one(species_id)

@router.get("/{species_id}/with-birds", response_model=Species, status_code=status.HTTP_200_OK)
async def get_species_with_birds(species_id: int, repo: Annotated[SpeciesRepository, Depends(get_species_repository)]):
    """Retrieve a specific species by its ID with all its birds.
    
    Args:
        species_id (int): The ID of the species to retrieve.
        
    Returns:
        Species: The requested species with its birds.
        
    Raises:
        HTTPException: If the species is not found.
    """
    return repo.get_with_birds(species_id)

@router.post("/", response_model=Species, status_code=status.HTTP_201_CREATED)
async def add_species(species: SpeciesCreate, repo: Annotated[SpeciesRepository, Depends(get_species_repository)]):
    """Add a new species to the database.
    
    Args:
        species (SpeciesCreate): The species data to create.
        
    Returns:
        Species: The created species.
    """
    return repo.insert(species)

@router.put("/{species_id}", response_model=Species, status_code=status.HTTP_200_OK)
async def update_species(species_id: int, species: SpeciesUpdate, repo: Annotated[SpeciesRepository, Depends(get_species_repository)]):
    """Update a species by its ID.
    
    Args:
        species_id (int): The ID of the species to update.
        species (SpeciesUpdate): The species data to update.
        
    Returns:
        Species: The updated species.
        
    Raises:
        HTTPException: If the species is not found.
    """
    return repo.update(species_id, species)

@router.delete("/{species_id}", status_code=status.HTTP_200_OK)
async def delete_species(species_id: int, repo: Annotated[SpeciesRepository, Depends(get_species_repository)]):
    """Delete a species by its ID.
    
    Args:
        species_id (int): The ID of the species to delete.
        
    Returns:
        dict: Confirmation message.
        
    Raises:
        HTTPException: If the species is not found.
    """
    return repo.delete(species_id)