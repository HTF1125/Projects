from dash import html, dcc


class Footer:
    # style = {
    #     "position": "fixed",
    #     "bottom": 0,
    #     "width": "100%",
    #     "background-color": "white",
    #     "box-sizing": "border-box",
    #     "text-align": "center",
    #     "padding": "20px",
    #     "background-color": "#f4f4f4",
    #     "left": 0,
    #     "bottom": 0,
    # }

    @classmethod
    def layout(cls):
        return html.Div(
            style={
                "position": "relative",
                "min-height": "20vh",
                "width": "100%",
            },
            children=[
                html.Div(
                    children=[
                        html.H4("Welcome to My Dash App"),
                        html.P("This is the main content of the application."),
                    ],
                    style={
                        "padding-bottom": "2px"
                    },  # Adjust padding to reduce the space
                ),
                html.Div(
                    style={
                        "text-align": "center",
                        "padding": "10px",
                        "background-color": "#f4f4f4",
                        "position": "absolute",
                        "left": 0,
                        "bottom": 0,
                        "width": "100%",
                    },
                    children=[html.Footer("This is the footer")],
                ),
            ],
        )
