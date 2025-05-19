import reflex as rx
import datetime
from app_fyf_sag.styles import style as style
from app_fyf_sag.pages import login

class CondState(rx.State):
    hoja: str = "Lista",
    anho: int = datetime.date.today().year,
    c_s_disable: bool = True
    which_dialog_open: str = ""

    def anho_m1(self):
        self.anho = datetime.date.today().year + 1

    def anho_(self):
        self.anho = datetime.date.today().year  

    def anho_1(self):
        self.anho = datetime.date.today().year - 1

    def lista(self):
        self.hoja = "Lista"
        self.c_s_disable = False

    def aduana(self):
        self.hoja = "Aduana"
        self.c_s_disable = True

    def documentos(self):
        self.hoja = "Documentos"   
        self.c_s_disable = False

    def cumplicdos(self):
        self.hoja = "Cumplidos"   
        self.c_s_disable = True

    def provisiones(self):
        self.hoja = "Provisiones" 
        self.c_s_disable = False

    def provCumplida(self):
        self.hoja = "ProvCumplida"  
        self.c_s_disable = True

    def open_a_aduana_dialog(self):
        self.which_dialog_open = "a_aduana"

def navbar() -> rx.Component:
    return rx.flex(
        rx.vstack(
            rx.hstack(
                rx.button(
                    "Log out",
                    color_scheme="green",
                    type="button",
                    border_radius = "1em", 
                    on_click= login.LoginState.do_logout,
                ),
                rx.spacer(),
                rx.button(
                    "Admin",
                    color_scheme="green",
                    border_radius = "1em", 
                    type="button",
                    on_click= print("Admin"),
                ),
                width="100%",
            ),
            rx.hstack(
                menu_hojas(),
                rx.cond(
                    (CondState.hoja == "Lista") | (CondState.hoja == "Aduana"),
                    rx.menu.root(
                        rx.menu.trigger(
                            rx.button("Panel Principal", style= style.menu_drop_style),
                        ), 
                        rx.menu.content( 
                            rx.menu.item("Entrada Carpeta",color_scheme = "green", disabled= CondState.c_s_disable), #, on_click=CondState.open_a_aduana_dialog), 
                            rx.menu.item("Llegada Buque",color_scheme = "green", disabled= CondState.c_s_disable),
                            rx.menu.item("Documentacion Carga",color_scheme = "green", disabled= CondState.c_s_disable),
                            rx.menu.item("Partida del Buque",color_scheme = "green", disabled= CondState.c_s_disable),
                            rx.menu.item("Resultado Carga/Descarga",color_scheme = "green", disabled= CondState.c_s_disable),
                            rx.menu.item("Diligenciar Carpeta",color_scheme = "green", disabled= CondState.c_s_disable),
                            rx.menu.item("Observaciones",color_scheme = "green", disabled= CondState.c_s_disable),
                            rx.menu.item("A la Aduana",color_scheme = "green", disabled= CondState.c_s_disable),
                            rx.menu.item("Busqueda",color_scheme = "green"),
                            rx.menu.item("Correccion de Errores",color_scheme = "green"),
                        ), 
                    ),
                    rx.cond(
                        (CondState.hoja == "Documentos") | (CondState.hoja == "Cumplidos"),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.button("Panel Principal", style= style.menu_drop_style),
                            ), 
                            rx.menu.content( 
                                rx.menu.item("Entrada Documento",color_scheme = "green", disabled= CondState.c_s_disable), 
                                rx.menu.item("Cumplir Documento",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Observaciones",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Carpeta --> Caseta",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Busqueda",color_scheme = "green"),
                                rx.menu.item("Correccion de Errores",color_scheme = "green"),
                            ) 
                        ),
                        rx.menu.root(
                            rx.menu.trigger(
                                rx.button("Panel Principal", style= style.menu_drop_style),
                            ), 
                            rx.menu.content( 
                                rx.menu.item("Entrada Correo",color_scheme = "green", disabled= CondState.c_s_disable), 
                                rx.menu.item("Correo Autorizacion",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Correo Realizacion",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Diligenciar",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Cumplir Provisiones",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Observaciones",color_scheme = "green", disabled= CondState.c_s_disable),
                                rx.menu.item("Busqueda",color_scheme = "green"),
                                rx.menu.item("Correccion de Errores",color_scheme = "green"),
                            ) 
                        ), 
                    ),
                ), 
                menu_anho(),                                                                                                                                     
            ),            
        ),       
        rx.spacer(),
        rx.hstack(
            rx.vstack(
                rx.spacer(),
                rx.cond(
                    (CondState.hoja == "Lista") | (CondState.hoja == "Aduana"),
                    rx.icon("folders", size= 36, color='green'),
                    rx.cond(
                        (CondState.hoja == "Documentos") | (CondState.hoja == "Cumplidos"),
                        rx.icon("file", size= 36, color='green'),
                        rx.cond(
                            (CondState.hoja == "Provisiones") | (CondState.hoja == "ProvCumplida"),
                            rx.icon("gift", size= 36, color='green'),
                            rx.icon("hourglass", size= 36, color='green'),
                        ),
                    ),
                ),
                rx.spacer(),
                padding_x="16px",
            ),
            rx.vstack(
                rx.center(                    
                    rx.heading("Destacamento FyF Sagunto",
                                size='6'),                   
                    rx.heading("Carpetas y Solicitos",
                                size='6'),
                    align="center",
                    justify="center",
                    direction="column"               
                ),
            ),
        ),
        rx.spacer(),
        rx.vstack(
            rx.text(f"© 1983 - {datetime.date.today().year} Tin Buccaneer Corp.", font_size= style.Spacer.MEDIUM.value),
            rx.spacer(),
            rx.hstack(
                rx.badge(
                    f"Hoja: {CondState.hoja}", variant="solid",
                    color_scheme="green",
                    aling="left"
                ),
                rx.spacer(),
                rx.badge(
                    f"Año: {CondState.anho}", variant="solid",
                    color_scheme="green",
                    aling="left"
                ),
                width="100%",
            ),
        ),  
        position="sticky",
        padding="16px",
        z_index="999",
        top = "0",
        width="100%",  
    )

