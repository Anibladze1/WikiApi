from celery import Celery
from pymongo.errors import DuplicateKeyError

from src.core.genAI import GenAIClient
from src.core.mongo_db import MongoDB
from src.core.constants import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from src.logger import get_logger

celery_app = Celery('tasks',
                    broker='redis://redis:6379/0',
                    backend='redis://redis:6379/0')

mongo_db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
generative_client = GenAIClient()
logger = get_logger(__name__)


def generate_summary(topic, wiki_data):
    """
    Generates a summary for the given topic based on Wikipedia data.

    :param topic: The topic to summarize.
    :param wiki_data: The data retrieved from Wikipedia, including the text to summarize.
    :return: A dictionary containing the topic, summary, and page ID.
    """
    logger.info(f"Generating summary for topic: {topic}")

    wiki_page_id = str(wiki_data['page_id'])
    summary = generative_client.analyze_text(wiki_data['text'])
    topic_title = topic.title()

    return {
        "_id": wiki_page_id,
        "topic": topic_title,
        "summary": summary
    }


@celery_app.task
def insert_in_database(topic, wiki_data):
    """
    Analyzes and summarizes the text for a given topic, then attempts to save it to the database.
    If a document with the same ID already exists, it catches the DuplicateKeyError and skips insertion.

    :param topic: The topic to summarize.
    :param wiki_data: The data retrieved from Wikipedia, including the text to summarize.
    :return: A message indicating the outcome of the operation.
    """
    document = generate_summary(topic, wiki_data)
    wiki_page_id = document["_id"]
    topic_title = document["topic"]

    try:
        inserted_id = mongo_db.insert_document(COLLECTION_NAME, document)
        logger.info(f"Successfully analyzed and saved summary for topic {topic_title} with page ID {inserted_id}")
        return f"Successfully analyzed and saved summary for page ID {inserted_id} with topic {topic_title}"
    except DuplicateKeyError:
        logger.warning(f"DuplicateKeyError: Document with page ID {wiki_page_id} already exists, skipping insertion.")
        return (f"Document with page ID {wiki_page_id} was inserted in database"
                f" before finishing task, skipping insertion.")
