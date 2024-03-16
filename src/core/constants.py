import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = ""
MODEL_NAME = "gpt-3.5-turbo-0125"
TOKEN_LIMIT = 4096
VERBOSE = False
DATABASE_NAME = 'mongo_db'
COLLECTION_NAME = 'wikipedia_summaries'
MONGO_URI = 'mongodb://mongo:27017/'