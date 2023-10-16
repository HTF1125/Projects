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
