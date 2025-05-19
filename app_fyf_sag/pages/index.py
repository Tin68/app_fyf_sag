import reflex as rx

from app_fyf_sag.componentes import routes
from app_fyf_sag.styles import utils

class State(rx.State):
    """The app state."""

    ...


#esto funciona
@rx.page(
        route= routes.Route.INDEX.value,
        title = utils.index_title,
        description = utils.index_description        
)  
def index() -> rx.Component:
    # Welcome Page (Index)
    return rx.fragment( 
        rx.color_mode.button(position="top-right"),
        rx.vstack(
            rx.heading("Bienvenido a la pagina Web!", font_size="2em"),
            rx.link(
                    "Pagina Protegida, Autentifiquese",
                    color_scheme="grass",
                    href =routes.Route.SHEET.value
                    ),
            spacing="2",
            padding_top = "10%",
            align="center",
        )
    )


