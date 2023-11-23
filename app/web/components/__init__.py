from .layout import *
from .navbar import *
from .footer import *
from .button import *
from .table import *

import time

import dash_mantine_components as dmc
from dash import html, Output, Input, no_update, callback, State
from dash_iconify import DashIconify
from app.api import factor

def log_in():
    return html.Div(
        style={"width": 200},
        children=dmc.LoadingOverlay(
            dmc.Stack(
                id="loading-form",
                children=[
                    dmc.TextInput(
                        label="Username",
                        placeholder="Your username",
                        id="user-login-username",
                        icon=DashIconify(icon="radix-icons:person"),
                    ),
                    dmc.PasswordInput(
                        label="Your password:",
                        id="user-login-password",
                        placeholder="Your password",
                        icon=DashIconify(icon="bi:shield-lock"),
                    ),
                    dmc.Checkbox(
                        label="Remember me",
                        checked=True,
                        id="user-login-remember",
                    ),
                    dmc.Button(
                        "Login",
                        id="user-login-button",
                        variant="outline",
                        fullWidth=True,
                    ),
                ],
            )
        ),
    )


@callback(
    Output("loading-form", "children"),
    Output("status", "data"),
    Input("user-login-button", "n_clicks"),
    State("user-login-username", "value"),
    State("user-login-password", "value"),
    State("status", "data"),
    prevent_initial_call=True,
)
def func(n_clicks, username: str, password: str, data):
    print(data)
    if data:
        return (html.Div("you are logged in."),)
    if username == "admin" and password == "admin":
        data = True
        return (html.Div("you are logged in."), data)
    # return no_update


from app.api import Universe


def get_universe():
    data = list(Universe.UNIVERSE.keys())
    return dmc.Select(
        label="Investment Universe",
        data=data,
        id="user-universe",
        value=data[0],
        persistence=True,
    )
def get_factor():
    data = list(factor.__all__)
    return dmc.Select(
        label="Investment Factor",
        data=data,
        id="user-factor",
        value=data[0],
        persistence=True,
    )

def get_periods():
    return dmc.NumberInput(
        label="Investment Horizon (Day)",
        id="user-periods",
        value=5,
        min=0,
        max=250,
        step=5,
        persistence=True,
    )


def get_commission():
    return dmc.NumberInput(
        label="Trade Commission (bps)",
        id="user-commission",
        value=10,
        min=0,
        max=100,
        step=2,
        persistence=True,
    )


def get_factor_args():
    style = {
        "margin-top": 0,
        "margin-bottom": 10,
        "display": "flex",
        "justify-content": "center",
        "align-items": "center",
    }

    return dmc.Group(
        style=style,
        children=[
            get_universe(),
            # get_periods(),
            get_factor(),
        ],
    )
