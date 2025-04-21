import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from smarthouse.persistence import SmartHouseRepository
from smarthouse.domain import Sensor, Actuator,ActuatorWithSensor
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

#Devices Root   
    
@app.get("/smarthouse/device")
def get_device_info():
    """
    This endpoint returns information about all devices in the smarthouse
    """
    return [
        {
            "id": device.id,
            "model_name": device.model_name,
            "supplier": device.supplier,
            "device_type": device.device_type,
            "room_name": device.room.room_name if device.room and device.room.room_name else "Unknown",
            "floor_id": device.room.floor.level if device.room and device.room.floor else "Unknown",
        }   
        
        for device in smarthouse.get_devices()
    ]
    
@app.get("/smarthouse/device/{uuid}")
def get_device_info(uuid: str):
    """
    This endpoint returns information about a specific device identified by its UUID.
    """
    # Hent enheten basert på UUID
    device = next((d for d in smarthouse.get_devices() if d.id == uuid), None)
  
    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")
    
    # Returner informasjon om enheten
    return {
        "id": device.id,
        "model_name": device.model_name,
        "supplier": device.supplier,
        "device_type": device.device_type,
        "room_name": device.room.room_name if device.room and device.room.room_name else "Unknown",
        "floor_id": device.room.floor.level if device.room and device.room.floor else "Unknown",
    }
    
#Sensor Root   


@app.get("/smarthouse/sensor/{uuid}/current")
def get_current_sensor_measurement(uuid: str):
    """
    This endpoint returns the latest measurement for a specific sensor identified by its UUID.
    """
    # Finn sensoren basert på UUID
    sensor = next((d for d in smarthouse.get_devices() if isinstance(d, Sensor) and d.id == uuid), None)

    if sensor is None:
        raise HTTPException(status_code=404, detail="Sensor not found")

    # Hent siste måling fra sensoren
    latest_measurement = sensor.last_measurement()

    # Returner informasjon om sensoren og siste måling
    return {
        "id": sensor.id,
        "model_name": sensor.model_name,
        "supplier": sensor.supplier,
        "device_type": sensor.device_type,
        "unit": sensor.unit if sensor.unit else "Unknown",  # Sjekk om enheten er definert
        "last_measurement": {
            "timestamp": latest_measurement.timestamp,
            "value": latest_measurement.value,
            "unit": sensor.unit if sensor.unit else "Unknown",  # Sjekk om enheten er definert
        },
        "room_name": sensor.room.room_name if sensor.room and sensor.room.room_name else "Unknown",
        "floor_id": sensor.room.floor.level if sensor.room and sensor.room.floor else "Unknown",
    }

if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
