
class Sensor:
    def __init__(self, sensorID, sensorType, sensorValue):
        self.sensorID = sensorID
        self.sensorType = sensorType
        self.sensorValue = sensorValue

    def getSensorValue(self):
        self.sensorValue =