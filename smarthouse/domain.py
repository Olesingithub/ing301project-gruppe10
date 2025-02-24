#from Buildings import Floor, Room
from datetime import datetime
import random

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
    def __init__(self, name, device_id, device_type):
        self.name = name
        self.device_id = device_id
        self.device_type = device_type

    def __str__getDeviceType(self):
        if self.device_type == "sensor":
            return "Sensor"
        elif self.device_type == "actuator":
            return "Actuator"

class Sensor:
    def __init__(self, sensorID, sensorType, sensorValue):
        self.device_id = sensorID
        self.sensorType = sensorType
        self.sensorValue = sensorValue
        #self.measurements =

    def __int__getSensorID(self):
        last_sensorID = self.device_id
        self.sensorID = random.randint(1, 10000)
        append(last_sensorID, self.sensorID)
        if (self.sensorID == ):
         return self.device_id

class TemperatureSensor(Sensor):
    Measurement.Unit = "C"


class HumiditySensor(Sensor):
    Measurement.Unit = "%"

class PressureSensor(Sensor):
    Measurement.Unit = "hPa"
    airPressure = 0

    def getAirPressure(self):


class WindSpeedSensor(Sensor):
    Measurement.Unit = "mph"
    windSpeed = 0

    def getWindSpeed(self):
        self.windSpeed = random.randint(1,35)

    Measurement.Value = windSpeed
    #return
    pass

class WindDirectionSensor(Sensor):
    Measurement.Unit = "deg"
    windDirection = 0
    def getWindDirection(self):
        self.windDirection = random.randint(0,360)

        if((self.windDirection > 330)and(self.windDirection < 30)):
            print("wind direction is SW")
        elif((self.windDirection > 240)and(self.windDirection < 330)):
            print("wind direction is S")
        elif((self.windDirection > 210)and(self.windDirection < 240)):
            print("wind direction is S")

class WindGustSensor(Sensor):
    Measurement.Unit = "deg"

class WindChillSensor(Sensor):
    Measurement.Unit = "mph"

   
   
# TODO: Add your own classes here!

class Actuator:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id
        self.state = False  # False betyr "av", True betyr "på"

    def turn_on(self):
        self.state = True
        print(f"{self.name} (ID: {self.id}) er nå PÅ")

    def turn_off(self):
        self.state = False
        print(f"{self.name} (ID: {self.id}) er nå AV")

    def get_status(self):
        return f"{self.name} (ID: {self.id}) er {'PÅ' if self.state else 'AV'}"



class Room:
    def __init__(self,name: str, area: float):
        if area < 0:
          raise  ValueError("Area can not be negative")
        self.name = name    
        self.area = area
        
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
        self.floors : dict[Floor] = {} # lagrer etasjer som dictionary {etasjenummer: floor}

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
        pass

    
    def get_device(self, device_id):
        """
        This method retrieves a device object via its id.
        """
        pass
    
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
   





