



import streamlit as st




import app





@st.cache_data()
def get_chart():
    uni = app.api.get_universe(code="GlobalAllo")
    uni.f.append(app.api.factor.UsCli3Y)
    return uni.f.plot()



st.plotly_chart(get_chart())