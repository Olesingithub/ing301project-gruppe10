from smarthouse.domain import SmartHouse

DEMO_HOUSE = SmartHouse("Our_House")

# Building house structure
# TODO: continue registering the remaining floor, rooms and devices

#etage 1 
ground_floor = DEMO_HOUSE.register_floor(1)
Garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
Guest_Room_1 = DEMO_HOUSE.register_room(ground_floor, 8, "Guest_Room_1")
Bathroom = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom")
LivngRoom_Kitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "LivngRoom_Kitchen")

# etage 2
second_floor = DEMO_HOUSE.register_floor(2)
Guest_Room_2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest_Room_2")
Bathroom_2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom_2")
Office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
Hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
Guest_Room_3 = DEMO_HOUSE.register_room(second_floor, 10, "Guest_Room_3")
Dressing_room = DEMO_HOUSE.register_room(second_floor, 4, "Dressing_room")
Master_bedroom = DEMO_HOUSE.register_room(second_floor, 17, "Master_bedroom")

#print(DEMO_HOUSE)
