from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_chroma import Chroma
from langchain_community.document_loaders.csv_loader import CSVLoader
from langchain_huggingface import HuggingFaceEmbeddings
from exception.custom_exception import CustomException
from logger import GLOBAL_LOGGER as log
import os
import chromadb
from utils.model_loader import ModelLoader
from dotenv import load_dotenv
load_dotenv()

class VectorStoreBuilder:
    def __init__(self,csv_path:str,persist_dir:str="chroma_db"):
        self.csv_path = csv_path
        self.persist_dir = persist_dir
        self.embedding = self._load_embeddings()
    
    def _load_embeddings(self):
        try:
            embedding = ModelLoader().load_embeddings()
            if not embedding:
                raise CustomException("No embedding model loaded")
            log.info("Embedding model loaded successfully")
            return embedding
        except Exception as e:
            log.error(f"Failed to load embeddings {str(e)}")
            raise CustomException("Error during loading embeddings" , e)

    def build_and_save_vectorstore(self):
        try:
            log.info("Building and saving vector store")
            loader = CSVLoader(
                file_path=self.csv_path,
                encoding='utf-8',
                metadata_columns=[]
            )

            data = loader.load()

            log.info(f"Loaded {len(data)} documents from CSV")
            text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
            texts = text_splitter.split_documents(data)

            log.info(f"Split documents into {len(texts)} chunks")

            vector_store = Chroma(
                collection_name='example_collection',
                embedding_function=self.embedding,
                persist_directory=self.persist_dir
            )

            log.info("Adding documents to vector store")

            vector_store.add_documents(texts)
        except Exception as e:
            log.error(f"Failed to build and save vector store {str(e)}")
            raise CustomException("Error during building and saving vector store" , e)

    def load_vector_store(self):
        client = chromadb.PersistentClient(path=self.persist_dir)
        return Chroma(
            client=client,
            collection_name="example_collection",
            embedding_function=self.embedding
        )


    def get_retriever(self):
        vector_store = self.load_vector_store()
        return vector_store.as_retriever()

