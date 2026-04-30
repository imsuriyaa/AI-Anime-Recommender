from langchain_groq import ChatGroq
from prompt.prompt_library import anime_chat_prompt
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
from logger import GLOBAL_LOGGER as log
from exception.custom_exception import CustomException
from utils.model_loader import ModelLoader

class AnimeRecommender:
    def __init__(self,retriever):
        self.llm = self._load_llm()
        self.prompt = anime_chat_prompt

        self.qa_chain = (
            {
                "context": retriever,   # retriever auto-fills context
                "question": RunnablePassthrough()
            }
            | self.prompt
            | self.llm
            | StrOutputParser()
        )


    def _load_llm(self):
        try:
            llm = ModelLoader().load_llm()
            if not llm:
                raise ValueError("LLM loading returned None")
            log.info("LLM loaded successfully")
            return llm
        except Exception as e:
            log.error(f"Failed to load LLM {str(e)}")
            raise CustomException("Error during LLM loading" , e)

    def get_recommendation(self,query:str):
        result = self.qa_chain.invoke(query)
        return result
