import faiss
import numpy as np

def create_vector_store(embeddings):
    vectors = np.array(
        np.array(),
        dtype="float32"
    )

    dimension = vectors.shape()

    index = faiss.IndexFlatL2(dimension)
    index.add(vectors)

    return index
