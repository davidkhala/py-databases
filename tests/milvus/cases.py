from pymilvus import MilvusClient, model
def create_collection(client:MilvusClient):
    if client.has_collection(collection_name="demo_collection"):
        client.drop_collection(collection_name="demo_collection")
    client.create_collection(
        collection_name="demo_collection",
        dimension=768,  # The vectors we will use in this demo has 768 dimensions
    )
def prepare_data():
    embedding_fn = model.DefaultEmbeddingFunction()  # small embedding model "paraphrase-albert-small-v2"
    docs = [
        "Artificial intelligence was founded as an academic discipline in 1956.",
        "Alan Turing was the first person to conduct substantial research in AI.",
        "Born in Maida Vale, London, Turing was raised in southern England.",
    ]

    vectors = embedding_fn.encode_documents(docs)

    print("Dim:", embedding_fn.dim, vectors[0].shape)  # dimensions: 768

    # Each entity has id, vector representation, raw text, and a subject label
    data = [
        {"id": i, "vector": vectors[i], "text": docs[i], "subject": "history"}
        for i in range(len(vectors))
    ]

    print("Data has", len(data), "entities, each with fields: ", data[0].keys())
    print("Vector dim:", len(data[0]["vector"]))