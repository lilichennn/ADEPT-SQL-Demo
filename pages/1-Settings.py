import os,sys
pythonon_path = os.path.dirname('../')
sys.path.append(pythonon_path)

from call_llm import callLLM
from call_emb import callm3e, vectorize_localmodel
from opDB import localsqlite

import streamlit as st
from streamlit import session_state as ss
import pandas as pd
import json

def writejson(ssdict,file):
    json_object = json.dumps(ssdict, indent=4)
    with open("./backend/"+file, "w") as outfile:
        outfile.write(json_object)

def readjson(file):
    with open("./backend/"+file, 'r') as openfile:
        json_object = json.load(openfile)
    return(json_object)
#################### PAGE START ######################
st.title("Define your Assistant ~")
st.logo("logobar.png",icon_image= 'logonew.png', size = 'large')


# side bar setting
if st.sidebar.button('Check Status'):
    llm = readjson('llm.json')
    st.sidebar.checkbox("LLM Connected 🥳", value=llm['active']) 
    st.sidebar.write(llm)

    emb = readjson('emb.json')
    st.sidebar.checkbox("EMB Connected 🥳", value=emb['active']) 
    st.sidebar.write(emb)

    userdb = readjson('db.json')
    st.sidebar.checkbox("DB Connected 🥳", value=userdb['conn'])
    st.sidebar.write(userdb)


tabllm, tabdb, tabsql = st.tabs(['LLM', 'DataSource', 'Your SQLs'])


###################### llm TAB #######################

with tabllm:

    st.header('Large Language Model')
    
    if "llm" not in ss : 
        ss.llm = {}
        ss.llm['active'] = False

    ss.llm['name'] = st.text_input("Model Name", value='')
    ss.llm['url'] = st.text_input("URL", value='')
    ss.llm['token'] = st.text_input("API Key", value='')
    #ss.llm['active'] = False

    if st.button("Connect", icon=":material/mood:"):

        if ss.llm['name'] != '' and ss.llm['url'] != '' and ss.llm['token'] != '':

            res = callLLM(ss.llm).init_prompt('When user ask who are you, answer:You are a Text2SQL expert. You respond cannot exceed 20 words.', 'Who are you?').call().get_response_content()

            if res == 'LLM Fail':
                st.error("Connection FAIL, please check the form")
                ss.llm['active'] = False
            else:
                #st.success("Connection success!")
                st.write("✅ Connection success!")
                ss.llm['active'] = True
                writejson(ss.llm, 'llm.json')
                st.markdown(f''' 
                            🫠： Who are you?

                            😼： {res}
                            ''')
                
        else:
            st.error("Connection FAIL, please check the form")
            ss.llm['active'] = False
        
    st.divider()

    st.header('Embedding Model')

    if "emb" not in ss : 
        ss.emb = {}
        ss.emb['active'] = False
    ss.emb['name'] = st.text_input("Model Name",key='emb1', value='local model')
    ss.emb['url'] = st.text_input("URL",key='emb2', value='local model')
    ss.emb['token'] = st.text_input("API Key",key='emb3', value='local model')
    #ss.llm['active'] = False

    if st.button("Connect", icon=":material/mood:", key='butforemb'):

        if ss.emb['name'] != '' and ss.emb['url'] != '' and ss.emb['token'] != '':

            if ss.emb['name'] != 'local model':

                res = callm3e(ss.emb).init_prompt('TestText').call()  ###### why no para?????
            else:
                res = vectorize_localmodel('TestText')

            if res == 'Emb Fail':
                st.error("Connection FAIL, please check the form")
                ss.emb['active'] = False
            else:
                st.success("Connection success!")
                ss.emb['active'] = True
                writejson(ss.emb, 'emb.json')
                st.markdown(f'''
                            ------------------------
                            TEST RESPONSE

                            - Test Text
                            
                            - The embedded vector length is : {len(res)}
                            ''')
                
        else:
            st.error("Connection FAIL, please check the form")
            ss.emb['active'] = False

