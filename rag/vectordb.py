from langchain_chroma import Chroma

from rag.embeddings import EmbeddingModel


class VectorStore:

    def __init__(
        self,
        collection_name: str = "resolveops",
        persist_directory: str = "./chroma_db",
    ):
        self.embedding_model = EmbeddingModel()

        self.db = Chroma(
            collection_name=collection_name,
            embedding_function=self.embedding_model.model,
            persist_directory=persist_directory,
    )

    def add_documents(self, documents):
        self.db.add_documents(documents)


    def similarity_search(self, query: str, k: int = 5):
        return self.db.similarity_search(query, k=k)

    def mmr_search(
        self,
        query: str,
        k: int = 5,
        fetch_k: int = 20,
    ):
       
        return self.db.max_marginal_relevance_search(
            query=query,
            k=k,
            fetch_k=fetch_k,
    )

    def delete_collection(self):
        self.db.delete_collection()