from .schemas import groupSchema
from bson.objectid import ObjectId
from ..db import MongoCluster

class Group(MongoCluster):
    def __init__(self,groups: list[groupSchema] = None):
        super().__init__()
        self.groupList = groups if groups is not None else []

    def __str__(self):
        return self.groupList.__str__()
        
    def add(self, group_data: groupSchema) -> groupSchema:
        """
        Create a new group in the database.
        """
        group_data['cluster'] = str(self._id) if self._id else None
        new_group_data = groupSchema(**group_data)
        new_group = self.groups.insert_one(dict(new_group_data))
        self.clusters.update_one({"_id": ObjectId(self._id)}, {"$push": {"groups": dict(new_group_data)}})
        return self.groups.find_one({"_id": new_group.inserted_id})
    
    