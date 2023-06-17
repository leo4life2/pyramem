import os
import pinecone
from .base import AbstractDatastore

class PineconeDatastore(AbstractDatastore):
    def __init__(self, namespace="default"):
        self.namespace = namespace
        pinecone.init(
            api_key=os.environ.get("PINECONE_API_KEY"),
            environment=os.environ.get("PINECONE_ENVIRONMENT")
        )
            
        self.index = pinecone.Index(os.environ.get("PINECONE_INDEX"))
    
    def upsertOne(self, vector_id: str, vector: list[float], text: str, metadata=None):
        vector = {
            'id': vector_id,
            'values': vector,
            }
        
        if metadata:
            metadata['text'] = text
            vector['metadata'] = metadata
        else:
            vector['metadata'] = {
                'text': text
            }
        
        response = self.index.upsert(
            vectors=[
                vector
            ],
            namespace=self.namespace
        )
        
        return response.get('upsertedCount') is not None and response.get('upsertedCount') == 1
        
    
    def query(self, vector, top_k=10, include_values=False, include_metadata=True, filter_obj=None):
        kwargs = {
            'namespace': self.namespace,
            'top_k': top_k,
            'include_values': include_values,
            'include_metadata': include_metadata,
            'vector': vector
        }
        
        if filter_obj:
            kwargs['filter'] = filter_obj
        
        query_response = self.index.query(**kwargs)
        return query_response
    
    def delete(self, namespace, key):
        response = self.index.delete(
            ids=[key],
            namespace=namespace
        )
        
        # response should be an empty dict if successful
        return response == {}
        