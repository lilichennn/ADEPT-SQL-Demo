import streamlit as st
from streamlit import session_state as ss
st.logo("logobar.png",icon_image= 'logonew.png', size = 'large')
st.set_page_config(layout="wide")
#
st.title('Welcome to ADEPT-SQL!👋')

st.markdown(
"""
*Welcome for trying out the DEMO version of ADEPT-SQL!*


**ADEPT-SQL is designed for High-Complexity Text2SQL tasks, and have been applied for multiple REAL-WORLD INDUSTRY databases.**
"""
)

st.divider()
st.header('How to Use')
st.markdown(
"""
1) Start with the **Settings** page, 
With the perfect **Settings**, ADEPT-SQL is able to achieve stunning results~


2) Before enter **StartChat**, make sure you get all these side-bar status:
"""
)

st.image("sidebar.png",
         )
st.markdown(
"""
3) Look into **Review**, to see infomations you need for asking questions.
"""
)

st.divider()

st.markdown(
"""
- Check out [Github](https://github.com/lilichennn/ADEPT-SQL)
"""
)
