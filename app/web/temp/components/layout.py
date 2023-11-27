from dash import html


class GlobalLayout(html.Div):
    style = {
        "width": "100%",
        "height": "100%",
        "box-sizing": "border-box",
        "font-family": "Calibri, sans-serif",
    }


class MainLayout(html.Div):
    style = {
        "position": "relative",
        "max-width": "960px",
        "min-height" : "500px",
        "margin": "0 auto",
        "padding": "0 20px",
        "@media (min-width: 400px)": {
            "width": "85%",
            "padding": "0",
        },
        "@media (min-width: 550px)": {
            "width": "80%",
        },
    }
