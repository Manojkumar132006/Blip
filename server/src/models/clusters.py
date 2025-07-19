from .schemas import clusterSchema
from ..db import db
from bson import ObjectId


class ClusterManager():
    def get_by_id(self, id: str):
        # Check if provided id is of right Format
        try:
            ID = ObjectId(id)
        except Exception:
            raise ValueError(f"Invalid MongoDB Object-ID {id}")

        # Get document from Database
        cluster = db['clusters'].find_one({"_id": ID})

        # If no document Exist in Dictionary
        if not cluster:
            raise ValueError(f"Document with given ID doesnt exist")

        # Add attributes from document
        for key in cluster:
            setattr(self, key, cluster[key])

    def add_by_instance(self, instance: dict):
        # Validate Instance
        clusterSchema(**instance)

        # Add instance to DataBase
        result = db['clusters'].insert_one(instance)

        # Add attributes form instance
        self._id = result.inserted_id
        for key in instance:
            setattr(self, key, instance[key])

    def load(self):
        try:
            self._id
        except Exception:
            raise ValueError("Instance not Found")
        return db['clusters'].find_one({'_id': ObjectId(self._id)})

    def load_all(self):
        return list(db['clusters'].find())

    def update(self):
        return

    def delete(self):
        try:
            self._id
        except Exception:
            raise AttributeError("Instance not found")
        db['clusters'].delete_one({'_id': ObjectId(self._id)})
