from pysondb import db


class JsonDB:

    def __init__(self, path: str = "localdb.json") -> None:
        super().__init__()
        self.database = db.getDb(path)

    def find_document(self, query: dict):
        try:
            return self.database.getBy(query)[0]
        except:
            return None

    def insert_document(self, data: dict):
        self.database.add(new_data=data)

    def insert_documents(self, data: list[dict]):
        self.database.addMany(new_data=data)

    def update_document(self, _id: int, data: dict):
        self.database.updateById(pk=_id, new_data=data)

    def find_documents(self) -> list[dict]:
        return list(self.database.getAll())

    def last_documents(self, limit=5) -> list[dict]:
        return self.database.get(num=limit)

    def clear(self):
        self.database.deleteAll()
