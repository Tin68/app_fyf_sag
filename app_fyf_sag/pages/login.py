#import requests 

from typing import Annotated
from fastapi import Form
from fastapi.datastructures import FormData
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm
import reflex as rx


from app_fyf_sag.componentes import routes
from app_fyf_sag.styles import utils
from app_fyf_sag.db import auth_users_db


class LoginState(rx.State):
    form_data_state: dict = []
    
    @rx.event
    async def submit(self, form_data: dict):
        print(form_data)
        form_data_state = Annotated(OAuth2PasswordRequestForm(form_data))
        form_data_state["username"] = form_data_state.get("username").upper() #pone en mayusculas el usuario
        print(form_data_state)
        #no funciona el envio, no deberia ser un dict, sino un form-data (no soy capaz de realizarlo)
        aut_dic = await auth_users_db.logindb(form_data_state)
        token_aut = aut_dic["access_token"]
        print (token_aut)
        if token_aut is None:
            rx.redirect(routes.Route.LOGIN.value)
        else:
            rx.redirect(routes.Route.SHEET.value)


@rx.page(
        route= routes.Route.LOGIN.value,
        title= utils.login_title,
        description= utils.login_description        
)
def login() -> rx.Component:
    return rx.flex(
    rx.vstack(
        rx.center(
            rx.card(
                rx.hstack(
                    rx.icon(tag="lock-keyhole", size = 40, color="green"),
                    rx.vstack(
                        rx.heading("Autentificación"),
                        rx.text(
                            "Acceso a la aplicación.", size="1"
                        ),
                        spacing="0",
                    ),   
                    margin = "1em",           
                ), 
                rx.form.root(
                    rx.vstack(
                        rx.text(
                            "Usuario ",
                            rx.text.span("*", color="red"),
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
                            rx.text.span("*", color="red"),
                        ),
                        rx.input(
                            name="password",
                            width = "100%",
                            type="password",
                            required=True,
                        ),
                        margin_y = "1em",  
                    ),  
                    rx.center(
                        rx.button(
                            "Enviar",
                            type="submit",
                            color_scheme= "grass"                                        
                        ),
                    ),
                    on_submit=LoginState.submit   
                ),
            ),
            padding = "50px 50px 50px 50px",
            bg="#1D2330",
            borderRadius="15px",
            boxShadow="41px -41px 82px #0D0F15, -41px 41px 82px #2D374B",
        ),

        #rx.hstack(
        #    rx.heading("Results:"),
        #    rx.badge(
        #        LoginState.form_data.to_string()
        #    ),
        # ),
    ),
    justify="center",
    padding="100px",
    height="100vh" 
    ),


