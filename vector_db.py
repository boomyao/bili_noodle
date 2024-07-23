from chromadb import PersistentClient as Client

client = Client(path='temp')

def get_or_create_collection(name: str):
    return client.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})