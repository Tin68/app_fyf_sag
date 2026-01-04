#import requests 
import reflex as rx
import jwt
from app_fyf_sag.componentes import routes
from app_fyf_sag.styles import utils
from app_fyf_sag.db import auth_users_db
from localStoragePy import localStoragePy as ls

localStorage = ls('fyf', 'json')
ALGORITHM = utils.login_algorithm
SECRET = utils.login_secret

class LoginState(rx.State):
    form_data_state: dict = []
    redirect_to: str = ""
    token_aut: str = ""
    token_refr: str = ""

    rx.event
    async def submit(self, form_data: dict):      
        form_data["username"] = form_data.get("username").upper() #pone en mayusculas el usuario
        form_data_state = form_data
        aut_dic = await auth_users_db.logindb(form_data_state)
        self.token_aut = aut_dic["acc_token"]["access_token"]
        self.token_refr = aut_dic["ref_token"]["refresh_token"]
        print("login")
        print(self.token_aut)
        print(self.token_refr)
        rol = jwt.decode(self.token_aut, SECRET, algorithms= [ALGORITHM]).get("rol")
        localStorage.setItem("rol",rol)
        print(rol)
        sub = jwt.decode(self.token_aut, SECRET, algorithms= [ALGORITHM]).get("sub")
        localStorage.setItem("sub",sub)
        print(sub)
        exp_token = jwt.decode(self.token_aut, SECRET, algorithms= [ALGORITHM]).get("exp")
        localStorage.setItem("exp",exp_token)
        print(exp_token)
        exp_ref_token = jwt.decode(self.token_refr, SECRET, algorithms= [ALGORITHM]).get("exp")
        localStorage.setItem("exp",exp_ref_token)
        print(exp_ref_token)
        if self.token_aut is None:
            return rx.redirect(routes.Route.LOGIN.value)
        else:
            return rx.redirect(routes.Route.SHEET.value)
        
    def redir(self) -> rx.event.EventSpec | None:
        #Redirect to the redirect_to route if logged in, or to the login page if not.
        if not self.is_hydrated:
            # wait until after hydration to ensure auth_token is known
            return LoginState.redir()  # type: ignore
        page = self.router.page.path
        if self.token_aut == "" and page != routes.Route.LOGIN.value:
        #if not self.is_authenticated and page != routes.Route.LOGIN.value:
            self.redirect_to = self.router.page.raw_path
            return rx.redirect(routes.Route.LOGIN.value)
        #elif self.is_authenticated and page == routes.Route.LOGIN.value:
        elif self.token_aut != "" and page == routes.Route.LOGIN.value:
            return rx.redirect(self.redirect_to or "/")    

    @rx.event
    async def do_logout(self):
        """Destroy LocalAuthSessions associated with the auth_token."""
        self.token_aut = ""
        self.token_refr =""
        localStorage.clear()
        yield rx.redirect(routes.Route.INDEX.value)    

def require_login(page: rx.app.ComponentCallable) -> rx.app.ComponentCallable:
    """Decorator to require authentication before rendering a page.
    If the user is not authenticated, then redirect to the login page.
    Args:
        page: The page to wrap.
    Returns:
        The wrapped page component.
    """

    def protected_page():
        return rx.fragment(
            rx.cond(
                True,
                #LoginState.is_hydrated & LoginState.token_aut!="",
                #State.is_hydrated & State.is_authenticated,  # type: ignore
                page(),
                rx.center(
                    # When this spinner mounts, it will redirect to the login page
                    rx.spinner(on_mount=LoginState.redir),
                ),
            )
        )

    protected_page.__name__ = page.__name__
    return protected_page

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
                            color_scheme= "grass",                                       
                        ),
                    ),
                    on_submit=LoginState.submit,   
                    reset_on_submit=True,
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



