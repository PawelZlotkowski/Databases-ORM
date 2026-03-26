from fastapi import FastAPI
from gradio.monitoring_dashboard import demo
from database import start_db, get_session
from routers.spieces import router as species_router
from routers.birds import router as birds_router
from routers.birdspotting import router as birdspotting_router
import gradio as gr


app = FastAPI()
start_db()
app.include_router(species_router)
app.include_router(birds_router)
app.include_router(birdspotting_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}

