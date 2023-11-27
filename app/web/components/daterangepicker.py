from typing import Optional
from datetime import date
from dash import callback, Input, Output
import feffery_antd_components as fac


def DateRangePicker(**kwargs):
    params = {
        "value": ["2023-01-01", date.today()],
        "autoFocus": True,
        "locale": "en-us",
    }
    params.update(kwargs)
    return fac.AntdDateRangePicker(**params)
