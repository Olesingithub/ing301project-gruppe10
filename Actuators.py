# Actuator.py

from domain import Device

class Actuator(Device):
    """
    Actuator class for the SmartHouse project.
    Inherits from Device and represents a device that can be switched on or off.
    """
    def __init__(self, name: str, device_id: int):
        # Initialize as a device with device_type set to "actuator"
        super().__init__(name, device_id, "actuator")
        self.state = False  # Initial state is OFF

    def turn_on(self):
        """Switch the actuator on."""
        self.state = True
        print(f"{self.name} (ID: {self.device_id}) is now ON")

    def turn_off(self):
        """Switch the actuator off."""
        self.state = False
        print(f"{self.name} (ID: {self.device_id}) is now OFF")

    def get_status(self):
        """Return the current status of the actuator."""
        return f"{self.name} (ID: {self.device_id}) is {'ON' if self.state else 'OFF'}"
        
# Example usage (for testing purposes only)
if __name__ == "__main__":
    actuator = Actuator("Main Light", 101)
    print(actuator.get_status())
    actuator.turn_on()
    print(actuator.get_status())
    actuator.turn_off()
    print(actuator.get_status())
