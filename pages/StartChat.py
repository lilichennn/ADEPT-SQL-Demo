import os,sys
pythonon_path = os.path.dirname('../')
sys.path.append(pythonon_path)
import json
import pandas as pd
import streamlit as st
from streamlit import session_state as ss

from run import adept

def readjson(file):
    with open("./backend/"+file, 'r') as openfile:
        json_object = json.load(openfile)
    return(json_object)
#################### PAGE START ######################
st.set_page_config(layout="wide")
st.logo("logo.png", size = 'large')


# side bar setting
if st.sidebar.button('Check Status'):
    ss.llm = readjson('llm.json')
    st.sidebar.checkbox("LLM Connected 🥳", value=ss.llm['active']) 
    st.sidebar.write(ss.llm)

    ss.emb = readjson('emb.json')
    st.sidebar.checkbox("EMB Connected 🥳", value=ss.emb['active']) 
    st.sidebar.write(ss.emb)

    ss.userdb = readjson('db.json')
    st.sidebar.checkbox("DB Connected 🥳", value=ss.userdb['conn'])
    st.sidebar.write(ss.userdb)



st.title('Now, Chat with you Database!')


user_input = st.chat_input("Say something")
if user_input:
    input_blk = st.chat_message("user",avatar="🫠")
    input_blk.write(user_input)

    #### 这里写完就结束!!!!!
    out = adept(user_input, ss.llm, ss.emb,  ss.userdb)

    output_blk = st.chat_message("assistant",avatar="😼")
    output_blk.write(out['answer'])
    output_blk.code(out['sql'],wrap_lines  = True)
    output_blk.dataframe(out['table'].T.drop_duplicates().T)
#Did Blake book Adan Dinning?