class users:
    # Model creation (Constructor)
    def __init__(self, tag: str, password: str, logged: bool):
        self._tag = tag
        self._password = password
        self._logged = logged


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


    
