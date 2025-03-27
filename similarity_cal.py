
from user_input_process import user_input_init
from call_emb import callm3e
from typing import Type
from sklearn.metrics.pairwise import cosine_similarity

import pandas as pd
import numpy as np
import os
current_dir = os.getcwd()

def similarity(vec1,vec2):

    similarity = cosine_similarity(np.array(vec1).reshape(1, -1), 
                                   np.array(vec2).reshape(1, -1))
    return(similarity[0])

def search_qvec(full_processed_user_input:Type[user_input_init], emb):

    new_vec = callm3e(emb).init_prompt(full_processed_user_input.trans).call() #original question
    qvec_df = pd.read_csv(os.path.join('backend/qvec.csv'))

    found_df = pd.DataFrame(columns = ['question', 'sql', 'similarity'])
    
    for i in range(qvec_df.shape[0]):
        simlarity = similarity(new_vec, eval(qvec_df['qvec'][i]))

        if simlarity > 0.85:
            found_df = pd.concat([found_df, pd.DataFrame([{
                'question': qvec_df.iloc[i]['question'], 
                'sql':qvec_df.iloc[i]['sql'], 
                'similarity':simlarity
            }])], ignore_index=True)

    if found_df.shape[0]<1:
        return(True, 'No similar Questions',found_df)
    else:
        return(False, 'Similar Questions are found', found_df)


if __name__ == "__main__":

    emb = {"name":"m3e-base-local","url":"http://10.29.253.101:19997/v1/embeddings","token":"eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJleHAiOjE3MjEyNzA0NDZ9.mT-Ky0xt_Dw1s2MhyzNuMkgl4dJe_eH3d2PZ7FXgKR8"}

    from user_input_process import user_input_init

    input = '"Did Blake book Adan Dinning?"'
    input = user_input_init(input).full_process()
    

    not_found_flag, info, found_df = search_qvec(input, emb)
    print(not_found_flag, info, found_df)


