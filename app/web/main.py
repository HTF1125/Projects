from dash import Dash, dcc
from dash import callback, Output, Input
from app.web import pages, components
from dash_iconify import DashIconify
import dash_mantine_components as dmc


app = Dash(
    name=__name__,
    title="RobertDashboard",
    suppress_callback_exceptions=True,
)

server = app.server


@callback(
    Output("page", "children"),
    Input("url", "pathname"),
)
def display(pathname: str):
    for page in pages.all_pages:
        if page.href == pathname:
            return page.layout()
    raise


app.layout = dmc.MantineProvider(
    theme={
        "fontFamily": "'Inter', sans-serif",
        "primaryColor": "indigo",
        "components": {
            "Button": {"styles": {"root": {"fontWeight": 400}}},
            "Alert": {"styles": {"title": {"fontWeight": 500}}},
            "AvatarGroup": {"styles": {"truncated": {"fontWeight": 500}}},
        },
    },
    inherit=True,
    withGlobalStyles=True,
    withNormalizeCSS=True,
    children=[
        dcc.Store(id="store"),
        dcc.Location(id="url", refresh=False),
        components.Navbar.layout(),
        DashIconify(icon="ion:logo-github", width=30, rotate=0, flip="horizontal"),
        components.MainLayout(id="page"),
        components.Footer.layout(),
    ],
)


app.clientside_callback(
    """
    function(trigger) {
        //  can use any prop to trigger this callback - we just want to store the info on startup
        const inner_width  = window.innerWidth || document.documentElement.clientWidth || document.body.clientWidth;
        const inner_height = window.innerHeight|| document.documentElement.clientHeight|| document.body.clientHeight;
        const screenInfo = {height :screen.height, width: screen.width, in_width: inner_width, in_height: inner_height};
        return screenInfo
    }
    """,
    Output("store", "data"),
    Input("store", "data"),
)
