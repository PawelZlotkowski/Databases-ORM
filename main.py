from fastapi import FastAPI
from database import start_db, get_session
from repositories.spieces import SpeciesRepository
from routers.spieces import router as species_router
from routers.birds import router as birds_router


app = FastAPI()
start_db()
app.include_router(species_router)
app.include_router(birds_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}