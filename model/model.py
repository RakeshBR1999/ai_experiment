import os,getpass
import requests
import sys
from langchain.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from ibm_watson_machine_learning.foundation_models.utils.enums import ModelTypes
from ibm_watson_machine_learning.metanames import GenTextParamsMetaNames as GenParams
from ibm_watson_machine_learning.foundation_models.utils.enums import DecodingMethods
from ibm_watson_machine_learning.foundation_models import Model
from ibm_watson_machine_learning.foundation_models.extensions.langchain import WatsonxLLM
from langchain.chains import RetrievalQA
# import subprocess
# import chromadb
# Set your OpenAI API key here
# api_key = "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"

def doc_search(texts):
        print("inside docsearch")
        sys.setrecursionlimit(10000)
        embeddings = HuggingFaceEmbeddings()
        print("after embeddings")
        docsearch = Chroma.from_documents(texts, embeddings)
        return docsearch



class myGpt:

    def install_dependencies(self):
        pass

    def api_call(self):
        credentials = {
            "url": "https://us-south.ml.cloud.ibm.com",
            "apikey": getpass.getpass("Please enter your WML api key (hit enter): ")
        }
        try:
            project_id = os.environ["PROJECT_ID"]
        except KeyError:
            project_id = input("Please enter your project_id (hit enter): ")
        return credentials,project_id
 
    def document_read(self):
        print("inside document_read")
        # reading file from url
        filename = 'state_of_the_union.txt'
        url = 'https://raw.github.com/IBM/watson-machine-learning-samples/master/cloud/data/foundation_models/state_of_the_union.txt'

        response = requests.get(url)
        with open(filename, 'wb') as f:
            f.write(response.content)

        # semantic similarity
        loader = TextLoader(filename)
        documents = loader.load()
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        texts = text_splitter.split_documents(documents)
        print(len(texts))
        # print("after loader")
        # # creating embedding 
        # embeddings = HuggingFaceEmbeddings()
        # print("after embeddings")
        # docsearch = Chroma.from_documents(texts, embeddings)
        # print("docsearch",docsearch)
        return texts

    def model_setup(self,credentials,project_id):
        model_id = ModelTypes.FLAN_UL2
        print("inside model_setup")

        parameters = {
                GenParams.DECODING_METHOD: DecodingMethods.GREEDY,
                GenParams.MIN_NEW_TOKENS: 1,
                GenParams.MAX_NEW_TOKENS: 100
            }
        model = Model(
                model_id=model_id,
                params=parameters,
                credentials=credentials,
                project_id=project_id
            )
        return model

    def generate_response(self,model,user_input,docsearch):
        flan_ul2_llm = WatsonxLLM(model=model)
        print("inside generate_response, user input",user_input)

        qa = RetrievalQA.from_chain_type(llm=flan_ul2_llm, chain_type="stuff", retriever=docsearch.as_retriever())
        query = "What did the president say about Ketanji Brown Jackson"
        returnn = qa.run(user_input)
        print("return value",returnn)
        return returnn
        # openai.api_key = api_key
        # response = openai.Completion.create(
        #     engine="davinci",
        #     prompt=user_input,
        #     max_tokens=50,
        #     n=1,
        #     stop=None,
        #     temperature=0.7,
        # )
        # return response.choices[0].text

    def main(self,user_input):
        self.install_dependencies()
        credentials,project_id = self.api_call()
        texts = self.document_read()
        docsearch = doc_search(texts)
        model = self.model_setup(credentials,project_id)
        return self.generate_response(model,user_input,docsearch)
        

