import pytest
from pyramem.datastore.chroma import ChromaDatastore

@pytest.fixture
def store():
    s = ChromaDatastore(namespace="UNIT_TEST_CHROMA")
    yield s
    s.reset()

def test_chromadatastore(store):
    # assert that there is no matching result for vector [0]*1536 before insertion
    assert store.query([0]*1536, top_k=1000) == {'ids': [[]], 'embeddings': None, 'documents': [[]], 'metadatas': [[]], 'distances': [[]]}

    # insert a document with id "test", vector [0]*1536 and text "hello world"
    assert store.upsertOne("test", [0]*1536, "hello world") == True

    # assert that there is a matching result for vector [0]*1536 after insertion
    assert store.query([0]*1536, top_k=1000) == {'ids': [['test']], 'embeddings': None, 'documents': [['hello world']], 'metadatas': [[None]], 'distances': [[0.0]]}

    # delete the document with id "test"
    store.delete("test")

    # assert that there is no matching result for vector [0]*1536 after deletion
    assert store.query([0]*1536, top_k=1000) == {'ids': [[]], 'embeddings': None, 'documents': [[]], 'metadatas': [[]], 'distances': [[]]}
