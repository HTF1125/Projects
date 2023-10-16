from dash import html


class FlexRight(html.Div):
    style = {
        "display": "flex",
        "justify-content": "flex-end",
    }


class HorizontalBox(html.Div):
    style = {
        "display": "flex",
        "justify-content": "space-between",
        "align-items": "center",
        "padding": "10px 20px",
    }


class VerticalBox(html.Div):
    style = {
        "display": "flex",
        "flex-direction": "column",
        "justify-content": "space-between",
        "align-items": "center",
        "height": "100%",
    }


class Button(html.Button):
    style = {
        "background-color": "blue",
        "color": "white",
        "border": "none",
        "padding": "10px 20px",
        "border-radius": "5px",
        "cursor": "pointer",
        "font-size": "14px",
    }


class RightSideButton:
    @classmethod
    def layout(cls, **kwargs):
        return html.Div(
            style={"display": "flex", "justify-content": "flex-end"},
            children=html.Button(
                **kwargs,
                style={
                    "background-color": "white",
                    "cursor": "pointer",
                },
            ),
        )


class Card(html.Div):
    style = {
        "border": "1px solid #ccc",
        "border-radius": "5px",
        "padding": "20px",
        "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
    }


class LightCard(html.Div):
    style = {
        "border": "1px solid #ccc",
        "border-radius": "5px",
        "padding": "20px",
        "box-shadow": "0 2px 4px rgba(0, 0, 0, 0.05)",
        "width": "100%",
    }


class Container(html.Div):
    style = {
        "display": "block",
        "margin": "2px, 0px",
        "position": "relative",
        "width": "calc(100% - 2px)",
        "height": "auto",
        "border-radius": "2px",
        "trasition": "box-shadow .2s ease",
    }


class Row(html.Div):
    style = {"width": "100%"}
