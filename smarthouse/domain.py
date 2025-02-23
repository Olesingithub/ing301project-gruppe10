from Buildings import Building, Floor, Room
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
        self.measurements =

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

class WindSpeedSensor(Sensor):
    Measurement.Unit = "mph"
    windSpeed = 0

    def getWindSpeed(self):
        self.windSpeed = random.randint(1,100)

class WindDirectionSensor(Sensor):
    Measurement.Unit = "deg"

class WindGustSensor(Sensor):
    Measurement.Unit = "deg"

class WindChillSensor(Sensor):
    Measurement.Unit = "mph"



    # TODO: Add your own classes here!


class SmartHouse:
    """
    This class serves as the main entity and entry point for the SmartHouse system app.
    Do not delete this class nor its predefined methods since other parts of the
    application may depend on it (you are free to add as many new methods as you like, though).

    The SmartHouse class provides functionality to register rooms and floors (i.e. changing the 
    house's physical layout) as well as register and modify smart devices and their state.
    """

    def register_floor(self, level):
        """
        This method registers a new floor at the given level in the house
        and returns the respective floor object.
        """
        if level in self.floors: # skjekker om 
            ValueError(f"Floor {level} already exists. ")
            
        floor = Floor(level) #Oppretter ny etasje med angitt nivå
        self.floors[level] = floor #lagres i self.floors (Dictionary med etasje som nøkkel)
        return floor #returnerer det nye etasjenivået
        
        

    def register_room(self, floor, room_size, room_name = None):
        """
        This methods registers a new room with the given room areal size 
        at the given floor. Optionally the room may be assigned a mnemonic name.
        """
        pass


    def get_floors(self):
        """
        This method returns the list of registered floors in the house.
        The list is ordered by the floor levels, e.g. if the house has 
        registered a basement (level=0), a ground floor (level=1) and a first floor 
        (leve=1), then the resulting list contains these three flors in the above order.
        """
        pass


    def get_rooms(self):
        """
        This methods returns the list of all registered rooms in the house.
        The resulting list has no particular order.
        """
        pass


    def get_area(self):
        """
        This methods return the total area size of the house, i.e. the sum of the area sizes of each room in the house.
        """


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

