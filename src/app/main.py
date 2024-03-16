from fastapi import FastAPI, HTTPException

from src.core.mongo_db import MongoDB
from src.core.wikipedia import WikipediaClient
from src.core.celery_config import analyze_text_with_llm
from src.core.constants import MONGO_URI, DATABASE_NAME, COLLECTION_NAME

app = FastAPI()
wikipedia_client = WikipediaClient()
mongo_db = MongoDB(uri=MONGO_URI, db_name=DATABASE_NAME)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/process/")
async def process_text(topic: str):
    try:
        wiki_data: dict = await wikipedia_client.retrieve_topic_data(topic_title=topic)
        wiki_page_id = str(wiki_data['page_id'])

        existing_document = mongo_db.find_document(COLLECTION_NAME, {'_id': wiki_page_id})
        if existing_document:
            return f"Document with page ID {wiki_page_id} already exists, skipping summarization."
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    # Offload the heavy computation to Celery
    task = analyze_text_with_llm.delay(topic=topic, wiki_data=wiki_data)
    return {"message": "Processing started", "task": task.id}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="127.0.0.1", port=8800, reload=True)
