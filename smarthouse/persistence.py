import sqlite3
from typing import Optional, Dict

from smarthouse.domain import SmartHouse, Measurement, Room, Floor, Device, Sensor, Actuator, ActuatorWithSensor

class SmartHouseRepository:
    """
    Provides the functionality to persist and load a _SmartHouse_ object 
    in a SQLite database.
    """

    def __init__(self, file: str) -> None:
        self.file = file 
        self.conn = sqlite3.connect(file, check_same_thread=False)

    def __del__(self):
        self.conn.close()

    def cursor(self) -> sqlite3.Cursor:
        """
        Provides a _raw_ SQLite cursor to interact with the database.
        When calling this method to obtain a cursor, you have to 
        remember calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    def load_smarthouse_deep(self):
        """
        This method retrieves the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        c = self.conn.cursor()
        smart_house = SmartHouse()

        # Load rooms
        rooms = c.execute("SELECT id, floor, area, name FROM rooms;").fetchall()
        floor_map = {}
        room_map = {}
        for room_id, floor_level, area, name in rooms:
            if floor_level not in floor_map:
                floor = smart_house.register_floor(floor_level)
                floor_map[floor_level] = floor
            else:
                floor = floor_map[floor_level]
            room = smart_house.register_room(floor, area, name)
            room.id = room_id  # Add id attribute to Room object
            room_map[room_id] = room

        # Load devices
        devices = c.execute("SELECT id, room, kind, category, supplier, product FROM devices;").fetchall()
        for device_id, room_id, kind, category, supplier, product in devices:
            room = room_map[room_id]
            if kind == "sensor":
                device = Sensor(device_id, product, supplier, category)
            elif kind == "actuator":
                device = Actuator(device_id, product, supplier, category)
            elif kind == "actuator_with_sensor":
                device = ActuatorWithSensor(device_id, product, supplier, category)
            else:
                continue
            smart_house.register_device(room, device)

        c.close()
        return smart_house

    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        c = self.cursor()

        if sensor is not None:
            query = c.execute("""
                   SELECT ts, value, unit
                   FROM measurements
                   WHERE device_id = ?
                   ORDER BY ts DESC
                   LIMIT 1;
                   """, (sensor.id,))

            row = query.fetchone()
            if row:
                m = Measurement(row[0], row[1], row[2])
            else:
                m = None
            c.close()
            return m
        else:
            c.close()
            return None

    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        if not self.conn:
            raise ValueError("Database connection is not established.")

        if not hasattr(actuator, 'id') or not hasattr(actuator, 'state'):
            raise ValueError("The actuator object must have 'id' and 'state' attributes.")

        cursor = self.cursor()

        try:
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS actuators (
                    actuator_id TEXT PRIMARY KEY,
                    state TEXT
                )
            ''')

            cursor.execute('SELECT state FROM actuators WHERE actuator_id = ?', (actuator.id,))
            result = cursor.fetchone()

            if result:
                cursor.execute('''
                    UPDATE actuators
                    SET state = ?
                    WHERE actuator_id = ?
                ''', (actuator.state, actuator.id))
            else:
                cursor.execute('''
                    INSERT INTO actuators (actuator_id, state)
                    VALUES (?, ?)
                ''', (actuator.id, actuator.state))

            self.conn.commit()

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            self.conn.rollback()

        finally:
            cursor.close()

    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> Dict[str, float]:
        """
        Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data from the devices located in that room,
        filtering the measurements by the given time range.
        """
        c = self.cursor()
        query = """
            SELECT date(m.ts) as date, AVG(m.value) as avg_temp
            FROM measurements m
            JOIN devices d ON m.device_id = d.id
            WHERE d.room_id = ?
            AND m.unit = 'C'
        """
        params = [room.id]

        if from_date:
            query += " AND m.ts >= ?"
            params.append(from_date)
        if until_date:
            query += " AND m.ts <= ?"
            params.append(until_date)

        query += " GROUP BY date"

        c.execute(query, params)
        results = c.fetchall()
        c.close()

        return {row[0]: row[1] for row in results}

    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of numbers representing hours [0-23].
        """
        cursor = self.cursor()

        try:
            cursor.execute('''
                SELECT strftime('%H', ts) AS hour, AVG(value) AS avg_humidity
                FROM measurements
                WHERE room_id = ? AND date(ts) = ? AND unit = 'percent'
                GROUP BY hour
            ''', (room.id, date))

            avg_humidity_per_hour = {row[0]: row[1] for row in cursor.fetchall()}

            hours_with_high_humidity = []

            for hour, avg_humidity in avg_humidity_per_hour.items():
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM measurements
                    WHERE room_id = ? AND strftime('%H', ts) = ? AND date(ts) = ? AND unit = 'percent' AND value > ?
                ''', (room.id, hour, date, avg_humidity))

                count = cursor.fetchone()[0]
                if count > 3:
                    hours_with_high_humidity.append(int(hour))

            return hours_with_high_humidity

        except sqlite3.Error as e:
            print(f"An error occurred: {e}")
            return []

        finally:
            cursor.close()