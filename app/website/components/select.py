# """ROBERT"""
# from typing import Type
# import streamlit as st
# from robo.wm import portfolio
# from robo.wm import factor
# from robo.wm import universe


# def s_portfolio() -> Type[portfolio.Portfolio]:
#     out = str(st.selectbox(label="Portfolio", options=portfolio.__all__))
#     out = getattr(portfolio, out)
#     if not issubclass(out, portfolio.Portfolio):
#         raise ValueError()
#     return out

# def s_factor() -> Type[factor.Factor]:
#     out = str(st.selectbox(label="factor", options=factor.__all__))
#     out = getattr(factor, out)
#     if not issubclass(out, factor.Factor):
#         raise ValueError()
#     return out

# def s_universe() -> Type[universe.Universe]:
#     out = str(st.selectbox(label="universe", options=universe.__all__))
#     out = getattr(universe, out)
#     if not issubclass(out, universe.Universe):
#         raise ValueError()
#     return out

import streamlit as st
