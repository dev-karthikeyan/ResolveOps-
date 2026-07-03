from rag.vectordb import VectorStore


class Retriever:
   
    def __init__(self):
        self.vector_store = VectorStore()

    def retrieve(
        self,
        query: str,
        k: int = 5,
        search_type: str = "mmr",
    ):
       

        if search_type == "similarity":
            return self.vector_store.similarity_search(
                query=query,
                k=k,
            )

        elif search_type == "mmr":
            return self.vector_store.mmr_search(
                query=query,
                k=k,
            )

        else:
            raise ValueError(
                f"Unsupported search type: {search_type}"
            )