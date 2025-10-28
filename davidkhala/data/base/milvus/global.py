from pymilvus import Collection

def drop_index(collection:Collection, index_name:str):
    collection.release()
    collection.drop_index(index_name=index_name)
