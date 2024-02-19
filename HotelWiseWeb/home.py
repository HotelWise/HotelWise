from htbuilder.funcs import rgba, rgb
from htbuilder.units import percent, px
from htbuilder import HtmlElement, div, ul, li, br, hr, a, p, img, styles, classes, fonts
import streamlit as st
import pandas as pd
from views.navbar import page_navbar
from views.footer import page_footer

logo = "_src/HotelWiseLogo.Horizontal.png"
st.set_page_config(
    layout="wide",
    initial_sidebar_state="collapsed",
    page_title='HotelWise - HOME',
    page_icon="_src/HotelWiseLogo.Icon.png",)
st.set_option('deprecation.showPyplotGlobalUse', False)

hide_streamlit_style = """
<style>
    MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>

"""
st.markdown(hide_streamlit_style, unsafe_allow_html=True)
left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image(logo, use_column_width=True)

page_navbar()

page_bg_img = f"""
    <style>
        [data-testid="stAppViewContainer"] > .main 
        {{
            background-image: url("https://i.postimg.cc/4xgNnkfX/Untitled-design.png");
            background-size: cover;
            background-position: center center;
            background-repeat: no-repeat;
            background-attachment: local;
        }}
        [data-testid="stHeader"]
        {{
            background: rgba(0,0,0,0);
        }}
    </style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

left_co, cent_co, last_co = st.columns(3)
with cent_co:
    st.image(logo, use_column_width=True)

st.image("_src/HotelWiseLogo.Horizontal.png")


st.image('_src/HotelWiseLogo.Horizontal.Fondo.png')

page_footer()

st.info(
    '© 2024 Copyright: HotelWise ([Project GitHub](https://github.com/jgutierrezladino/HotelWise))')
