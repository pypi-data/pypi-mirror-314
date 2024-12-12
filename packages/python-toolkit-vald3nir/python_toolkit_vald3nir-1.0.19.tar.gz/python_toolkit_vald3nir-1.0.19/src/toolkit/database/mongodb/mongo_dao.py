import pymongo
from bson import ObjectId
from pymongo import WriteConcern


class MongoDAO:

    def __init__(self, client_url: str, project_name: str, collection: str) -> None:
        super().__init__()
        self.client = pymongo.MongoClient(client_url)
        self._db = self.client[project_name][collection]

    # ------------------------------------------------------------------------------------------------------------------
    # Implementations
    # ------------------------------------------------------------------------------------------------------------------
    def insert_document(self, document: dict):
        self._db.insert_one(document)

    def insert_documents(self, documents: list[dict]):
        self._db.insert_many(documents)

    def update_one(self, query: dict, values: dict):
        self._db.update_one(query, update={"$set": values})

    def update_many(self, query: dict, values: dict):
        self._db.update_many(query, update={"$set": values})

    def clear(self):
        self._db.drop()

    def delete_objects(self, _ids: list[ObjectId]):
        self.delete_documents(query={"_id": {"$in": _ids}})

    def delete_documents(self, query: dict = None):
        self._db.delete_many(filter=query)

    def find_document(self, query: dict) -> dict:
        return self._db.find_one(query)

    def find_documents(self, query: dict = None, sort_field='_id', limit: int = 999999999) -> list[dict]:
        return list(self._db.find(query).sort(sort_field, pymongo.ASCENDING).limit(limit))

    def last(self, query: dict, sort_field: str = '_id', limit: int = 5):
        return list(self._db.find(query).sort([(sort_field, pymongo.DESCENDING)]).limit(limit))

    def distinct(self, key: str) -> list[str]:
        return self._db.distinct(key=key)

    def aggregate(self, pipeline: [dict]) -> list[dict]:
        return list(self._db.aggregate(pipeline=pipeline, maxTimeMS=60000, allowDiskUse=True))

    def collection_size(self) -> int:
        return self._db.count_documents({})

    def close(self):
        self.client.close()


# ----------------------------------------------------------------------------------------------------------------------
# Extra Methods
# ----------------------------------------------------------------------------------------------------------------------

def copy_databases(origin_database_name: str, origin_database_address: str, destination_database_name: str, destination_database_address: str, collections: [str], max_collection_size: int = 100000):
    origin = pymongo.MongoClient(origin_database_address)[origin_database_name]
    destination = pymongo.MongoClient(destination_database_address)[destination_database_name]

    if collections is None or len(collections) == 0:
        collections = origin.list_collection_names()

    for collection in collections:
        collections_cursor = origin[collection].find(limit=max_collection_size)
        clt = destination[collection]
        clt.drop()
        for document in collections_cursor:
            clt.with_options(write_concern=WriteConcern(w=0)).insert_one(document)
