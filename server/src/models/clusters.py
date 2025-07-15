from .schemas import clusterSchema,roleSchema,routineSchema,sparkSchema,groupSchema
from bson.objectid import ObjectId
import functools
from ..db import MongoCluster

class ClusterManager(MongoCluster):
    def __init__(self,id:str=None, instance:clusterSchema=None):
        super().__init__()
        self.instance = instance
        self._id = id if id else None
    

    def add(self,cluster_data:clusterSchema) -> clusterSchema:
        """
        Create a new cluster in the database.
        """
        new_cluster_data = clusterSchema(**cluster_data)
        new_cluster = self.db.clusters.insert_one(dict(new_cluster_data))
        return self.db.clusters.find_one({"_id":new_cluster.inserted_id})

    def load(self):
        if self._id is None and self.instance is None:
            return self.db.clusters.find()
        elif self._id is not None:
            self.instance = self.db.clusters.find_one({"_id": self._id})
            if not self.instance:
                raise ValueError(f"Cluster with id {self._id} not found.")
            else:
                self.instance = clusterSchema(**self.instance)
        elif self._id is None and self.instance is not None:
            self.instance = self.add(self.instance)    