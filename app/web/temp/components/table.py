from dash.dash_table import DataTable


class Table(DataTable):
    style_as_list_view = True
    style_cell = {
        "padding": "5px",
        "border": "1px solid grey",
        "textAlign": "center",
    }
    style_header = {
        "backgroundColor": "rgb(210, 210, 210)",
        "color": "black",
        "fontWeight": "bold",
        "border": "1px solid black",
        "textAlign": "center",
    }
    style_data = {
        "color": "black",
        "backgroundColor": "white",
        "textAlign": "center",
    }


import pandas as pd
import dash_ag_grid as dag


class AgTable:
    @classmethod
    def layout(cls, id: str, data: pd.DataFrame):
        return dag.AgGrid(
            id="cell-double-clicked-grid",
            rowData=data.to_dict("records"),
            columnDefs=[{"field": i} for i in data.columns],
            defaultColDef={
                "resizable": True,
                "sortable": True,
                "filter": True,
                "minWidth": 125,
            },
            columnSize="sizeToFit",
            getRowId="params.data.State",
        )
