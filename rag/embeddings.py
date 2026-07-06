from langchain_huggingface import HuggingFaceEmbeddings

class EmbeddingModel :
    
    def __init__(self , model_name = "BAAI/bge-small-en-v1.5") :

        self.model = HuggingFaceEmbeddings(
          
            model_name = model_name ,
            model_kwargs = {"device" : "cpu"} ,
            encode_kwargs={"normalize_embeddings": True})

    def embed_documents(self,documents : list[str]) :
        return self.model.embed_documents(documents)

    def embed_query(self,query : list[str]) :
        return self.model.embed_query(query)    
