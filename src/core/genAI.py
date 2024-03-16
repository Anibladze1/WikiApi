import os
import textwrap

from dotenv import load_dotenv

from langchain_openai import OpenAI
from langchain.chains.summarize import load_summarize_chain

import tiktoken


load_dotenv()

model_name = "text-davinci-003"
token_limit = 4096
verbose = True
openai_key = os.getenv("OPEN_AI_KEY")

llm = OpenAI(openai_key=openai_key, model_name=model_name)


def num_tokens_from_string(string: str, encoding_name: str) -> int:
    encoding = tiktoken.encoding_for_model(encoding_name)
    num_tokens = len(encoding.encode(string))
    return num_tokens


num_tokens = num_tokens_from_string("news_article", model_name)

if num_tokens < token_limit:
  chain = load_summarize_chain(llm, chain_type="stuff", verbose=verbose)
else:
  chain = load_summarize_chain(llm, chain_type="map_reduce", map_prompt=prompt, combine_prompt=prompt, verbose=verbose)

summary = chain.run()

print(f"Chain type: {chain.__class__.__name__}")
print(f"Summary: {textwrap.fill(summary, width=100)}")