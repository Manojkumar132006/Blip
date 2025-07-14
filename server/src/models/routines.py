from schemas import routineSchema
from ..db import MongoCluster
from bson.objectid import ObjectId

class Routine(MongoCluster):
    def __init__(self, id: str = None, instance: routineSchema = None):
        super().__init__()
        self.instance = instance
        self._id = ObjectId(id) if id else None

    def new(self, routine_data: routineSchema) -> routineSchema:
        """
        Create a new routine in the database.
        """
        new_routine_data = routineSchema(**routine_data)
        new_routine = self.routines.insert_one(dict(new_routine_data))
        self.clusters.update_one({"_id": ObjectId(new_routine_data.cluster)}, {"$push": {"routines": dict(new_routine_data)}})
        if new_routine_data.group:
            self.groups.update_one({"_id": ObjectId(new_routine_data.group)}, {"$push": {"routines": dict(new_routine_data)}})
        return self.routines.find_one({"_id": new_routine.inserted_id})

    def load(self):
        if self._id is None and self.instance is None:
            raise ValueError("Routine ID or instance must be provided to load a routine.")
        
        routine_doc = self.routines.find_one({"_id": ObjectId(self._id)})
        if routine_doc:
            self.instance = routineSchema(**routine_doc)
        else:
            raise ValueError(f"Routine with ID {self._id} not found in database.")