from typing import Any

import numpy as np

from rag.embeddings import embed_query


def retrieve_chunks(
    question: str,
    index,
    chunks: list[dict[str, Any]],
    top_k: int = 3,
    model_name: str = "all-MiniLM-L6-v2",
) -> list[dict[str, Any]]:
    """Retrieve the top-k most similar chunks for a question."""
    if top_k <= 0:
        raise ValueError("top_k must be greater than 0.")
    if index.ntotal == 0 or not chunks:
        return []

    query_vector = embed_query(question, model_name)
    scores, indices = index.search(
        np.asarray(query_vector, dtype="float32"),
        min(top_k, index.ntotal),
    )

    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx < 0:
            continue

        record = chunks[int(idx)]
        results.append({
            "text": record["text"],
            "metadata": record.get("metadata", {}),
            "score": float(score),
        })

    return results
