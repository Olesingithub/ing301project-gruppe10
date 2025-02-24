class Actuator:
    def __init__(self, name: str, id: int):
        self.name = name
        self.id = id
        self.state = False  # False betyr "av", True betyr "på"

    def turn_on(self):
        self.state = True
        print(f"{self.name} (ID: {self.id}) er nå PÅ")

    def turn_off(self):
        self.state = False
        print(f"{self.name} (ID: {self.id}) er nå AV")

    def get_status(self):
        return f"{self.name} (ID: {self.id}) er {'PÅ' if self.state else 'AV'}"
