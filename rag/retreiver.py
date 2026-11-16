import numpy as np
def retreive_chunks(question, model, index, chunks, k=3):
    query_embedding = model.encode([question])

    query_embedding = np.array(
        query_embedding,
        dtype = "float32"
    )

    distances, indices = index.search(
        query_embedding,
        k
    )

    return [
        chunks[i]
        for i in indices[0]
        if i >= 0
    ]
