from enum import Enum

class Route(Enum):
    INDEX = "/"
    SHEET = "/follas"
    LOGIN = "/login"
    LOGOUT = "/"
    USERDB = "/userdb"
    FORMUSERS = "/formusers"