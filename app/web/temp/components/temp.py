

from typing import Optional, Dict,
import feffery_antd_components as fac



def Select(
    options: Dict,
    placeholder: Optional[str] = None,
    
)

def Select(
    options: typing.Dict,
    placeholder:
    id: typing.Optional[str] = None,
    value: typing.Optional[str] = None,
    persistence: bool = True,
    style: typing.Dict = {},
):





    return fac.AntdSelect(
        options=[
            {
                "label": f"选项{i}",
                "value": f"选项{i}",
            }
            for i in range(1, 6)
        ],
        style={"width": 200},
        autoFocus=True,
        persistence=persistence,
    )
