from pathlib import Path

import numpy as np
from sentence_transformers import SentenceTransformer


class ManualRAG:
    def __init__(self, documents: list[str]) -> None:
        self.documents = documents
        self.model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        self.embeddings = self.model.encode(documents, normalize_embeddings=True)

    def search(self, query: str, k: int = 3) -> list[tuple[str, float]]:
        query_embedding = self.model.encode([query], normalize_embeddings=True)[0]
        scores = self.embeddings @ query_embedding
        indices = np.argsort(scores)[::-1][:k]
        return [(self.documents[int(i)], float(scores[int(i)])) for i in indices]


if __name__ == "__main__":
    docs = [
        "Whitefield is a major technology corridor in Bengaluru.",
        "Silk Board is famous for heavy traffic and major bus routes.",
        "Binary search requires a sorted search space for the classic halving logic.",
    ]
    rag = ManualRAG(docs)
    for text, score in rag.search("Why is Whitefield associated with tech jobs?", k=2):
        print(round(score, 3), text)
