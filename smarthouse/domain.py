#from Buildings import Floor, Room
from datetime import datetime
import random

from tests.demo_house import co2_sensor, air_quality_sensor, motion_sensor, humidity_sensor, temperature_sensor


class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """
    
    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit

class Device:
    """
    This class represents a device that is either a sensor or an actuator.
    """
    def __init__(self, device_id, supplier, model_name, device_type):
        self.device_id = device_id
        self.supplier = supplier
        self.model_name = model_name
        self.device_type = device_type

    def is_actuator(self):
        """Returnerer True hvis enheten er en aktuator, ellers False."""
        return self.device_type.lower() == "actuator"

    def is_sensor(self):
        """Returnerer True hvis enheten er en sensor, ellers False."""
        return self.device_type.lower() == "sensor"

    def get_device_type(self):
        """Returnerer en beskrivelse av enhetstypen."""
        return self.device_type

    def __str__(self):
        return f"Device ID: {self.device_id}, Supplier: {self.supplier}, Model: {self.model_name}, Type: {self.get_device_type()}"

class Sensor(Device):
    def __init__(self, sensor_id, supplier, sensorValue):
        super.device_id = sensor_id
        super.supplier = supplier
        self.sensorValue = sensorValue
        self.last_measurement_timestamp = None

    def measure(Measurment):
        Measurment.last_measurement_timestamp = datetime.now()
        Measurment.last_measurement_value = Measurment.sensorValue
        Measurment.device_type = "sensor"

    def getSensorID(self):
        

class TemperatureSensor(Sensor):
    def __init__(self, sensor_id, supplier, sensorValue):
        self.name = temperature_sensor
        super.sensor_id = self.device_id
        super.supplier = self.supplier

    Measurement.Unit = "C"

    def getTemperature(self):
        self.temperature = random.randint(-20, 30)
        return self.temperature

class HumiditySensor(Sensor):
    def __init__(self, sensor_id, supplier, sensorValue):
        self.name = humidity_sensor
        super.sensor_id = self.device_id
        super.supplier = self.supplier

    Measurement.Unit = "%"
    humidityValue = 0

    def getHumidityValue(self):
        self.humidityValue = random.randint(1, 100)
        return self.humidityValue

class MotionSensor(Sensor):
    def __init__(self, sensor_id, supplier, sensorValue):
        self.name = motion_sensor
        super.sensor_id = self.device_id
        super.supplier = self.supplier
    Measurement.Unit = "mps"

class AirQualitySensor(Sensor):
    def __init__(self, sensor_id, supplier, sensorValue):
        self.name = air_quality_sensor
        super.sensor_id = air_quality_sensor.device_id
        super.supplier = air_quality_sensor.supplier

    Measurement.Unit = "%"

class Co2Sensor(Sensor):
    def __init__(self, sensor_id, supplier, sensorValue):
        self.name = co2_sensor
        super.sensor_id = co2_sensor.device_id
        super.supplier = co2_sensor.supplier

    Measurement.Unit = "ppm"
   
# TODO: Add your own classes here!
    
class Actuator(Device):

    def __init__(self, device_id: str, supplier: str, model_name: str):
        # Call the Device constructor
        super().__init__(device_id, supplier, model_name)
        self._active = False
        self._target_value = None

    def is_actuator(self) -> bool:
        return True

    def get_device_type(self) -> str:
        # Provide a more specific description than the base class
        return f"Actuator ({self.model_name})"

    def turn_on(self):
        self._active = True
        print(f"{self.model_name} turned ON.")

    def turn_off(self):
        self._active = False
        print(f"{self.model_name} turned OFF.")

    def is_active(self) -> bool:
        return self._active

    def set_target_value(self, value):
        self._target_value = value

    def get_target_value(self):
        return self._target_value



class Room:
    def __init__(self, name: str, area: float):
        if area < 0:
            raise ValueError("Area can not be negative")
        self.name = name
        self.area = area
        self.devices = []  # Liste over enheter i rommet

    def add_device(self, device):
        self.devices.append(device)

    def __str__(self):
        return f"Room: {self.name}, Area: {self.area} m²"
    

class Floor:
    def __init__(self, floor_number):
        if floor_number < 0:
           raise ValueError("Floor number can not be negative")
        self.floor_number = floor_number
        self.rooms: list[Room] = []
    
    def add_room(self, room: Room):
        self.rooms.append(room)
        
    def calculate_area(self):
        return sum(room.area for room in self.rooms)  

class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """

    def __init__(self,name):
        """
        initialiserer et smartHouse med et gitt navn
        """
        self.name = name
        self.floors : dict[int, Floor] = {} # lagrer etasjer som dictionary {etasjenummer: floor}

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        if level in self.floors: # skjekker om etasjen allerede finnes i self.floors
          raise ValueError(f"Floor {level} already exists. ")
            
        floor = Floor(level) #Oppretter ny etasje med angitt nivå
        self.floors[level] = floor #lagres i self.floors (Dictionary med etasje som nøkkel)
        return floor #returnerer det nye etasjenivået
        
        

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        if floor.floor_number not in self.floors: # skjekker om etasjen allerede finnes i self.floors
          raise ValueError(f"Floor {floor.floor_number} does not exist. Please register the floor first.")
        
        room_name = room_name if room_name else f"Room {len(self.floors[floor].rooms)+ 1}" # ikke nødvendig, men generer defaut romnavn Room i+1
        room = Room(room_name,room_size)
        self.floors[floor.floor_number].add_room(room)
        return room

        


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        return sorted(self.floors.values(),key= lambda floor: floor.floor_number)


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        rooms = []
        for floor in self.floors.values():
            rooms.extend(floor.rooms) # legger til floor.rooms i samme liste som rooms
        return rooms


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """
        return sum(floor.calculate_area() for floor in self.floors.values())


    def register_device(self, room, device):
        """
        This methods registers a given device in a given room.
        """
        if not isinstance(room, Room):
            raise ValueError("Invalid room")
        if not isinstance(device, Device):
            raise ValueError("Invalid device")

        room.add_device(device)

    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        for floor in self.floors.values():
            for room in floor.rooms:
                for device in room.devices:
                    if device.device_id == device_id:
                        return device
        return None  # Returnerer None hvis enheten ikke finnes
    
    def __str__(self):
        house_info = f"SmartHouse: {self.name}, Total Area: {self.get_area()} m²\n"
        """
        for floor in self.get_floors():
            house_info += str(floor) + "\n"
            for room in floor.rooms:
                house_info += "  " + str(room) + "\n"
        """
        return house_info
        
    
"""
 # Test
if __name__ == "__main__":
    house = SmartHouse("My Smart House")

    # legger til etasjer
    floor1 = house.register_floor(1)
    floor2 = house.register_floor(2)

    # legger til rom
    house.register_room(1, 30, "Living Room")
    house.register_room(1, 15, "Kitchen")
    house.register_room(2, 20, "Bedroom")

    print(house)
"""
   





