import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from pathlib import Path
from fastapi import HTTPException
import os
from urllib.parse import unquote  # Add this import

def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

if not (Path.cwd() / "www").exists():
    os.chdir(Path.cwd().parent)
if (Path.cwd() / "www").exists():
    # http://localhost:8000/welcome/index.html
    app.mount("/static", StaticFiles(directory="www"), name="static")


# http://localhost:8000/ -> welcome page
@app.get("/")
def root():
    return RedirectResponse("/static/index.html")


# Health Check / Hello World
@app.get("/hello")
def hello(name: str = "world"):
    return {"hello": name}


# Starting point ...

@app.get("/smarthouse")
def get_smarthouse_info() -> dict[str, int | float]:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return {
        "no_rooms": len(smarthouse.get_rooms()),
        "no_floors": len(smarthouse.get_floors()),
        "registered_devices": len(smarthouse.get_devices()),
        "area": smarthouse.get_area()
    }

# TODO: implement the remaining HTTP endpoints as requested in
# https://github.com/selabhvl/ing301-projectpartC-startcode?tab=readme-ov-file#oppgavebeskrivelse
# here ...

@app.get("/smarthouse/floor")
def get_smarthouse_info() -> list[dict[str, int | float]]:
    """
    This endpoint returns information about all floors in the smarthouse
    """
    return [ 
        {
        "floor_id": floor.level,
        "no_rooms": len(floor.rooms), # Bruker direkte  tilgang til listen
        "area": sum(room.room_size for room in floor.rooms)
        }
        for floor in smarthouse.get_floors()
    ]
    
@app.get("/smarthouse/floor/{fid}")
def get_smarthouse_info(fid: int):  # <-- Dette er viktig!
    """
    This endpoint returns information about spesific floor selected
    """
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)
  
    if floor is None:
        return HTTPException(status_code=404, detail = "Floor not found")
    
    return {
        "floor_id": floor.level,
        "no_rooms": len(floor.rooms), # Bruker direkte  tilgang til listen
        "area": sum(room.room_size for room in floor.rooms)
    }



@app.get("/smarthouse/floor/{fid}/room")
def get_smarthouse_info(fid: int):
    """
    This endpoint returns information about spesific floors, and rooms in them
    """
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)
  
    if floor is None:
        return HTTPException(status_code=404, detail = "Floor not found")
    
    
    return [ 
    {
        "floor_id": floor.level,
        "room_name": room.room_name,
        "area": room.room_size,
        "devices": [
            {
                "id": device.id,
                "model_name": device.model_name,
                "supplier": device.supplier,
                "device_type": device.device_type,
            }
            for device in room.devices
        ]
    }
    for room in floor.rooms
]
    
@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_smarthouse_info(fid: int, rid: str = None):
    """
    This endpoint returns information about specific floors and specific rooms in them
    """
    floor = next((f for f in smarthouse.get_floors() if f.level == fid), None)

    if floor is None:
        return HTTPException(status_code=404, detail="Floor not found")
    
    room = next((r for r in floor.rooms if r.room_name.lower() == rid.lower()), None)

    if room is None:
        return HTTPException(status_code=404, detail="Room not found in this floor")
     
    return {
        "floor_id": floor.level,
        "room_name": room.room_name,
        "area": room.room_size,
        "devices": [
            {
                "id": device.id,
                "model_name": device.model_name,
                "supplier": device.supplier,
                "device_type": device.device_type,
            }
            for device in room.devices
        ]
    }
   

    

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
