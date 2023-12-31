"""ROBERT"""
from typing import Optional
import streamlit as st
import plotly.graph_objects as go


class BasePage:
    """
    This is the base page
    """

    @classmethod
    def render(cls) -> "BasePage":
        return cls()

    def load(self) -> None:
        """
        Hello world"""
        self.load_header()
        self.load_page()

    def load_page(self):
        st.warning("The Page is under construction...")

    def load_header(self):
        st.subheader(self.__class__.__name__)
        self.divider()

    def plotly(
        self,
        fig: go.Figure,
        title: Optional[str] = None,
        height: int = 300,
        hovermode: Optional[str] = None,
    ) -> None:
        fig.update_layout(
            # plot_bgcolor='rgba(0,0,0,0)',  # Set plot background color as transparent
            # paper_bgcolor='rgba(0,0,0,0)',  # Set paper background color as transparent
            # showlegend=False,  # Hide the legend for a cleaner border look
            # autosize=False,  # Disable autosizing to maintain border consistency
            # width=600,  # Set the width of the chart
            height=height,  # Set the height of the chart
            # margin=dict(l=20, r=20),  # Adjust the margins as needed
            # paper_bordercolor='black',  # Set the border color
            # paper_borderwidth=1  # Set the border width
            hovermode=hovermode,
            legend={
                "orientation": "h",
                "xanchor": "center",
                "x": 0.5,
                "y": -0.3,
                "font": {"size": 12},
            },
            margin={"t": 50, "l": 0, "r": 0, "b": 0},
        )
        if title:
            self.h3(text=title)
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

    @staticmethod
    def h3(text: str = "", align: str = "justify", decoration: str = "auto") -> None:
        st.markdown(
            f"<h3 style='text-align: {align}; font-size: 1.0em; text-decoration: {decoration};'>{text}</h3>",
            unsafe_allow_html=True,
        )

    @staticmethod
    def h4(text: str = "", align: str = "justify", decoration: str = "auto") -> None:
        st.markdown(
            f"<h4 style='text-align: {align}; font-size: 1.0em; text-decoration: {decoration};'>{text}</h4>",
            unsafe_allow_html=True,
        )

    @staticmethod
    def note(text: str = "", align: str = "justify", decoration: str = "auto") -> None:
        st.markdown(
            f"<div style='text-align: {align}; font-size: 1.0em; text-decoration: {decoration};'>{text}</div>",
            unsafe_allow_html=True,
        )

    @staticmethod
    def divider(margin_top: int = 0, margin_bottom: int = 5):
        st.markdown(
            f'<hr style="margin-top: {margin_top}px; margin-bottom: {margin_bottom}px;">',
            unsafe_allow_html=True,
        )
