from smarthouse.persistence import SmartHouseRepository

def test_update_room_name():
    repo = SmartHouseRepository("data/db.sql")  # Sett inn riktig databasefil
    smarthouse = repo.load_smarthouse_deep()  # Last inn smarthouse-objektet

    # Finn rommet du vil endre
    room_to_rename = next((room for room in smarthouse.get_rooms() if room.room_name == "Living Room / Kitchen"), None)

    if room_to_rename:
        repo.update_room_name(room_to_rename, "Livingroom and kitchen")
        print(f"Romnavnet er oppdatert til: {room_to_rename.room_name}")

        # Last inn data på nytt for å bekrefte
        smarthouse = repo.load_smarthouse_deep()
        updated_room = next((room for room in smarthouse.get_rooms() if room.db_id == room_to_rename.db_id), None)
        print(f"Oppdatert romnavn: {updated_room.room_name}")
    else:
        print("Rommet ble ikke funnet!")