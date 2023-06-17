import openai

class Embeddings:
    def __init__(self, model="text-embedding-ada-002"):
        self.model = model
        
    def get_embedding(self, text):
        return openai.Embedding.create(input = [text], model=self.model)['data'][0]['embedding']