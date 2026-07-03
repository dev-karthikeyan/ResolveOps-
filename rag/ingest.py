from pathlib import Path

from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter

from rag.vectordb import VectorStore


class DocumentIngestor:
    

    def __init__(
        self,
        chunk_size: int = 1000,
        chunk_overlap: int = 200,
    ):
        self.vector_store = VectorStore()

        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )

    def load_document(self, file_path: str) -> Document:
        

        path = Path(file_path)

        text = path.read_text(encoding="utf-8")

        return Document(
            page_content=text,
            metadata={
                "source": path.name,
                "file_path": str(path),
            },
        )

    def chunk_document(self, document: Document):
        return self.text_splitter.split_documents([document])


    def add_metadata(self, chunks):
        for index, chunk in enumerate(chunks):
            chunk.metadata["chunk_id"] = index

        return chunks

    def ingest(self, file_path: str):

        document = self.load_document(file_path)

        chunks = self.chunk_document(document)

        chunks = self.add_metadata(chunks)

        self.vector_store.add_documents(chunks)
