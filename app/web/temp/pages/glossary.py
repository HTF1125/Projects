from dash import html, dcc

from .dashboard import Page


class Glossary(Page):
    href = "/glossary"
    icon = "antd-read"

    @classmethod
    def layout(cls):
        return (html.H1(__name__),)