################### DataSource Tab ##################
# Connect to Local SQLite

    
def dataframe_with_selections(df):
    df_with_selections = df.copy()
    df_with_selections.insert(0, "Select", False)

    # Get dataframe row-selections from user with st.data_editor
    edited_df = st.data_editor(
        df_with_selections,
        hide_index=True,
        width=1000,
        height=400,
        column_config={"Select": st.column_config.CheckboxColumn(required=True)},
        disabled=('Table'),
    )

    # Filter the dataframe using the temporary column, then drop the column
    selected_rows = edited_df[edited_df.Select]
    return selected_rows.drop('Select', axis=1)

with tabdb:
    # DB信息填写表单
    if 'userdb' not in ss or ss.userdb['conn'] == False:
        ss.userdb = {}
        ss.userdb['option'] = st.pills(
            "Database Type",
            options=['MySQL', 'Sqlite', 'Turtorial DB'],
            default='Turtorial DB',
            selection_mode="single",
            )
        if ss.userdb['option'] == 'MySQL':
            ss.userdb['ip'] = st.text_input("IP")
            ss.userdb['port'] = st.text_input("Port")
            ss.userdb['user_name']= st.text_input("User name")
            ss.userdb['user_password'] = st.text_input("Password")
            ss.userdb['db_name'] = st.text_input("Database")
            ss.userdb['conn'] = False

        if ss.userdb['option'] == 'Sqlite':
            ss.userdb['sqlite_path'] = st.text_input("Database Location")
            ss.userdb['db_name'] = ss.userdb['sqlite_path'].split('/')[-1]
            ss.userdb['conn'] = False

        if ss.userdb['option'] == 'Turtorial DB':
            ss.userdb['sqlite_path'] = "./sqlite/cre_Drama_Workshop_Groups.sqlite"
            ss.userdb['db_name'] = ss.userdb['sqlite_path'].split('/')[-1]
            ss.userdb['conn'] = False


    # 连接DB / 显示链接信息
    if not ss.userdb['conn']:
        if st.button("Connect"):
            try:
                db = localsqlite(ss.userdb['sqlite_path']).conn()
                ss.userdb['conn'] = True
                writejson(ss.userdb, 'db.json')
                pass
            except Exception as e:
                st.write(f"Connection failed: {e}")
    else:
        st.markdown(f'''                     
            - Database Type:  {ss.userdb['option']}

            - Database Name:  {ss.userdb['db_name']}''')    
        if st.button("Reconnect"):
            del st.session_state['userdb']
            st.rerun()


    st.divider()

    # DB信息写入session_state -》 可根据需求添加
    if ss.userdb['conn']:

        ss.dbconn = localsqlite(ss.userdb['sqlite_path']).conn()

        ss.alltables = list(ss.dbconn.metadata.tables.keys())
        ss.alltablesdf = pd.DataFrame(
            {"Table":ss.alltables#,  "Description":[" "] * len(ss.alltables)
             } )

        ss.alltable_cols = {'Table':[], 'Column':[]#, 'Description':[]
                            }
        for table in ss.alltables:
            columns = ss.dbconn.metadata.tables[table].columns.keys()
            for i in range(len(columns)):
                ss.alltable_cols['Table'].append(table)
                ss.alltable_cols['Column'].append(list(columns)[i]) 
                #ss.alltable_cols['Description'].append('')
        ss.alltable_colsdf = pd.DataFrame(ss.alltable_cols)

        #st.write(ss.alltable_colsdf)

    #复选table 
    if 'selected_table_colsdf' not in ss:
        ss.selected_table_colsdf = pd.DataFrame(columns = ['Table','Table Description','Column','Columns Description'])

    if ss.userdb['conn']:

        col4table, col4col = st.columns(2)

        with col4table:
            st.subheader("Choose Tables")
            ss.tableselection = dataframe_with_selections(ss.alltablesdf)
            ss.selectedtables = list(ss.tableselection['Table'])

        with col4col:

            newtable = None 
            if len(ss.selectedtables) == 1:
                newtable = ss.selectedtables[0]
            elif len(ss.selectedtables) > 1:
                newtable = ss.selectedtables[-1]


            if newtable:
                st.subheader('Columns of "'+ newtable+'"')
            else:
                st.subheader("Choose Columns")
            ss.colselection = dataframe_with_selections(ss.alltable_colsdf[ss.alltable_colsdf['Table'] == newtable][['Column']])


        ss.selected_table_colsdf = pd.concat([ss.selected_table_colsdf,
                                                pd.DataFrame({
                                                    'Table':[newtable]*len(ss.colselection),
                                                    'Table Description':['']*len(ss.colselection),
                                                    'Column':list(ss.colselection['Column']),
                                                    'Column Description':['']*len(ss.colselection)
                                                    })
                                                ]
                                            ).drop_duplicates()
                
        st.subheader("Check Descriptions")

        df_summary = ss.selected_table_colsdf.copy().reset_index()
        df_summary.insert(0,"As Terminology", False)
        edited_df = st.data_editor(
            df_summary[['As Terminology','Table','Table Description','Column','Column Description']],
            hide_index=True,
            width=2000,
            height=300,
            column_config={"As Terminology": st.column_config.CheckboxColumn(required=True, width='small',help="By selecting, the values from the (Table.column) will be stored for question recognization"),
                           "Table Description": st.column_config.Column(width="large", help="Fill one line for the same Table"),
                           "Column Description": st.column_config.Column(width="large")
                           },
            disabled=('Table','Column'),
            num_rows='dynamic'
        )
        selected_df = edited_df[edited_df['As Terminology']][['Table','Column']]

        if st.button('Save'):

            ## db meta 
            dbmeta = edited_df[['Table','Table Description','Column','Column Description']]
            dbmeta.to_csv('./backend/dbmata.csv')

            ## term list
            termlistdf = pd.DataFrame(columns = [ 'table', 'field', 'term'])
            for i in range(selected_df.shape[0]):
                
                table = selected_df.iloc[i]['Table']
                col = selected_df.iloc[i]['Column']
                sql = f"SELECT {col} FROM {table}"
                coldf = ss.dbconn.exesql(sql)
                print(coldf)
                coltermset = set(list(coldf[col]))
                for term in coltermset:
                    termlistdf = pd.concat([termlistdf,
                                        pd.DataFrame({
                                            'table': [table],
                                            'field': [col],
                                            'term': [term]
                                        })], ignore_index= True)
            #termlistdf = termlistdf.dropna()
            termlistdf.to_csv('./backend/term.csv')

            st.success(f'{termlistdf.shape[0]} records Saved!')


