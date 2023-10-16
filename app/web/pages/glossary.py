from dash import html, dcc


class Glossary:
    href = "/glossary"

    @classmethod
    def layout(cls):
        return (html.H1(__name__),)
