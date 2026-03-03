from src.data_loader import AnimeDataLoader
from src.vector_store import VectorStoreBuilder
from dotenv import load_dotenv
from utils.logger import get_logger
from utils.custom_exception import CustomException
from src.recommender import AnimeRecommender
import os
from config.config import MODEL_NAME

load_dotenv()

logger = get_logger(__name__)

def main():
    try:
        logger.info("Starting to build pipeline...")

        loader = AnimeDataLoader("data/anime_with_synopsis.csv" , "data/anime_updated.csv")
        processed_csv = loader.load_and_process()

        logger.info("Data  loaded and processed...")

        vector_builder = VectorStoreBuilder(processed_csv)
        vector_builder.build_and_save_vectorstore()

        logger.info("Vector store Built sucesfully....")

        recommender = AnimeRecommender(vector_builder.get_retriever(),os.getenv("GROQ_API_KEY"), MODEL_NAME)
        logger.info("Pipelien built sucesfuly....")

        print('*'*50)
        print(recommender.get_recommendation("I want to watch an anime like Naruto"))
        print('*'*50)

    except Exception as e:
            logger.error(f"Failed to execute pipeline {str(e)}")
            raise CustomException("Error during pipeline " , e)
    
if __name__=="__main__":
     main()

