from pymongo import MongoClient
from typing import Any


class MongoDB:
    def __init__(self, uri: str, db_name: str):
        self.client = MongoClient(uri)
        self.db = self.client[db_name]

    def get_collection(self, collection_name: str):
        """
        Retrieves a collection from the database.

        :param collection_name: The name of the collection to retrieve.
        :return: Collection
        """
        return self.db[collection_name]

    def insert_document(self, collection_name: str, document: dict):
        """
        Inserts a single document into the specified collection.

        :param collection_name: The name of the collection where the document will be inserted.
        :param document: The document to insert.
        :return: The result of the insert operation.
        """
        collection = self.get_collection(collection_name)
        result = collection.insert_one(document)
        return result.inserted_id

    def find_document(self, collection_name: str, query: dict) -> Any:
        """
        Finds a single document in the specified collection.

        :param collection_name: The name of the collection to search.
        :param query: The query used to find the document.
        :return: The found document or None.
        """
        collection = self.get_collection(collection_name)
        document = collection.find_one(query)
        return document
