
class Room:
    def __init__(self,name: str, area: float):
        if area < 0:
            ValueError("Area can not be negative")
        self.name = name    
        self.area = area
        
    def __str__(self):
        return f"Room: {self.name}, Area: {self.area} m²" 
    

class Floor:
    def __init__(self, floor_number):
        if floor_number < 0:
            ValueError("Floor number can not be negative")
        self.floor_number = floor_number
        self.rooms =[] # self.rooms: List[room] = []
    
    def add_room(self, room: Room):
        self.rooms.append(room)
        
    def calculate_area(self):
        return sum(room.area for room in self.rooms)
    
    def __str__(self):
        return f"Floor: {self.floor_number}, Total Area: {self.calculate_area()} m²"
    
    
class Building:
    def __init__(self, name: str):
        self.name = name
        self.floors = [] # self.floor: List[Floor] = []
        
    def add_floor(self, floor: Floor):
            self.floors.append(floor)
            
    def calculate_total_area(self):
        return sum(floor.calculate_area() for floor in self.floors)
    
    def __str__(self):
        return f"Building {self.name}, Total area: {self.calculate_total_area()} m² "
    
    
    
    
     
        

