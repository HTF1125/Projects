import feffery_antd_components as fac


def Info(*args, **kwargs):
    return fac.AntdCollapse(
        isOpen=False,
        title="Info",
        *args,
        **kwargs,
    )
