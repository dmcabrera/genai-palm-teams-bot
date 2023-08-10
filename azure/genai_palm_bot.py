import os

import vertexai
from vertexai.preview.language_models import TextGenerationModel
from infofin_tool import InfoFinTool

class GenAIPaLMBot(object):

    # Constructor
    def __init__(self):
        # Initialize the VertexAI client
        PROJECT_ID = os.environ['PROJECT_ID']
        LOCATION = "us-central1"
        MODEL_NAME = "text-bison@001"
        vertexai.init(project=PROJECT_ID, location=LOCATION)

        # Initialize the language model
        self.model = TextGenerationModel.from_pretrained(MODEL_NAME)

        # Initialize the InfoFinTool
        self.infofin_tool = InfoFinTool()

    # Format string
    def format_string(self, text):
        result = text.replace("\u00f3", "ó")
        result = result.replace("\u00e1", "á")
        result = result.replace("\u00ed", "í")
        return result

    # Chat
    def chat(self, message):

        # Busco en el Search Engine
        context, sources = self.infofin_tool.query(message)

        print(context)

        # Armo el prompt
        prompt = """Use the following pieces of context to answer the question at the end. 
If you don't know the answer, just say that you don't know, don't try to make up an answer. 
Keep the answer as concise as possible. 
Always answer in Spanish. 
{}
Question: {}
Helpful Answer:"""

        # Respondo la pregunta
        response = self.model.predict(
            prompt=prompt.format(context, message),
            temperature=0.2,
            max_output_tokens=1024,
            top_k=40,
            top_p=0.8,)
        
        answer = response.text.encode('utf-32', errors='backslashreplace').decode('utf-32', errors='ignore')
        print(answer)
        
        # Retorno la respuesta 
        return self.format_string(answer)