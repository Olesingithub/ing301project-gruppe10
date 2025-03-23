import sqlite3
from typing import Optional

from smarthouse.domain import Measurement

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
        When calling this method to obtain a cursors, you have to 
        rememeber calling `commit/rollback` and `close` yourself when
        you are done with issuing SQL commands.
        """
        return self.conn.cursor()

    def reconnect(self):
        self.conn.close()
        self.conn = sqlite3.connect(self.file)

    
    def load_smarthouse_deep(self):
        """
        This method retrives the complete single instance of the _SmartHouse_ 
        object stored in this database. The retrieval yields a _deep_ copy, i.e.
        all referenced objects within the object structure (e.g. floors, rooms, devices) 
        are retrieved as well. 
        """
        # TODO: START here! remove the following stub implementation and implement this function 
        #       by retrieving the data from the database via SQL `SELECT` statements.

        c = self.cursor()
        c.execute("SELECT * FROM rooms;")
        get_rooms = c.fetchall()
        c.execute(""" SELECT area FROM rooms ; """)
        get_area = c.fetchall
        c.execute(""" SELECT * FROM devices; """)
        get_devices = c.fetchall()
        get_device_by_id = c.execute(""" SELECT d.id FROM devices d""").fetchall()
        c.close()


        return get_rooms, get_area, get_devices, get_device_by_id


    def get_latest_reading(self, sensor) -> Optional[Measurement]:
        """
        Retrieves the most recent sensor reading for the given sensor if available.
        Returns None if the given object has no sensor readings.
        """
        # TODO: After loading the smarthouse, continue here
        m = Measurement()
        c = self.cursor()
        query = c.execute("""
               SELECT *, MAX(m.ts) AS ts
               FROM devices d, measurements m
               WHERE d.id = {0};
               """, sensor.id)
        if query is not None:
            row = query.fetchall()
            m.timestamp = row[7]
            m.value = row[8]
            m.unit = row[9]
            c.close()
            return m
        else:
            m.timestamp = None
            m.value = None
            m.unit = None
            c.close()
            return None


    def update_actuator_state(self, actuator):
        """
        Saves the state of the given actuator in the database. 
        """
        # TODO: Implement this method. You will probably need to extend the existing database structure: e.g.
        #       by creating a new table (`CREATE`), adding some data to it (`INSERT`) first, and then issue
        #       and SQL `UPDATE` statement. Remember also that you will have to call `commit()` on the `Connection`
        #       stored in the `self.conn` instance variable.

        if not self.conn:
            raise ValueError("Database connection is not established.")

        if not hasattr(actuator, 'id') or not hasattr(actuator, 'state'):
         raise ValueError("The actuator object must have 'id' and 'state' attributes.")

        
        cursor = self.cursor()

        try:
            # Opprett tabellen hvis den ikke finnes
          
            cursor.execute('''
             CREATE TABLE IF NOT EXISTS actuators (
                actuator_id TEXT PRIMARY KEY,
                state TEXT      
                )
            ''')

            # Sjekk om actuatoren allerede finnes i databasen
            cursor.execute('SELECT state FROM actuators WHERE actuator_id = ?', (actuator.id,))
            result = cursor.fetchone()
        
            if result:
             # Oppdater tilstanden hvis actuatoren allerede finnes
                cursor.execute('''
                   UPDATE actuators
                   SET state = ?
                   WHERE actuator_id = ?
             ''', (actuator.state, actuator.id))
                
            else:
             # Sett inn en ny rad hvis actuatoren ikke finnes
             cursor.execute('''
                  INSERT INTO actuators (actuator_id, state)
                  VALUES (?, ?)
             ''', (actuator.id, actuator.state))
        
            # Commit endringene
            self.conn.commit()
    
        except sqlite3.Error as e:
            # Håndter eventuelle feil
            print(f"An error occurred: {e}")
            self.conn.rollback()
    
        finally:
            # Lukk cursor
            cursor.close()


    # statistics

    
    def calc_avg_temperatures_in_room(self, room, from_date: Optional[str] = None, until_date: Optional[str] = None) -> dict:
        """Calculates the average temperatures in the given room for the given time range by
        fetching all available temperature sensor data (either from a dedicated temperature sensor 
        or from an actuator, which includes a temperature sensor like a heat pump) from the devices 
        located in that room, filtering the measurement by given time range.
        The latter is provided by two strings, each containing a date in the ISO 8601 format.
        If one argument is empty, it means that the upper and/or lower bound of the time range are unbounded.
        The result should be a dictionary where the keys are strings representing dates (iso format) and 
        the values are floating point numbers containing the average temperature that day.
        """
        # TODO: This and the following statistic method are a bit more challenging. Try to design the respective 
        #       SQL statements first in a SQL editor like Dbeaver and then copy it over here.  
        return NotImplemented

    
    def calc_hours_with_humidity_above(self, room, date: str) -> list:
        """
        This function determines during which hours of the given day
        there were more than three measurements in that hour having a humidity measurement that is above
        the average recorded humidity in that room at that particular time.
        The result is a (possibly empty) list of number representing hours [0-23].
        """
        # TODO: implement
        cursor = self.cursor() # Bruker cursor() - metoden

        try: # SQL spørringer
            cursor.execute('''
                SELECT strftime('%H',timestamp) AS hour, AVG(humidity) AS avg_humidity
                From measurements
                WHERE room_id = ? AND date(timestamp) = ?
                GROUP BY hour              
                ''',(room.id, date))
            
            # Lagrer gjennomsnittlig luftfuktighet per time i dictionary
            avg_humidity_per_hour = {row[0]: row[1] for row in cursor.fetchall()} 

            # Finner timer med høy luftfuktighet
            hours_with_high_humidity = []

            for hour, avg_humidity in avg_humidity_per_hour.items():
                cursor.execute('''
                    SELECT COUNT(*)
                    FROM measurements
                    WHERE room_id = ? AND strftime('%H', timestamp) = ? AND date(timestamp) = ? AND humidity > ?
                ''', (room.id, hour, date, avg_humidity))

                count = cursor.fetchone()[0]
                if count > 3:
                    hours_with_high_humidity.append(int(hour))
                
            return hours_with_high_humidity # returnerer resultatet
        
        # feilhåndtering
        except sqlite3.Error as e:
            print(f"An error occured: {e}")
            return[]
        
        # lukker cursor
        finally:
            cursor.close() #Lukk cursoren manuelt



