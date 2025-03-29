import requests


class callLLM():
    def __init__(self, llmapi) -> None:

        self.llm_server = llmapi['url']
        self.llm_header = {
        "Content-Type": 'application/json',
        "Accept":'application/json',
        "Authorization": 'Bearer '+ llmapi['token']
        }
        self.modelname = llmapi['name']

    def init_prompt(self, sys_prompt, prompt):

        #print(sys_prompt,prompt)
        messages= [
            {"role": "system",  "content": sys_prompt},
            {"role": "user",    "content": prompt}
            ]
        
        self.llm_input = {
            "model": self.modelname,
            "messages": messages,
            "temperature": 0.1
        }

        return(self)
    
    def call(self):

        print('----calling llm: '+str(self.llm_input['model']))
        self.llm_response = requests.post(url = self.llm_server, 
                                          json = self.llm_input,   ### callLLM.llm_input_init(user_input)
                                          headers = self.llm_header).json()
        print('----llm response:\n', self.llm_response)

        return(self)


    def get_response_content(self):

        if 'choices' in self.llm_response:
            self.llmcontent = self.llm_response['choices'][0]['message']['content']
        else: 
            self.llmcontent = 'LLM Fail'
        #print('---- postprocess the llm response:\n'+str(self.llmcontent))

        return self.llmcontent


if __name__ == '__main__':

    llmapi = {'url': '', 
              'token': '', 
              'name': 'qwen2-7b-instruct-local'}
    
    #open router
    llmapi = {'url': 'https://openrouter.ai/api/v1/chat/completions', 
              'token': '', 
              'name': 'deepseek/deepseek-chat-v3-0324:free'}
    
    res = callLLM(llmapi).init_prompt('you are a text2sql assistant','who are you').call().get_response_content()
    print(type(res),len(res),res)



