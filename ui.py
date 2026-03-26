# ui.py
import gradio as gr
import httpx
from datetime import datetime
from typing import List, Dict
from decimal import Decimal

# Configuration
API_URL = "http://localhost:8000"

# ========================
# Data Constants
# ========================
CONSERVATION_STATUSES = [
    "Least Concern",
    "Near Threatened", 
    "Vulnerable",
    "Endangered",
    "Critically Endangered",
    "Extinct in the Wild",
    "Extinct"
]

# Bird families (you can hardcode these or fetch from API)
FAMILIES = [
    "Alcidae",
    "Accipitridae",
    "Alcedinidae",
    "Anatidae",
    "Ardeidae",
    "Columbidae",
    "Corvidae",
    "Cuculidae",
]

# ========================
# Helper: Convert Decimal to str for JSON
# ========================
def serialize_for_display(obj):
    """Convert objects that might contain Decimals to JSON-serializable format"""
    if isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, dict):
        return {k: serialize_for_display(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [serialize_for_display(item) for item in obj]
    elif isinstance(obj, datetime):
        return obj.isoformat()
    return obj

# ========================
# API Helper Functions
# ========================

async def fetch_species() -> List[Dict]:
    """Fetch all species from the API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/species/")
            data = response.json()
            return [serialize_for_display(item) for item in data]
    except Exception as e:
        print(f"Error fetching species: {e}")
        return []

async def fetch_birds() -> List[Dict]:
    """Fetch all birds from the API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/birds/")
            data = response.json()
            return [serialize_for_display(item) for item in data]
    except Exception as e:
        print(f"Error fetching birds: {e}")
        return []

async def fetch_sightings() -> List[Dict]:
    """Fetch all bird sightings from the API"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{API_URL}/birdspotting/")
            data = response.json()
            return [serialize_for_display(item) for item in data]
    except Exception as e:
        print(f"Error fetching sightings: {e}")
        return []

async def get_species_choices() -> List[str]:
    """Get list of species for dropdown"""
    try:
        species = await fetch_species()
        return [f"{s['name']} ({s['scientific_name']})" for s in species]
    except Exception as e:
        print(f"Error getting species choices: {e}")
        return []

async def get_bird_choices() -> List[str]:
    """Get list of birds for dropdown"""
    try:
        birds = await fetch_birds()
        return [f"{b['nickname']} [{b['ring_code']}]" for b in birds]
    except Exception as e:
        print(f"Error getting bird choices: {e}")
        return []

# ========================
# SPECIES TAB
# ========================

async def refresh_species_data():
    """Refresh species data table"""
    try:
        species = await fetch_species()
        df_data = []
        for s in species:
            df_data.append([
                s.get("id", ""),
                s.get("name", ""),
                s.get("scientific_name", ""),
                s.get("family", ""),
                s.get("conservation_status", ""),
                round(float(s.get("wingspan_cm", 0)), 2)
            ])
        return df_data
    except Exception as e:
        print(f"Error refreshing species: {e}")
        return []

async def create_species(name, scientific_name, family, conservation_status, wingspan_cm):
    """Create a new species"""
    try:
        if not all([name, scientific_name, family, conservation_status]):
            return [], "❌ Please fill all required fields", "", "", "", "", 0
        
        async with httpx.AsyncClient() as client:
            payload = {
                "name": name,
                "scientific_name": scientific_name,
                "family": family,
                "conservation_status": conservation_status,
                "wingspan_cm": float(wingspan_cm)
            }
            response = await client.post(f"{API_URL}/species/", json=payload)
            if response.status_code == 201:
                data = await refresh_species_data()
                return data, "✅ Species created successfully!", "", "", "", "", 0
            else:
                return [], f"❌ Error: {response.text}", "", "", "", "", 0
    except Exception as e:
        return [], f"❌ Error: {str(e)}", "", "", "", "", 0

# ========================
# BIRDS TAB
# ========================

async def refresh_birds_data():
    """Refresh birds data table"""
    try:
        birds = await fetch_birds()
        df_data = []
        for b in birds:
            species_name = "Unknown"
            if isinstance(b.get("species"), dict):
                species_name = b.get("species", {}).get("name", "Unknown")
            
            df_data.append([
                b.get("id", ""),
                b.get("nickname", ""),
                b.get("ring_code", ""),
                b.get("age", 0),
                species_name
            ])
        return df_data
    except Exception as e:
        print(f"Error refreshing birds: {e}")
        return []

async def create_bird(nickname, ring_code, age, species_choice):
    """Create a new bird"""
    try:
        if not all([nickname, ring_code, species_choice]):
            return [], "❌ Please fill all required fields", "", "", "", ""
        
        # Find species_id from choice string
        species_list = await fetch_species()
        species_id = None
        for s in species_list:
            if f"{s['name']} ({s['scientific_name']})" == species_choice:
                species_id = s["id"]
                break
        
        if not species_id:
            return [], "❌ Invalid species selected", "", "", "", ""
        
        async with httpx.AsyncClient() as client:
            payload = {
                "nickname": nickname,
                "ring_code": ring_code,
                "age": int(age) if age else 0,
                "species_id": species_id
            }
            response = await client.post(f"{API_URL}/birds/", json=payload)
            if response.status_code == 201:
                data = await refresh_birds_data()
                return data, "✅ Bird created successfully!", "", "", "", ""
            else:
                error_msg = response.text
                try:
                    error_msg = response.json().get("detail", error_msg)
                except:
                    pass
                return [], f"❌ Error: {error_msg}", "", "", "", ""
    except Exception as e:
        return [], f"❌ Error: {str(e)}", "", "", "", ""

# ========================
# SIGHTINGS TAB
# ========================

async def refresh_sightings_data():
    """Refresh sightings data table"""
    try:
        sightings = await fetch_sightings()
        df_data = []
        for s in sightings:
            bird_info = "Unknown"
            if isinstance(s.get("bird"), dict):
                bird = s.get("bird", {})
                nickname = bird.get("nickname", "Unknown")
                ring_code = bird.get("ring_code", "Unknown")
                bird_info = f"{nickname} [{ring_code}]"
            
            df_data.append([
                s.get("id", ""),
                bird_info,
                s.get("spotted_at", ""),
                s.get("location", ""),
                s.get("observer_name", ""),
                s.get("notes", "")
            ])
        return df_data
    except Exception as e:
        print(f"Error refreshing sightings: {e}")
        return []

async def create_sighting(bird_choice, spotted_at, location, observer_name, notes):
    """Create a new sighting"""
    try:
        if not all([bird_choice, spotted_at, location, observer_name]):
            return [], "❌ Please fill all required fields", "", "", "", "", ""
        
        # Find bird_id from choice string
        birds_list = await fetch_birds()
        bird_id = None
        for b in birds_list:
            if f"{b['nickname']} [{b['ring_code']}]" == bird_choice:
                bird_id = b["id"]
                break
        
        if not bird_id:
            return [], "❌ Invalid bird selected", "", "", "", "", ""
        
        async with httpx.AsyncClient() as client:
            payload = {
                "bird_id": bird_id,
                "spotted_at": spotted_at,
                "location": location,
                "observer_name": observer_name,
                "notes": notes if notes else None
            }
            response = await client.post(f"{API_URL}/birdspotting/", json=payload)
            if response.status_code == 201:
                data = await refresh_sightings_data()
                return data, "✅ Sighting recorded successfully!", "", "", "", "", ""
            else:
                error_msg = response.text
                try:
                    error_msg = response.json().get("detail", error_msg)
                except:
                    pass
                return [], f"❌ Error: {error_msg}", "", "", "", "", ""
    except Exception as e:
        return [], f"❌ Error: {str(e)}", "", "", "", "", ""

# ========================
# BUILD GRADIO INTERFACE
# ========================

def build_interface():
    with gr.Blocks(title="🦅 Birds Viewer") as demo:
        gr.Markdown("# 🦅 Birds Viewer")
        gr.Markdown("Live data from the Birds API at http://127.0.0.1:8000")
        
        with gr.Tabs():
            # ==================
            # SPECIES TAB
            # ==================
            with gr.Tab("Species"):
                gr.Markdown("## Species Management")
                gr.Markdown("View all bird species and add new ones")
                
                with gr.Row():
                    refresh_species_btn = gr.Button("🔄 Refresh", size="sm")
                
                species_table = gr.DataFrame(
                    value=[],
                    headers=["id", "name", "scientific_name", "family", "conservation_status", "wingspan_cm"],
                    interactive=False,
                    label="Species"
                )
                
                gr.Markdown("### Add New Species")
                
                with gr.Row():
                    sp_name = gr.Textbox(label="Name", placeholder="e.g., Atlantic Puffin")
                    sp_scientific = gr.Textbox(label="Scientific name", placeholder="e.g., Fratercula arctica")
                
                with gr.Row():
                    sp_family = gr.Dropdown(
                        choices=FAMILIES,
                        label="Family",
                        allow_custom_value=True
                    )
                    sp_conservation = gr.Dropdown(
                        choices=CONSERVATION_STATUSES,
                        label="Conservation status"
                    )
                
                sp_wingspan = gr.Slider(
                    minimum=5,
                    maximum=300,
                    step=5,
                    label="Wingspan (cm)",
                    value=50
                )
                
                sp_status = gr.Textbox(label="Status", interactive=False)
                sp_create_btn = gr.Button("Create species", variant="primary", size="lg")
                
                # Event handlers
                refresh_species_btn.click(
                    refresh_species_data,
                    outputs=species_table
                )
                
                sp_create_btn.click(
                    create_species,
                    inputs=[sp_name, sp_scientific, sp_family, sp_conservation, sp_wingspan],
                    outputs=[species_table, sp_status, sp_name, sp_scientific, sp_family, sp_conservation, sp_wingspan]
                )
                
                # Load initial data
                demo.load(refresh_species_data, outputs=species_table)
            
            # ==================
            # BIRDS TAB
            # ==================
            with gr.Tab("Birds"):
                gr.Markdown("## Birds Management")
                gr.Markdown("View all registered birds and add new ones")
                
                with gr.Row():
                    refresh_birds_btn = gr.Button("🔄 Refresh", size="sm")
                    refresh_species_dropdown_btn = gr.Button("🔄 Refresh species list", size="sm")
                
                birds_table = gr.DataFrame(
                    value=[],
                    headers=["id", "nickname", "ring_code", "age", "species"],
                    interactive=False,
                    label="Birds"
                )
                
                gr.Markdown("### Add New Bird")
                
                b_nickname = gr.Textbox(label="Nickname", placeholder="e.g., Skipper")
                b_ring_code = gr.Textbox(label="Ring code", placeholder="e.g., AB-1234")
                
                with gr.Row():
                    b_age = gr.Number(label="Age (years)", value=0, minimum=0)
                    b_species = gr.Dropdown(
                        choices=[],
                        label="Species"
                    )
                
                b_status = gr.Textbox(label="Status", interactive=False)
                b_create_btn = gr.Button("Create bird", variant="primary", size="lg")
                
                # Event handlers
                refresh_birds_btn.click(
                    refresh_birds_data,
                    outputs=birds_table
                )
                
                refresh_species_dropdown_btn.click(
                    get_species_choices,
                    outputs=b_species
                )
                
                b_create_btn.click(
                    create_bird,
                    inputs=[b_nickname, b_ring_code, b_age, b_species],
                    outputs=[birds_table, b_status, b_nickname, b_ring_code, b_age, b_species]
                )
                
                # Load initial data
                demo.load(refresh_birds_data, outputs=birds_table)
                demo.load(get_species_choices, outputs=b_species)
            
            # ==================
            # SIGHTINGS TAB
            # ==================
            with gr.Tab("Sightings"):
                gr.Markdown("## Bird Sightings")
                gr.Markdown("Record and view bird sightings")
                
                with gr.Row():
                    refresh_sightings_btn = gr.Button("🔄 Refresh", size="sm")
                    refresh_birds_dropdown_btn = gr.Button("🔄 Refresh birds list", size="sm")
                
                sightings_table = gr.DataFrame(
                    value=[],
                    headers=["id", "bird", "spotted_at", "location", "observer_name", "notes"],
                    interactive=False,
                    label="Sightings"
                )
                
                gr.Markdown("### Record New Sighting")
                
                s_bird = gr.Dropdown(
                    choices=[],
                    label="Bird"
                )
                
                s_spotted_at = gr.Textbox(
                    label="Spotted at (ISO 8601)",
                    placeholder="e.g., 2024-06-01T10:30:00"
                )
                
                with gr.Row():
                    s_location = gr.Textbox(label="Location", placeholder="e.g., Cliffs of Moher")
                    s_observer = gr.Textbox(label="Observer name", placeholder="e.g., Jane Doe")
                
                s_notes = gr.Textbox(label="Notes (optional)", placeholder="e.g., Flying low over water")
                
                s_status = gr.Textbox(label="Status", interactive=False)
                s_create_btn = gr.Button("Create sighting", variant="primary", size="lg")
                
                # Event handlers
                refresh_sightings_btn.click(
                    refresh_sightings_data,
                    outputs=sightings_table
                )
                
                refresh_birds_dropdown_btn.click(
                    get_bird_choices,
                    outputs=s_bird
                )
                
                s_create_btn.click(
                    create_sighting,
                    inputs=[s_bird, s_spotted_at, s_location, s_observer, s_notes],
                    outputs=[sightings_table, s_status, s_bird, s_spotted_at, s_location, s_observer, s_notes]
                )
                
                # Load initial data
                demo.load(refresh_sightings_data, outputs=sightings_table)
                demo.load(get_bird_choices, outputs=s_bird)
    
    return demo

if __name__ == "__main__":
    demo = build_interface()
    demo.launch(server_name="127.0.0.1", server_port=7860, share=False)