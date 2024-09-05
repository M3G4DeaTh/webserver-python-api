

class iotDevice:
    # Model creation (Constructor)
    def __init__(self, tag: str, password: str, logged: bool, input01: float, input02: float, input03: float, input04: float):
        self._tag = tag
        self._password = password
        self._logged = logged
        self._input01 = input01
        self._input02 = input02
        self._input03 = input03
        self._input04 = input04


    # Get and Setters
    def get_tag(self):
        return self._tag
    def set_tag(self, value):
        self._tag = value

    def get_password(self):
        return self._password
    def set_password(self, value):
        self._password = value

    def get_logged(self):
        return self._logged
    def set_logged(self, value):
        self._logged = value

    def get_input01(self):
        return self._input01
    def set_input01(self, value):
        self._input01 = value

    def get_input02(self):
        return self._input02
    def set_input02(self, value):
        self._input02 = value

    def get_input03(self):
        return self._input03
    def set_input03(self, value):
        self._input03 = value

    def get_input04(self):
        return self._input04
    def set_input04(self, value):
        self._input04 = value

    
