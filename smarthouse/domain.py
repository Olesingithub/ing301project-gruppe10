from Buildings import Floor, Room

class Measurement:
    """
    This class represents a measurement taken from a sensor.
    """

    def __init__(self, timestamp, value, unit):
        self.timestamp = timestamp
        self.value = value
        self.unit = unit



# TODO: Add your own classes here!
    

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
        if floor not in self.floors: # skjekker om etasjen allerede finnes i self.floors
          raise ValueError(f"Floor {floor} does not exist. Please register the floor first.")
        
        room_name = room_name if room_name else f"Room {len(self.floors[floor].rooms)+ 1}" # ikke nødvendig, men generer defaut romnavn Room i+1
        room = Room(room_name,room_size)
        self.floors[floor].add_room(room)
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

   





