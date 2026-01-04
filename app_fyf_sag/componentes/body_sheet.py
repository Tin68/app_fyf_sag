import reflex as rx
import reflex_enterprise as rxe

from app_fyf_sag.db.client import db_client
from app_fyf_sag.db.models.sheet import Sheet
from localStoragePy import localStoragePy as ls

localStorage = ls('fyf', 'json')

class AGGridDatabaseState(rx.State):
    sheets: list[Sheet] 
    #lista_columns: list = []
    #aduana_columns: list = []
    #column_defs: list = lista_columns
    #hoja :str = str(localStorage.getItem("hoja"))

    # Fetch data from the database using a computed variable
    @rx.var
    def data(self) -> list[dict]:
        sheets = db_client.carpetas2025.find()
        for index in sheets:
            if not index.get("Aduana"):
                self.sheets.append(index)
        return self.sheets
    
    column_defs = [
        {"field": "Nº", "filter": True,  "sort" : "asc",},  #filtro otra linea "floatingFilter" : True,
        {"field": "Buque","filter": rxe.ag_grid.filters.text,},
        {"field": "Fecha Entrada", "filter": rxe.ag_grid.filters.date,},
        {"field": "TIP Carp","filter": rxe.ag_grid.filters.text,},
        {"field": "Consignatario","filter": rxe.ag_grid.filters.text,},
        {"field": "C/D","filter": rxe.ag_grid.filters.text,},
        {"field": "Doc","filter": rxe.ag_grid.filters.number,},
        {"field": "TIP Doc","filter": rxe.ag_grid.filters.text,},
        {"field": "Fecha Llegada", "filter": rxe.ag_grid.filters.date,},
        {"field": "Sol","filter": rxe.ag_grid.filters.number,},
        {"field": "Estibadora","filter": rxe.ag_grid.filters.text,},
        {"field": "Prov","filter": rxe.ag_grid.filters.number,},
        {"field": "Res Car","filter": rxe.ag_grid.filters.number,},
        {"field": "Dil","filter": rxe.ag_grid.filters.number,},
        {"field": "Fecha Partida", "filter": rxe.ag_grid.filters.date,},
        {"field": "Observaciones","filter": rxe.ag_grid.filters.text,},
        {"field": "TIP Aduana","filter": rxe.ag_grid.filters.text,},
        {"field": "Fecha Aduana", "filter": rxe.ag_grid.filters.date,},
    ]
    default_col_def = {"editable": False, "sortable":True, "gridOptions":True,"cellDataType" : False ,"floatingFilter" : True,}
    #sideBar = {"toolPanels": ["columns", "filters"] ,"defaultToolPanel": "columns",}
    autoSizeStrategy= {type: "fitCellContents"}

'''
    @rx.event
    def init_columns(self):
        self.lista_columns = [
            {"field": "Nº", "filter": True, "sortable" : True, "autosize":True},
            {"field": "Buque","filter": rxe.ag_grid.filters.text,},
            {"field": "Fecha Entrada", "filter": rxe.ag_grid.filters.date,},
            {"field": "TIP Carp","filter": rxe.ag_grid.filters.text,},
            {"field": "Consignatario","filter": rxe.ag_grid.filters.text,},
            {"field": "C/D","filter": rxe.ag_grid.filters.text,},
            {"field": "Doc","filter": rxe.ag_grid.filters.number,},
            {"field": "TIP Doc","filter": rxe.ag_grid.filters.text,},
            {"field": "Fecha Llegada", "filter": rxe.ag_grid.filters.date,},
            {"field": "Sol","filter": rxe.ag_grid.filters.number,},
            {"field": "Estibadora","filter": rxe.ag_grid.filters.text,},
            {"field": "Prov","filter": rxe.ag_grid.filters.number,},
            {"field": "Res Car","filter": rxe.ag_grid.filters.number,},
            {"field": "Dil","filter": rxe.ag_grid.filters.number,},
            {"field": "Fecha Partida", "filter": rxe.ag_grid.filters.date,},
            {"field": "Observaciones","filter": rxe.ag_grid.filters.text,},
            ]
        self.aduana_columns = [
            {"field": "Nº", "filter": True, "sortable" : True},
            {"field": "Buque","filter": rxe.ag_grid.filters.text,},
            {"field": "Fecha Entrada", "filter": rxe.ag_grid.filters.date,},
            {"field": "TIP Carp","filter": rxe.ag_grid.filters.text,},
            {"field": "Consignatario","filter": rxe.ag_grid.filters.text,},
            {"field": "C/D","filter": rxe.ag_grid.filters.text,},
            {"field": "Doc","filter": rxe.ag_grid.filters.number,},
            {"field": "TIP Doc","filter": rxe.ag_grid.filters.text,},
            {"field": "Fecha Llegada", "filter": rxe.ag_grid.filters.date,},
            {"field": "Sol","filter": rxe.ag_grid.filters.number,},
            {"field": "Estibadora","filter": rxe.ag_grid.filters.text,},
            {"field": "Prov","filter": rxe.ag_grid.filters.number,},
            {"field": "Res Car","filter": rxe.ag_grid.filters.number,},
            {"field": "Dil","filter": rxe.ag_grid.filters.number,},
            {"field": "Fecha Partida", "filter": rxe.ag_grid.filters.date,},
            {"field": "Observaciones","filter": rxe.ag_grid.filters.text,},
            {"field": "TIP Aduana","filter": rxe.ag_grid.filters.text,},
            {"field": "Fecha Aduana", "filter": rxe.ag_grid.filters.date,},
            ]
        self.column_defs = self.lista_columns


    @rx.event
    def update_columns(self):
        print("self.hoja")
        print(self.hoja)
        print(localStorage.getItem("hoja"))
        if self.hoja[0] == "Lista":
            self.column_defs = self.lista_columns
        else:
            self.column_defs = self.aduana_columns

def autoSizeAll(skipHeader) :
    allColumnIds: list = []
    rxe.ag_grid.api.getColumns().forEach((column) => {allColumnIds.push(column.getId())})

    rxe.ag_grid.api.autoSizeColumns(allColumnIds, skipHeader)
'''        


def ag_grid_api_sheet():
    my_api = rxe.ag_grid.api(
        id="ag_grid_basic_row_selection"
    )
    return rx.vstack(
        rx.flex(
            rxe.ag_grid(
                id="ag_grid_basic_row_selection",
                row_data=AGGridDatabaseState.data, 
                column_defs=AGGridDatabaseState.column_defs, #column_defs, 
                #on_mount=AGGridDatabaseState.init_def,    #update_columns, #
                row_selection="single",
                #paginacion
                pagination=True, 
                pagination_page_size=14,
                pagination_page_size_selector=[14, 50, 100],
                width="100%",
                height="85vh",
            ),
            width="100%",
            gridOptions = True,
        ),
        spacing="2",
        width="100%",
    )



def body_sheet() -> rx.Component:
    # Welcome Page (Index)
    return rx.vstack(
                ag_grid_api_sheet(),
                width="100%",
    )
