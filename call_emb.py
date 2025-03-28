import requests
from sentence_transformers import SentenceTransformer

class callm3e():
    def __init__(self,embapi) -> None:


        self.server = embapi['url']
        self.header = {
        "Content-Type": 'application/json',
        "Accept":'application/json',
        "Authorization": 'Bearer '+ embapi['token']
        }
        self.modelname = embapi['name']

    def init_prompt(self,  prompt):

        #print(sys_prompt,prompt)
        self.input = {
        "model": self.modelname,
        "input": prompt
        }

        return(self)
    
    def call(self):
        try:
            self.llm_response = requests.post(url = self.server, 
                                            json = self.input, 
                                            headers = self.header).json()
            vector = self.llm_response['data'][0]['embedding']
        except:
            vector = 'Emb Fail'

        return(vector)

def vectorize_localmodel(somestr):

    try:
        model = SentenceTransformer("./m3e-base")
        print("INFO: model loaded.")
        vector = list(model.encode(somestr, normalize_embeddings=True))
    
    except:
        vector = 'Emb Fail'

    return(vector)


if __name__ == '__main__':

    # api = {'url': 'http://10.29.253.101:19997/v1/embeddings', 
    #           'token': 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJhZG1pbiIsInNjb3BlcyI6WyJhZG1pbiJdLCJleHAiOjE3MjEyNzA0NDZ9.mT-Ky0xt_Dw1s2MhyzNuMkgl4dJe_eH3d2PZ7FXgKR8', 
    #           'name': 'm3e-base-local'}
    
    # res = callm3e(api).init_prompt('你是谁啊？').call()
    # print(type(res),res)

    res= vectorize_localmodel('hello')
    print(type(res),res)