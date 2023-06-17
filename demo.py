# from pyramem import HierarchicalMemory

# # Create a new HierarchicalMemory object
# mem = HierarchicalMemory(namespace="pyramemTest")
# mem.add_memory("hello world")

from pyramem.datastore.chroma import ChromaDatastore

store = ChromaDatastore(namespace="pyramemTest")

print(store.query([0]*1536, top_k=1000))

store.upsertOne("test", [0]*1536, "hello world")

print(store.query([0]*1536, top_k=1000))