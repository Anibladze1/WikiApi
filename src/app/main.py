from fastapi import FastAPI, HTTPException

from src.core.mongo_db import MongoDB
from src.core.wikipedia import WikipediaClient
from src.core.celery_config import insert_in_database
from src.core.constants import MONGO_URI, DATABASE_NAME, COLLECTION_NAME
from src.logger import get_logger

from src.app.schemas import SummarizeTopicResponse, ErrorResponse, ReadSummaryResponse


app = FastAPI()
wikipedia_client = WikipediaClient()
mongo_db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)

logger = get_logger(__name__)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post(
    path="/summarize_topic",
    response_model=SummarizeTopicResponse,
    responses={500: {'model': ErrorResponse}}
)
async def summarize_topic(topic_title: str):
    """
    Processes the text for a given topic by summarizing its content from Wikipedia.
    If the summary already exists in the database, it skips the summarization.

    :param topic_title: The topic to be summarized.
    :return: A message indicating the process status or an existing summary.
    """
    try:
        wiki_data = await wikipedia_client.retrieve_topic_data(topic_title=topic_title)
        wiki_page_id = str(wiki_data['page_id'])

        if mongo_db.find_document(COLLECTION_NAME, {'_id': wiki_page_id}):
            message = f"Document with page ID {wiki_page_id} already exists, skipping summarization."
            logger.info(message)
            return {"message": message}

        # Offload the heavy computation to Celery
        task = insert_in_database.delay(topic_title=topic_title, wiki_data=wiki_data)
        return {"message": "Processing started", "task_id": task.id}
    except Exception as e:
        logger.error(f"Error processing text for topic '{topic_title}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get(
    path="/read_summary",
    response_model=ReadSummaryResponse,
    responses={500: {'model': ErrorResponse}}
)
async def read_summary(topic_title_or_id: str):
    """
    Retrieves the summary of a topic from the database using either its title or ID.

    :param topic_title_or_id: The title or the ID of the topic to retrieve the summary for.
    :return: The summary of the topic if found, otherwise an error message.
    """
    try:
        query = {"$or": [{'_id': topic_title_or_id}, {'topic_title': topic_title_or_id.title()}]}
        existing_document = mongo_db.find_document(COLLECTION_NAME, query)

        if existing_document:
            return {"summary": existing_document['summary']}
        else:
            message = f"Summary with provided ID/Title '{topic_title_or_id}' doesn't exist."
            logger.error(message)
            raise HTTPException(status_code=404, detail=message)
    except Exception as e:
        logger.error(f"Error reading summary for '{topic_title_or_id}': {e}")
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8800, reload=True)
