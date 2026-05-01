from src.data_ingestion import VectorStoreBuilder
from src.retrieval import AnimeRecommender
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException


class AnimeRecommendationPipeline:

    def __init__(self,persist_dir="chroma_db"):
        try:
            log.info("Intializing Recommdation Pipeline")

            vector_builder = VectorStoreBuilder(csv_path="" , persist_dir=persist_dir)

            retriever = vector_builder.load_vector_store().as_retriever()

            self.recommender = AnimeRecommender(retriever)

            log.info("Pipleine intialized sucesfully...")

        except Exception as e:
            log.error(f"Failed to intialize pipeline {str(e)}")
            raise CustomException("Error during pipeline intialization" , e)
        
    def recommend(self,query:str) -> str:
        try:
            log.info(f"Received a query {query}")

            recommendation = self.recommender.get_recommendation(query)

            log.info("Recommendation generated successfully...")
            return recommendation
        except Exception as e:
            log.error(f"Failed to get recommendation {str(e)}")
            raise CustomException("Error during getting recommendation" , e)