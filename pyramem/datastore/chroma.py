import chromadb
from .base import AbstractDatastore

class ChromaDatastore(AbstractDatastore):
    def __init__(self, namespace="default"):
        self.client = chromadb.Client()
        self.namespace = namespace
        self.collection = self.client.get_or_create_collection(name=namespace)
    
    def upsertOne(self, vector_id: str, vector: list[float], text: str, metadata=None):        
        kwargs = {
            'embeddings': [vector],
            'documents': [text],
            'ids': [vector_id]
        }
        if metadata:
            kwargs['metadata'] = [metadata]
        
        self.collection.add(**kwargs)
        return True
    
    def query(self, vector, top_k=10, include_values=False, include_metadata=True):
        kwargs = {
            'query_embeddings': [vector],
            'n_results': top_k,
            'include': ["distances", "documents"]
        }
        if include_values:
            kwargs['include'].append("embeddings")
        if include_metadata:
            kwargs['include'].append("metadatas")
        
        results = self.collection.query(**kwargs)
        return results
    
    def delete(self, id):
        self.collection.delete(ids=[id])
        return True
        
    def persist(self):
        self.client.persist()
    
    def reset(self):
        self.client.reset()