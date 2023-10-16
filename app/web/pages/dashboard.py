from dash import html, dcc


class Dashboard:
    href = "/"

    @classmethod
    def layout(cls):
        return html.H1(__name__),


