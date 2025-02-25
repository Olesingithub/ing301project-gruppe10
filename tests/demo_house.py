from smarthouse.domain import SmartHouse,Device

DEMO_HOUSE = SmartHouse("Our_House")

# Building house structure
# TODO: continue registering the remaining floor, rooms and devices


ground_floor = DEMO_HOUSE.register_floor(1)
second_floor = DEMO_HOUSE.register_floor(2)

#etage 1 
Garage = DEMO_HOUSE.register_room(ground_floor, 19, "Garage")
entrance = DEMO_HOUSE.register_room(ground_floor, 13.5, "Entrance")
Guest_Room_1 = DEMO_HOUSE.register_room(ground_floor, 8, "Guest_Room_1")
Bathroom = DEMO_HOUSE.register_room(ground_floor, 6.3, "Bathroom")
LivingRoom_Kitchen = DEMO_HOUSE.register_room(ground_floor, 39.75, "LivingRoom_Kitchen")

# etage 2
Guest_Room_2 = DEMO_HOUSE.register_room(second_floor, 8, "Guest_Room_2")
Bathroom_2 = DEMO_HOUSE.register_room(second_floor, 9.25, "Bathroom_2")
Office = DEMO_HOUSE.register_room(second_floor, 11.75, "Office")
Hallway = DEMO_HOUSE.register_room(second_floor, 10, "Hallway")
Guest_Room_3 = DEMO_HOUSE.register_room(second_floor, 10, "Guest_Room_3")
Dressing_room = DEMO_HOUSE.register_room(second_floor, 4, "Dressing_room")
Master_bedroom = DEMO_HOUSE.register_room(second_floor, 17, "Master_bedroom")

# Enheter som er sensorer
co2_sensor = Device("8a43b2d7-e8d3-4f3d-b832-7dbf37bf629e", "ElysianTech", "Smoke Warden 1000", "sensor")
electricity_meter = Device("a2f8690f-2b3a-43cd-90b8-9deea98b42a7", "MysticEnergy Innovations", "Volt Watch Elite", "sensor")
motion_sensor = Device("cd5be4e8-0e6b-4cb5-a21f-819d06cf5fc5", "NebulaGuard Innovations", "MoveZ Detect 69", "sensor")
humidity_sensor = Device("3d87e5c0-8716-4b0b-9c67-087eaae07b45", "AetherCorp", "Aqua Alert 800", "sensor")
temperature_sensor = Device("4d8b1d62-7921-4917-9b70-bbd31ff6e28e", "AetherCorp", "SmartTemp 42", "sensor")
air_quality_sensor = Device("7c6e35e1-2d8b-4d81-a586-5d01a03bb02c", "CelestialSense Technologies", "AeroGuard Pro", "sensor")

# Enheter som er aktuatorer
smart_lock = Device("4d5f1ac6-906a-4fd1-b4bf-3a0671e4c4f1", "MythicalTech", "Guardian Lock 7000", "actuator")
heat_pump = Device("5e13cabc-5c58-4bb3-82a2-3039e4480a6d", "ElysianTech", "Thermo Smart 6000", "actuator")
smart_oven_1 = Device("8d4e4c98-21a9-4d1e-bf18-523285ad90f6", "AetherCorp", "Phennix HEAT 333", "actuator")
automatic_garage_door = Device("9a54c1ec-0cb5-45a7-b20d-2a7349fb132", "MythicalTech", "Guardian Lock 9000", "actuator")
smart_oven_2 = Device("c1e8fa9c-4bb8d-487a-a1a5-2b148ee9d2d1", "IgnisTech Solutions", "Ember Heat 3000", "actuator")
smart_plug = Device("1a66c3d6-22b2-44fe-bf5c-eb5b9d1a8c79", "MysticEnergy Innovations", "FlowState X", "actuator")
dehumidifier = Device("9e5b8274-4e77-4e4e-80d2-b40d648e802a", "ArcaneTech Solutions", "Hydra Dry 8000", "actuator")
light_bulb = Device("6b1c5f6b-37f6-4e3d-9145-1cfbe2f1fc28", "Elysian Tech", "Lumina Glow 4000", "actuator")


#print(DEMO_HOUSE)
