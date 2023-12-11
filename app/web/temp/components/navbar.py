from dash import html
from app.web import pages


class Nav(html.Nav):
    style = {
        "background-color": "#f8f9fa",
        "padding": "10px",
        "text-align": "center",
        "font-family": "Arial, sans-serif",
    }


class Link(html.A):
    style = {
        "margin": "10px",
        "text-decoration": "none",
        "color": "black",
        "font-size": "18px",
        "font-family": "Arial, sans-serif",
    }


class Navbar(html.Div):
    @classmethod
    def layout(cls):
        return cls(
            children=[
                Nav(
                    children=[
                        Link(
                            children=page.__name__,
                            href=page.href,
                        )
                        for page in pages.all_pages
                    ],
                    className="navbar",
                )
            ]
        )

