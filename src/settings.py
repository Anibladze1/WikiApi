"""
Configure settings for the FastAPI application.

This module contains configurations related to the FastAPI application, such as API settings, database settings, and any
other relevant configurations.

"""

import os

from dotenv import load_dotenv

from src import __version__

load_dotenv()


VERSION = __version__
ENVIRONMENT = os.getenv("ENVIRONMENT", "dev")
BASE_URL = os.getenv("BASE_URL", "/")

API_KEY = os.getenv("OPENAI_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
VERBOSE = os.getenv("VERBOSE")
DATABASE_NAME = os.getenv("DATABASE_NAME")
COLLECTION_NAME = os.getenv("COLLECTION_NAME")
MONGO_URI = os.getenv("MONGO_URI")

