# """ROBERT"""
# import streamlit as st
# from website.pages.base import BasePage
# from website import hooks, components
# from robo.wm import strategy
# from robo.wm import universe
# from robo import get_prices


# class Strategy(BasePage):
#     def load_page(self):
#         with st.form("strategy.form"):
#             uni, por, fac = st.columns(3)
#             with uni:
#                 s_uni = components.select.s_universe()
#             with por:
#                 portfolio = components.select.s_portfolio()
#             with fac:
#                 factor = components.select.s_factor()
#             kwargs = components.kwargs()

#             submitted = st.form_submit_button(label="Backtest")
#             if submitted:
#                 px = get_prices(tickers=s_uni.ASSETS)
#                 with st.spinner(text="Backtesting in progress..."):
#                     stra = strategy.Strategy(
#                         assets_pxs=px,
#                         portfolio=portfolio,
#                         factor=factor,
#                         **kwargs,
#                     ).backtest()
#                 hooks.strategy.add(stra)

#         strategies = hooks.strategy.get()
#         if strategies:
#             start, end = components.get_date_range()

#             fig = hooks.strategy.fig()

#             for idx, plt in enumerate(fig.data):
#                 new_performance = strategies[idx].performance.loc[start:end].dropna()
#                 new_performance = new_performance / new_performance.iloc[0]
#                 fig.data[idx]["x"] = new_performance.index
#                 fig.data[idx]["y"] = new_performance.values

#             self.plotly(fig)

#             assert isinstance(strategies, list)
#             s_strategy = st.selectbox(
#                 label="Strategy",
#                 options=strategies,
#                 format_func=lambda x: x.name,
#             )
#             if s_strategy is not None:
#                 st.write(s_strategy.allocations)
