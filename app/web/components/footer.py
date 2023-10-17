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
                # "min-height": "20vh",
                "width": "100%",
            },
            children=[
                html.Div(
                    children=[
                        html.Hr(),
                        html.H5("Welcome to RobertDashboard"),
                        html.P("This is the main content of the application."),
                    ],
                    style={
                        "padding": "2px, 20px"
                    },  # Adjust padding to reduce the space
                ),
                html.Div(
                    style={
                        "text-align": "center",
                        "background-color": "#f4f4f4",
                        "position": "absolute",
                        "left": 0,
                        "bottom": 0,
                        "width": "100%",
                    },
                    children=[html.Footer("Robert")],
                ),
            ],
        )
