from dash import html
import feffery_antd_components as fac
import feffery_utils_components as fuc


def Reloader():
    return fac.AntdSpin(
        html.Div(
            id="docs-content-spin-center",
            style={"position": "fixed"},
        ),  # 强制脱离文档流
        indicator=fuc.FefferyExtraSpinner(
            type="guard",
            color="#1890ff",
            style={
                "position": "fixed",
                "top": "50%",
                "left": "50%",
                "width": 100,
                "height": 100,
                "transform": "translate(-50%, -50%)",
                "zIndex": 999,
            },
        ),
    )
