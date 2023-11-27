from typing import Optional

import feffery_antd_components as fac
from dash import html
from .sidebar import SideBar


def Title(
    children,
    level: int = 1,
    id: Optional[str] = None,
):
    kwargs = {
        "id": id,
        "level": level,
        "style": {
            "color": "white",
            "margin": "0",
        },
    }
    return fac.AntdTitle(children, **kwargs)


def Header(
    id: Optional[str] = None,
):
    kwargs = {
        "id": id,
        "style": {
            "display": "flex",
            "justifyContent": "center",
            "alignItems": "center",
        },
    }

    return fac.AntdPageHeader(**kwargs)


def AffixLeft(
    children,
    id: Optional[str] = None,
):
    kwargs = {
        "id": id,
        "offsetTop": 100,
        "style": {
            "height": "100%",
        },
    }
    return fac.AntdAffix(children=children, **kwargs)


def Icon(
    name: str,
    id: Optional[str] = None,
    fontSize: int = 14,
):
    kwargs = {
        "id": id,
        "icon": name,
        "style": {
            "fontSize": fontSize,
        },
    }
    return fac.AntdIcon(**kwargs)
