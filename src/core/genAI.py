import logging
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.settings import API_KEY, MODEL_NAME, VERBOSE
from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
import tiktoken
from src.logger import get_logger


class GenAIClient:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.token_limit = 4096
        self.verbose = VERBOSE
        self.openai_key = API_KEY
        self.llm = OpenAI(openai_api_key=self.openai_key, model_name=self.model_name)
        self.logger = get_logger(__name__)

    @staticmethod
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def analyze_text(self, text: str) -> str:
        try:
            self.logger.info("Starting text analysis.")
            text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=12000,
                chunk_overlap=400,
            )
            texts = text_splitter.split_text(text)
            docs = [Document(page_content=t) for t in texts]

            num_tokens = self.num_tokens_from_string(text, self.model_name)
            self.logger.debug(f"Number of tokens in text: {num_tokens}")

            if num_tokens < self.token_limit:
                chain = load_summarize_chain(self.llm, chain_type="stuff", verbose=self.verbose)
                self.logger.debug("Using 'stuff' chain type for summarization.")
            else:
                chain = load_summarize_chain(self.llm, chain_type="map_reduce", verbose=self.verbose)
                self.logger.debug("Using 'map_reduce' chain type for summarization.")

            input_dict = {'input_documents': docs}
            summary = chain.invoke(input_dict)["output_text"]
            self.logger.info("Text analysis completed.")
            return summary.strip()

        except Exception as e:
            self.logger.error(f"Error during text analysis: {e}", exc_info=True)
            raise
