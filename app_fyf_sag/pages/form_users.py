import random
import re
import bcrypt
import reflex as rx

from app_fyf_sag.componentes import routes
from app_fyf_sag.styles import utils
from app_fyf_sag.db.models.user import User
from app_fyf_sag.db.client import db_client
from app_fyf_sag.db import user_db

PATTERN = "^[A-Z][0-9]{5}[A-Z]$"

class SelectState2(rx.State):
    form_data: dict = [] 
    values: list [str] =[]
    value_list: list [User] = []
    value: str = ""
    name_form: str = ""
    user_form: str = ""
    disabled_form: bool = False
    rol_form: str = "user"
    form_disable: bool = True
    icon_control: str = "1"

    @rx.var
    def invalid_username(self) -> bool:
        return not re.match(r"^[a-zA-Z][0-9]{5}[a-zA-Z]$", self.user_form) #suer_entered_usuario

    @rx.var
    def surname_empty(self) -> bool:
        #return not self.user_form.strip() # user_entered_name
        return not self.name_form.strip()
    
    @rx.var
    def surname_is_taken(self) -> bool:  
            return (self.name_form in self.values)    

    @rx.var
    def input_invalid(self) -> bool:
        if self.icon_control == "23":
            return True
        else:
            return (
                self.invalid_username
                or self.surname_is_taken
                or self.surname_empty
            )
    
    def reset_submit(self) -> bool:
        if self.icon_control.find("1") != -1:
            return True
        else:
            return False 
        
    @rx.event
    async def refresh_users(self): 
        self.values = []     
        self.value_list = []     

        users = db_client.users.find()
        for user_find in users:
            self.value_list.append(user_find)
            self.values.append(user_find.get("surname"))               
        self.values.append("****") 

    def set_users_change(self):
        if self.value == "****":
            self.icon_control = "1" 
            self.name_form= ""
            self.user_form= ""
            self.disabled_form= False
            self.rol_form= "user"
            self.form_disable=True
        else:    
            for user in self.value_list:
                if user.get("surname") == self.value:
                    self.name_form= user.get("surname") + " "
                    self.user_form= user.get("username")
                    self.disabled_form= user.get("disabled")
                    self.rol_form= user.get("rol")
            self.icon_control = "23"        

    def on_change_user_form (self):       
        self.user_form = self.user_form.upper()

    def on_change_name_form (self):
        self.name_form = self.name_form.title()    

    def edit_user(self):
        self.form_disable = False
        self.icon_control = "3" 

    def add_user(self):
        self.form_disable = False

    async def delete_user(self, username_form):
        indice = -1
        for user in self.value_list:
                indice += 1
                if user.get("username") == username_form:
                    id= user.get("_id")
                    break
        await user_db.delete_user(id)
        yield rx.toast.success("Borrado satisfactoriamente", duration=5000)
        yield SelectState2.refresh_users()
        del self.values[indice]
        del self.value_list[indice]        
        self.name_form= ""
        self.user_form= ""
        self.disabled_form= False
        self.rol_form= "user"
        self.form_disable=True    
        self.icon_control = "1"       

    @rx.event
    async def submit(self, form_data: dict):   
        self.form_data = form_data
        x =form_data.keys()
        reset = False
        desabilitado = False
        for keys in x:
            if keys == "check":
                if form_data["check"] == "on":
                    reset = True   
            if keys == "switch":
                if form_data["switch"] == "on":
                    desabilitado = True
        #surname = form_data["surname"]
        if not self.icon_control.find("1") != -1:            
            surname = form_data["surname"][0:len(form_data["surname"])-1] #por el espacio añadido para no ser duplicado
        else:    
            surname = form_data["surname"]
        username = form_data["username"]
        rol = form_data["select"]
        if self.icon_control.find("3") != -1:            
            replace_user: dict = {}
            for user in self.value_list:
                if user.get("username") == username:
                    id= str(user.get("_id"))
                    break
            replace_user.update({"id": id})
            replace_user.update({"username": username})
            replace_user.update({"surname": surname})
            replace_user.update({"rol": rol})
            replace_user.update({"disabled": desabilitado})
            if reset:
                bytes = username.encode('utf-8') 
                salt = bcrypt.gensalt() 
                result_psw = bcrypt.hashpw(bytes, salt).decode('utf-8')#lo convierte en str
            else:
                #pasword antiguo
                for user in self.value_list:
                    if user.get("surname") == surname:
                        result_psw = user.get("password")
            replace_user.update({"password": result_psw})           
            await user_db.replace_user(replace_user)
            yield rx.toast.success("Actualizado satisfactoriamente", duration=5000)
            self.icon_control = "23" 
            self.form_disable=True 
        else:
            bytes = username.encode('utf-8') 
            salt = bcrypt.gensalt() 
            result = bcrypt.hashpw(bytes, salt).decode('utf-8')#lo convierte en str
            password = result
            add_user: dict = {}
            add_user.update({"id": "1"})
            add_user.update({"username": username})
            add_user.update({"surname": surname})
            add_user.update({"rol": rol})
            add_user.update({"disabled": desabilitado})
            add_user.update({"password": password})
            await user_db.add_user(add_user)
            yield SelectState2.refresh_users() 
            yield rx.toast.success("Añadido satisfactoriamente", duration=5000)
            self.icon_control = "23" 
            self.name_form = self.name_form + " "
            self.form_disable = True 
            self.value = surname

    @rx.event
    async def cancel(self):   
        self.value = ""        
        self.icon_control = "1" 
        self.name_form= ""
        self.user_form= ""
        self.disabled_form= False
        self.rol_form= "user"
        self.form_disable=True

    @rx.event
    def choose_randomly(self):
        """Change the select value var."""
        original_value = self.value
        while self.value == original_value:
            self.value = random.choice(self.values)

@rx.page(
        route= routes.Route.FORMUSERS.value,
        title= utils.formusers_title,
        description= utils.formusers_description,
        on_load=SelectState2.refresh_users()        
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