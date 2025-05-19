import reflex as rx
import reflex_enterprise as rxe
from app_fyf_sag.componentes.navbar import CondState as cd
from app_fyf_sag.componentes.body_sheet import body_sheet
from app_fyf_sag.componentes.body_doc import body_doc
from app_fyf_sag.componentes.body_pro import body_pro
#from app_fyf_sag.views.header import header
from app_fyf_sag.styles import utils
from app_fyf_sag.componentes import routes as routes
from app_fyf_sag.componentes.navbar import navbar
import app_fyf_sag.pages.login as log
#from app_fyf_sag.pages.login import require_login


@rx.page(
        route= routes.Route.SHEET.value,
        title=utils.sheet_title,
        description= utils.sheet_description
)
@log.require_login
def sheet() -> rx.Component:
    # Welcome Page (Index)
    return rx.vstack(
        utils.lang(),
        navbar(),
        rx.cond(
            (cd.hoja == "Lista") | (cd.hoja == "Aduana"),
            body_sheet(),
            rx.cond(
                (cd.hoja == "Documentos") | (cd.hoja == "Cumplidos"),
                body_doc(),
                body_pro(),
            )
        ) 
        #header(),
    )