from dash import Dash, dcc, html
from dash import callback, Output, Input
from app.web import pages, components

import logging

logger = logging.getLogger("app.web")
logging.captureWarnings(capture=True)
formatter = logging.Formatter("%(asctime)s %(levelname)s %(name)s %(message)s")
streamhandler = logging.StreamHandler()
streamhandler.setFormatter(formatter)
streamhandler.setLevel(logging.DEBUG)
logger.addHandler(streamhandler)
logger.setLevel(logging.DEBUG)
logger.info("initialize streamlit webpage.")


app = Dash(
    name=__name__,
    title="RobertDashboard",
    suppress_callback_exceptions=True,
)


@callback(
    Output("page", "children"),
    Input("url", "pathname"),
)
def display(pathname: str):
    for page in pages.all_pages:
        if page.href == pathname:
            return page.layout()
    raise


app.layout = components.GlobalLayout(
    children=[
        dcc.Store(id="store"),
        dcc.Location(id="url", refresh=False),
        components.Navbar.layout(),
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
