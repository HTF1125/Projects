"""





"""


from dash import html, dcc, callback, Output, Input, State, no_update
import feffery_antd_components as fac
from app.api import factors
from .. import components
from .base import Page


class Factors(Page):
    menu = {
        "component": "Item",
        "props": {
            "key": "/Factors",
            "name": "/Factors",
            "title": "Factors",
            "href": "/Factors",
            "icon": "antd-dot-chart",
        },
    }

    def layout(self):
        return html.Div(
            children=[
                dcc.Store(id="cache", data={}),
                html.H1("Factor Analysis"),
                html.Div(
                    children=[
                        fac.AntdRow(
                            children=[
                                self.get_universe(),
                                self.get_factor(),
                            ],
                            style={
                                "margin-top": 0,
                                "margin-bottom": 10,
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                        html.Div(
                            fac.AntdButton("Test Factors", id="user-factor-test"),
                            style={
                                "display": "flex",
                                "justify-content": "center",
                                "align-items": "center",
                            },
                        ),
                    ],
                ),
                html.Div(
                    children=[
                        components.Info(
                            dcc.Markdown(
                                children="""
**Universe:**
The Universe module is specifically curated with major ETFs, simplifying your focus on essential assets.

- **GlobalAllo:**
  - SPY, AGG, TLT, TIP, GSG, GLD, TIP, IVV

- **UsSectors:**
  - XLC, XLY, XLK, and YOU KNOW WHATS NEXT.

**Factors:**
Given the constraints of data availability, our Factors predominantly encompass momentum, ensuring an intuitive and actionable analysis.

**Running the Module:**
Upon hitting 'run', the generated graph provides insights into the average expected forward performance on a daily basis. This projection extends over three distinct investment horizons: 1, 5, and 10 trading days.

**Additional Information:**
The notation `(q=5, za=0)` signifies the use of quantiles (in this case, 5) and a non-zero-aware approach when processing factor data.

                                """
                            )
                        ),
                        dcc.Loading(
                            children=html.Div(
                                id="factor-chart",
                                style={
                                    "min-height": 500,
                                    "min-width": 1000,
                                },
                            ),
                            type="circle",
                        ),
                    ],
                    style={
                        "margin-bottom": 20,
                    },
                ),
                html.Div(id="factor-performance-table"),
                html.Div(id="factor-performance-stats"),
            ]
        )


@callback(
    Output("factor-chart", "children"),
    Input("user-factor-test", "nClicks"),
    State("user-universe", "value"),
    State("user-factor", "value"),
    prevent_initial_call=True,
)
def handle_chart(nClicks, universe, factor):
    if nClicks:
        factor_ins = getattr(factors, factor)
        if issubclass(factor_ins, factors.Factor):
            return [
                fac.AntdCenter(html.H3(f"{factor} Performance")),
                fac.AntdCenter(
                    dcc.Graph(
                        figure=factor_ins.create(universe).plot(),
                        config={"displayModeBar": False},
                    ),
                ),
            ]
    return no_update
