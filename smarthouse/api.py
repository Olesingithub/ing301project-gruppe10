from typing import Literal
import uvicorn
from fastapi import FastAPI, Response
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse, JSONResponse
from fastapi.encoders import jsonable_encoder
from smarthouse.domain import Actuator, ActuatorWithSensor, Device, Floor, Measurement, Room, Sensor, SmartHouse
from smarthouse.persistence import SmartHouseRepository
from pydantic import BaseModel
from pathlib import Path

def setup_database():
    project_dir = Path(__file__).parent.parent
    db_file = project_dir / "data" / "db.sql" # you have to adjust this if you have changed the file name of the database
    print(db_file.absolute())
    return SmartHouseRepository(str(db_file.absolute()))

app = FastAPI()

repo = setup_database()

smarthouse = repo.load_smarthouse_deep()

# Data Transfer Object definitions below
class SmartHouseInfo(BaseModel):
    no_rooms: int
    no_floors: int 
    total_area: float
    no_devices: int 


    @staticmethod
    def from_obj(house: SmartHouse):
        return SmartHouseInfo(
            no_rooms=len(house.get_rooms()),
            no_floors=len(house.get_floors()),
            total_area=house.get_area(),
            no_devices=len(house.get_devices()))


class FloorInfo(BaseModel):
    fid: int
    rooms: list[int]

    @staticmethod
    def from_obj(floor: Floor):
        return FloorInfo(
            fid=floor.level,
            rooms=[r.db_id for r in floor.rooms if r.db_id ]
        )

class RoomInfo(BaseModel):
    rid: int | None
    room_size: float
    room_name: str | None
    floor: int 
    devices: list[str]

    @staticmethod
    def from_obj(room: Room):
        return RoomInfo(
            rid=room.db_id,
            room_size=room.room_size,
            floor=room.floor.level,
            room_name=room.room_name,
            devices=[d.id for d in room.devices]
        )

class DeviceInfo(BaseModel):
    id: str
    model: str
    supplier: str
    device_type: str
    device_category: Literal["actuator"] | Literal["sensor"] | Literal["actuator_with_sensor"] | Literal["unknown"]
    room: int | None


    @staticmethod
    def from_obj(device: Device):
        category : Literal['actuator', 'sensor', 'actuator_with_sensor', 'unknown'] = "unknown"
        if isinstance(device, ActuatorWithSensor):
            category = "actuator_with_sensor"
        elif isinstance(device, Actuator):
            category = "actuator"
        elif isinstance(device, Sensor):
            category = "sensor"
        return DeviceInfo(
            id=device.id,
            model=device.model_name,
            supplier=device.supplier,
            device_type=device.device_type,
            device_category=category,
            room=device.room.db_id if device.room else None
        )

class ActuatorStateInfo(BaseModel):
    state: str | float

    @staticmethod
    def from_obj(actuator: Actuator):
        if actuator.state and isinstance(actuator.state, float):
            return ActuatorStateInfo(state=actuator.state)
        elif actuator.state:
            return ActuatorStateInfo(state="running")
        else:
            return ActuatorStateInfo(state="off")




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


@app.get("/smarthouse")
def get_smarthouse_info() -> SmartHouseInfo:
    """
    This endpoint returns an object that provides information
    about the general structure of the smarthouse.
    """
    return SmartHouseInfo.from_obj(smarthouse)


@app.get("/smarthouse/floor")
def get_floors() -> list[FloorInfo]:
    return [FloorInfo.from_obj(x) for x in smarthouse.get_floors()]


@app.get("/smarthouse/floor/{fid}")
def get_floor(fid: int) -> Response:
    for f in smarthouse.get_floors():
        if f.level == fid:
            return JSONResponse(content=jsonable_encoder(FloorInfo.from_obj(f)))
    return Response(status_code=404)


@app.get("/smarthouse/floor/{fid}/room")
def get_rooms(fid: int) -> list[RoomInfo]:
    return [RoomInfo.from_obj(r) for r in smarthouse.get_rooms() if r.floor.level == fid]


