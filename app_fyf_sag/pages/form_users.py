import reflex as rx

from app_fyf_sag.componentes import routes
from app_fyf_sag.styles import utils
from app_fyf_sag.db import auth_users_db

class UsersState(rx.State):
    form_data_state: dict = []

@rx.page(
        route= routes.Route.FORMUSERS.value,
        title= utils.formusers_title,
        description= utils.formusers_description        
)
def form_users() -> rx.Component:
    return rx.flex(
    rx.vstack(
        rx.center(
            rx.card(
                rx.hstack(
                    rx.icon(tag="users-round", size = 40, color="green"),
                    rx.vstack(
                        rx.heading("Usuarios"),
                        rx.text(
                            "Gestion de usuarios.", size="1"
                        ),
                        spacing="0",
                    ),   
                    margin = "1em",           
                ), 
                rx.form.root(
                    rx.vstack(
                        rx.text(
                            "Nombre ",
                        ),
                        rx.input(
                            name="surname",
                            width = "100%",
                            required=True,
                        ),
                    ),                     
                    rx.vstack(
                        rx.text(
                            "Usuario ",
                        ),
                        rx.input(
                            name="username",
                            width = "100%",
                            required=True,
                        ),
                    ),                
                    rx.vstack(
                        rx.text(
                            "Contraseña ",
                        ),
                        rx.input(
                            name="password",
                            width = "100%",
                            type="password",
                            required=True,
                        ),
                        margin_y = "1em",  
                    ),  
                    #rx.checkbox(text="Deshabilitado", color_scheme="green"),
                    rx.hstack(
                        rx.text("Deshabilitado"),
                        rx.switch(color_scheme="green"),
                        margin_y = "1em", 
                    ),
                    rx.hstack(
                        rx.text("Rol"),
                        rx.select(
                            ["admin", "user"],
                            #value=SelectState.value,
                            #on_change=SelectState.change_value,
                            color_scheme="green",
                        ),
                        margin_y = "1em", 
                    ),
                    rx.center(
                        rx.button(
                            "Actualizar",
                            type="submit",
                            color_scheme= "grass",                                       
                        ),
                    ),
                    #on_submit=UsersState.submit,   
                    #reset_on_submit=True,
                ),
            ),
            padding = "50px 50px 50px 50px",
            bg="#1D2330",
            borderRadius="15px",
            boxShadow="41px -41px 82px #0D0F15, -41px 41px 82px #2D374B",
        ),
    ),
    justify="center",
    padding="100px",
    height="100vh" 
    ),