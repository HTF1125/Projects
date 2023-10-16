"""ROBERT"""
from app.website import pages, state
from app.website import components


def launch():
    components.loadLogger()
    components.loadStatic()
    components.loadNavbar()
    getattr(pages, state.Webpage.get())().load()