def menu_hojas () -> rx.Component:
    return rx.menu.root(
                rx.menu.trigger(
                    rx.button("Hoja", style= style.menu_drop_style),
                ),                    
                rx.menu.content(                         
                    rx.menu.sub(
                        rx.menu.sub_trigger("Carpetas", style= style.menu_sub_trigger_style),
                        rx.menu.sub_content(
                            rx.menu.item("Lista", color_scheme = "green", on_select = CondState.lista),
                            rx.menu.item("Aduana", color_scheme = "green", on_select = CondState.aduana),                               
                        ),                         
                    ),                             
                    rx.menu.sub(
                        rx.menu.sub_trigger("Solicitos", style= style.menu_sub_trigger_style),
                        rx.menu.sub_content(
                            rx.menu.item("Documentos",color_scheme = "green" , on_select = CondState.documentos),
                            rx.menu.item("Cumplidos",color_scheme = "green" , on_select = CondState.cumplicdos),
                        ),
                    ),    
                    rx.menu.sub(
                        rx.menu.sub_trigger("Provisiones", style= style.menu_sub_trigger_style),
                        rx.menu.sub_content(
                            rx.menu.item("Provisiones",color_scheme = "green" , on_select = CondState.provisiones),
                            rx.menu.item("ProvCumplida",color_scheme = "green" , on_select = CondState.provCumplida),
                        ),
                    ),  
                    color_scheme = "green"              
                ),                        
            ),

def menu_anho ()-> rx.Component:
    return rx.menu.root(
        rx.menu.trigger(
            rx.button("Año", style= style.menu_drop_style),
        ), 
        rx.menu.content( 
            rx.menu.item("2024",color_scheme = "green",on_select = CondState.anho_1()),
            rx.menu.item("2025",color_scheme = "green",on_select = CondState.anho_()),
            rx.menu.item("2026",color_scheme = "green",on_select = CondState.anho_m1()),
        ) 
    ),