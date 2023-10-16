"""ROBERT"""
import streamlit as st
from app.website.pages.base import BasePage
from app.database.client import get_glossaries


class Glossary(BasePage):
    def load_page(self):
        for glossary in get_glossaries():
            self.h4(glossary["code"])
            st.markdown(glossary.get("content"))
            self.divider()
