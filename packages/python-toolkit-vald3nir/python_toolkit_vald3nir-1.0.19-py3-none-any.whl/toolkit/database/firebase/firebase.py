import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

"""
To get firebase certificate: https://firebase.google.com/docs/admin/setup?hl=pt-br
"""


class Firebase:

    def __init__(self, firebase_config: dict, firebase_certificate: dict) -> None:
        super().__init__()
        cred = credentials.Certificate(firebase_certificate)
        firebase_admin.initialize_app(cred, firebase_config)
        self._db = db

    def insert_or_update(self, path: str, data):
        ref = self._db.reference(path)
        ref.set(data)

    def load(self, path: str):
        ref = self._db.reference(path)
        return ref.get()

    def clear(self, path: str):
        self.insert_or_update(path, {})
