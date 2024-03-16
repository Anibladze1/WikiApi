from celery import Celery
from src.core.genAI import GenAIClient
import asyncio
from src.core.mongo_db import MongoDB

from src.core.constants import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

celery_app = Celery('tasks',
                    broker='redis://redis:6379/0',
                    backend='redis://redis:6379/0')

mongo_db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)
generative_client = GenAIClient()


@celery_app.task
def analyze_text_with_llm(topic, wiki_data):
    wiki_page_id = str(wiki_data['page_id'])

    summary = generative_client.analyze_text(wiki_data['text'])
    topic_title = topic.title()

    # Then insert the new document
    inserted_id = mongo_db.insert_document(COLLECTION_NAME, {
        "_id": wiki_page_id,
        "topic": topic_title,
        "summary": summary
    })
    return f"Successfully analyzed and saved summary for page ID {wiki_page_id} with topic {topic_title}"