import os
import time

from src.core.constants import API_KEY, MODEL_NAME, TOKEN_LIMIT, VERBOSE

from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.chains.summarize import load_summarize_chain
from langchain.docstore.document import Document
from langchain.prompts import PromptTemplate

import tiktoken


class GenAIClient:
    def __init__(self):
        self.model_name = MODEL_NAME
        self.token_limit = TOKEN_LIMIT
        self.verbose = VERBOSE
        self.openai_key = API_KEY
        self.llm = ChatOpenAI(openai_api_key=self.openai_key, model_name=self.model_name)

    @staticmethod
    def num_tokens_from_string(string: str, encoding_name: str) -> int:
        encoding = tiktoken.encoding_for_model(encoding_name)
        num_tokens = len(encoding.encode(string))
        return num_tokens

    def analyze_text(self, text: str) -> str:
        text_splitter = CharacterTextSplitter.from_tiktoken_encoder(model_name=self.model_name)
        texts = text_splitter.split_text(text)
        docs = [Document(page_content=t) for t in texts]

        prompt_template = """
        Write a concise summary of the following:
        {text}
        CONSCISE SUMMARY IN ENGLISH:
        """

        prompt = PromptTemplate(template=prompt_template, input_variables=["text"])

        num_tokens = self.num_tokens_from_string(text, self.model_name)

        if num_tokens < self.token_limit:
            chain = load_summarize_chain(self.llm, chain_type="stuff", prompt=prompt, verbose=self.verbose)
        else:
            chain = load_summarize_chain(self.llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt,
                                         verbose=self.verbose)

        summary = chain.run(docs)

        return summary