@app.get("/smarthouse/floor/{fid}/room/{rid}")
def get_room(fid: int, rid: int) -> Response:
    for r in smarthouse.get_rooms():
        if r.db_id == rid and r.floor.level == fid:
            return JSONResponse(content=jsonable_encoder(RoomInfo.from_obj(r)))
    return Response(status_code=404)


@app.get("/smarthouse/device")
def get_devices() -> list[DeviceInfo]:
    return [DeviceInfo.from_obj(d) for d in smarthouse.get_devices()]


@app.get("/smarthouse/device/{uuid}")
def get_device(uuid: str) -> Response:
    for d in smarthouse.get_devices():
        if d.id == uuid:
            return JSONResponse(content=jsonable_encoder(DeviceInfo.from_obj(d)))
    return Response(status_code=404)


@app.get("/smarthouse/sensor/{uuid}/current")
def get_most_recent_measurement(uuid: str) -> Response:
    device = smarthouse.get_device_by_id(uuid)
    if device and device.is_sensor():
        reading = repo.get_latest_reading(device)
        if reading:
            return JSONResponse(content=jsonable_encoder(reading))
        else:
            return JSONResponse(content=jsonable_encoder({'reason': 'no timeseries available'}), status_code=404)
    else:
        return JSONResponse(content=jsonable_encoder({'reason': 'sensor with id not found'}), status_code=404)


@app.post("/smarthouse/sensor/{uuid}/current")
def add_sensor_measurement(uuid: str, measurement: Measurement) -> Response:
    device = smarthouse.get_device_by_id(uuid)
    if device and device.is_sensor():
        repo.insert_measurement(uuid, measurement)
        return JSONResponse(content=jsonable_encoder(measurement), status_code=201)
    else:
        return JSONResponse(content=jsonable_encoder({'reason': 'sensor with uuid not found'}), status_code=404)


@app.get("/smarthouse/sensor/{uuid}/values")
def get_measurements(uuid: str, n: int | None = None) -> Response:
    device = smarthouse.get_device_by_id(uuid)
    if device and device.is_sensor():
        result = repo.get_readings(uuid, n)
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content=jsonable_encoder({'reason': 'sensor with uuid not found'}), status_code=404)


@app.delete("/smarthouse/sensor/{uuid}/oldest")
def delete_old_measurement(uuid: str) -> Response:
    device = smarthouse.get_device_by_id(uuid)
    if device and device.is_sensor():
        result = repo.delete_oldest_reading(uuid)
        return JSONResponse(content=jsonable_encoder(result), status_code=200)
    else:
        return JSONResponse(content=jsonable_encoder({'reason': 'sensor with uuid not found'}), status_code=404)



@app.get("/smarthouse/actuator/{uuid}/current")
def get_sensor_state(uuid: str) -> Response:
    device = smarthouse.get_device_by_id(uuid)
    if device and isinstance(device, Actuator):
        return JSONResponse(jsonable_encoder(ActuatorStateInfo.from_obj(device)))
    else:
        return JSONResponse(content=jsonable_encoder({'reason': 'actuator with uuid not found'}), status_code=404)


@app.put("/smarthouse/actuator/{uuid}/")
def update_sensor_state(uuid: str, target_state: ActuatorStateInfo) -> Response:
    device = smarthouse.get_device_by_id(uuid)
    if device and isinstance(device, Actuator):
        if isinstance(target_state.state, float):
            device.turn_on(target_state.state)
        elif target_state.state == "running":
            device.turn_on()
        elif target_state.state == "off":
            device.turn_off()
        # else leave unchanged
        repo.update_actuator_state(device)
        return JSONResponse(jsonable_encoder(ActuatorStateInfo.from_obj(device)))
    else:
        return JSONResponse(content=jsonable_encoder({'reason': 'actuator with uuid not found'}), status_code=404)
    



if __name__ == '__main__':
    uvicorn.run(app, host="127.0.0.1", port=8000)
