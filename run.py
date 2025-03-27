import pandas as pd


from call_llm import callLLM
from opDB import localsqlite

from user_input_process import user_input_init
from similarity_cal import search_qvec
from prompt_templates import Prompt_Fewshot, Prompt_Zeroshot, Prompt_Answer

def generate_sql(prompt, llm):

    res = callLLM(llm).init_prompt('You are a SQL query writer. You cannot do anything except write SQL',prompt).call().get_response_content()
    res = res.strip().replace('\n',' ').removeprefix('```sql').removesuffix('```')
    return res

def generate_ans(prompt, llm):

    res = callLLM(llm).init_prompt('You are a Text2SQL task assistant.',prompt).call().get_response_content()
    res = res.strip()
    return res


def adept(user_input, llm, emb, db):

    # user question process
    full_processed_input = user_input_init(user_input).full_process()

    # similarity check
    smlQS_not_exist, info, founddf = search_qvec(full_processed_input,emb)
    print('-----------SIMILAR QS PAIRS SEARCH---------------')
    print(founddf)
    print('------------------------------------------------')




    # compile prompt
    if smlQS_not_exist:
        prompt = Prompt_Zeroshot(full_processed_input).compile()
    else:
        prompt = Prompt_Fewshot(full_processed_input, founddf).compile()

    # gen SQL
    sql = generate_sql(prompt, llm)
    print(sql)
 
 
 
 
 
    # run SQL                
    dbconn = localsqlite(db['sqlite_path']).conn()
    try:
        resdf = dbconn.exesql(sql)
    except:
        resdf = pd.DataFrame()
    print('-----------SQL EXCUTION RES TABLE---------------')
    #remove dup cols
    duplicate_cols = resdf.columns[resdf.columns.duplicated()]
    resdf.drop(columns=duplicate_cols, inplace=True)
    print(resdf)
    print('------------------------------------------------')





    #compile prompt
    if smlQS_not_exist:
        search_res = 'No similar Question-SQL pair is found, you generted the SQL by yourself.'
    else:
        questions = ';'.join(list(founddf['question']))
        search_res = f'You found {founddf.shape[0]} Question-SQL pair. \
            The similar Questions are : {questions}. So, you imitated the SQLs of these questions.'
    
    taskinfos = {
        'question':full_processed_input.input,
        'search_res':search_res,
        'sql':sql,
        'sqlexe':resdf.head(3)
    }
    prompt = Prompt_Answer(taskinfos).complie()

    # gen answer
    answer = generate_ans(prompt, llm)
    print(answer)




    #return
    return({'answer':answer,
            'sql':sql,
            'table': resdf})






if __name__ == "__main__":
    llm = {
    "name":"qwen2-7b-instruct-local",
    "url":"http://10.29.253.101:19997/v1/chat/completions",
    "token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJleHAiOjE3MjEyNzA0NDZ9.mT-Ky0xt_Dw1s2MhyzNuMkgl4dJe_eH3d2PZ7FXgKR8"
    }
    emb = {"name":"m3e-base-local","url":"http://10.29.253.101:19997/v1/embeddings","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJleHAiOjE3MjEyNzA0NDZ9.mT-Ky0xt_Dw1s2MhyzNuMkgl4dJe_eH3d2PZ7FXgKR8"}
    db = {"option":"Turtorial DB","sqlite_path":"./sqlite/cre_Drama_Workshop_Groups.sqlite","db_name":"cre_Drama_Workshop_Groups.sqlite"}

    user_input = 'Did Blake book Adan Dinning?'
    adept(user_input, llm, emb, db)