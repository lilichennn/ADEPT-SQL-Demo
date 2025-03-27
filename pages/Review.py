import os,sys
pythonon_path = os.path.dirname('../')
sys.path.append(pythonon_path)

import streamlit as st
from streamlit import session_state as ss
import pandas as pd

st.title('Review Your Settings~')

st.logo("logo.png", size = 'large')

st.header('Database Meta')
df = pd.read_csv('./backend/dbmata.csv', index_col=0)
st.data_editor(df,use_container_width  = True, hide_index = True,disabled = True)

st.header('Question-SQL')
df = pd.read_csv('./backend/qvec.csv', index_col=0)
st.data_editor(df,use_container_width  = True, hide_index = True,disabled = True)


st.header('Terminologies')
df = pd.read_csv('./backend/term.csv', index_col=0)
st.data_editor(df,use_container_width  = True, hide_index = True,disabled = True)