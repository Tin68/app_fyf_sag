from enum import Enum

#Constantes
MAX_WIDTH = "600px"

buttom_margin = "10%"

buttom_style = dict(
    bg ="green",
    border_radius = "1em",
    color_scheme= "grass",
    variant="soft",
    on_blur = False
)

menu_sub_trigger_style = dict(
    color = "#46a758",
    _hover={"color": "white"}
)

submenu_style = dict(
    color_scheme= "grass",
    variant="soft"
)

item_style = dict (
    color_scheme = "green",
    variant="soft"
    )

menu_drop_style = buttom_style 

'''
menu_drop_style = buttom_style | dict (
    margin_left = buttom_margin
)
'''
submenu_drop_style = submenu_style 

menu_item_style = item_style

menu_style = dict (color_scheme = "green",variant="soft")

#Size 
class Spacer(Enum):
    SMALL = "0.5em"
    MEDIUM = "0.8em"
    DEFAULT = "1em"
    NORMAL =  "1.5em"
    BIG = "2em"