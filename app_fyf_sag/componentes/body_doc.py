import reflex as rx
import reflex_enterprise as rxe
import pandas as pd

#from ..componentes.navbar import navbar as navbar

df = pd.read_csv(
    "https://raw.githubusercontent.com/plotly/datasets/master/GanttChart-updated.csv"
)

column_defs = [
    {"field": "Nº", "filter": True},
    {"field": "T.I.P. Carp.","filter": rxe.ag_grid.filters.text,},
    {"field": "Fecha Entrada", "filter": rxe.ag_grid.filters.date,},
    {"field": "Entidad Solicita","filter": rxe.ag_grid.filters.text,},
    {"field": "Nº Registro","filter": rxe.ag_grid.filters.text,},
    {"field": "Fecha Documento", "filter": rxe.ag_grid.filters.date,},
    {"field": "Motivo","filter": rxe.ag_grid.filters.text,},
    {"field": "Observaciones","filter": rxe.ag_grid.filters.text,},
    {"field": "Carp.","filter": rxe.ag_grid.filters.number,},
    {"field": "Guar.Conf.","filter": rxe.ag_grid.filters.text,},
    {"field": "T.I.P. Grab.","filter": rxe.ag_grid.filters.text,},
    {"field": "T.I.P. Cumpl.","filter": rxe.ag_grid.filters.text,},
    {"field": "Fecha Cumplido", "filter": rxe.ag_grid.filters.date,},            
]
default_col_def = {"editable": False}


def ag_grid_api_doc():
    my_api = rxe.ag_grid.api(
        id="ag_grid_basic_row_selection"
    )
    return rx.vstack(
        rx.flex(
            rxe.ag_grid(
                id="ag_grid_basic_row_selection",
                row_data=df.to_dict("records"),
                column_defs=column_defs,
                row_selection="single",
                #paginacion
                pagination=True, 
                pagination_page_size=16,
                pagination_page_size_selector=[16, 50, 100],
                width="100%",
                height="85vh",
            ),
            width="100%",
        ),
        spacing="2",
        width="100%",
    )



def body_doc() -> rx.Component:
    # Welcome Page (Index)
    return rx.vstack(
                ag_grid_api_doc(),
                width="100%",
    )