###################### sql TAB ##################
with tabsql:
    from user_input_process import user_input_init
    st.header("Add a QS pair")

    if "qa_pairs" not in ss:
        ss.qa_pairs = pd.DataFrame(columns=["Question",'Masked Question', "SQL"])

    Qstr = st.text_input("Enter the Question", key="q")
    Astr = st.text_area("Enter the SQL", key="a")

    if Qstr != '' and Astr !='':
        Qmask = user_input_init(Qstr).full_process().trans
        if st.button("Add"):
            if Qmask not in set(ss.qa_pairs['Masked Question']):
                ss.qa_pairs = pd.concat([ss.qa_pairs, pd.DataFrame({"Question": [Qstr],
                                                                    "Masked Question": [Qmask],
                                                                    "SQL": [Astr]})])
            else:
                st.error('Question MUST be a NEW one!')

    st.header("Check and Save your QS pairs")
    qa_df = ss.qa_pairs.copy().reset_index()
    edited_df = st.data_editor(
        qa_df[['Question',"Masked Question",'SQL']],
        hide_index=True,
        width=2000,
        height=300,
        num_rows='dynamic'
    )
    if st.button('Save', key='qssave'):

        if ss.emb['name'] != 'local model':
            embmodel = callm3e(ss.emb)
        else:
            embmodel = 'localmodel'

        qs_df = edited_df.dropna()
        qs_df_4csv = pd.DataFrame(columns = ['question','qmask','qvec','sql'])

        for i in range(qs_df.shape[0]):
            q = qs_df.iloc[i]['Question']
            qmask = qs_df.iloc[i]['Masked Question']
            sql = qs_df.iloc[i]['SQL']
            if embmodel != 'localmodel':
                qvec = embmodel.init_prompt(qmask).call()
            else: 
                qvec = vectorize_localmodel(qmask)

            qs_df_4csv = pd.concat([qs_df_4csv,
                                    pd.DataFrame({
                                        'question': [q],
                                        'qmask':[qmask],
                                        'qvec': [str(qvec)],
                                        'sql': [sql]
                                    })], ignore_index= True)
            qs_df_4csv.to_csv('./backend/qvec.csv')

        st.success('Data Saved!')


