"""Welcome to Reflex! This file outlines the steps to create a basic app."""

import reflex as rx
from app_fyf_sag.pages import index
from app_fyf_sag.pages import login
from app_fyf_sag.pages import sheet
from app_fyf_sag.db import auth_users_db #user_db, auth_users, 
from fastapi import FastAPI
import reflex_enterprise as rxe

from rxconfig import config

class State(rx.State):
    """The app state."""

    ...


#app = rxe.App()
#app = rx.App()


#probar esto ¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡¡funciona!!!!!!!!!!!!!!!!!!
fastapi_app = FastAPI()

#app = rx.App(api_transformer=fastapi_app)
app = rxe.App(api_transformer=fastapi_app)
#fastapi_app.include_router(auth_users.auth_router)
fastapi_app.include_router(auth_users_db.auth_db_router)
#fastapi_app.include_router(user_db.items_router)


#app.include_router(user_db.items_router)

#rx.heading("Hola to Reflex!", size="9"),
