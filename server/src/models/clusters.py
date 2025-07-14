from .schemas import clusterSchema,roleSchema,routineSchema,sparkSchema,groupSchema
from bson.objectid import ObjectId
import functools
from ..db import MongoCluster

class Cluster(MongoCluster):
    def __init__(self,id:str=None, instance:clusterSchema=None):
        super().__init__()
        self.instance = instance
        self._id = id if id else None


    def update(func):
        """
        Enhanced version with better error handling and optional logging
        """
        @functools.wraps(func)  # Preserves function metadata
        def wrapper(self, *args):
            # Pre-execution validation
            if not hasattr(self, 'instance') or not self.instance:
                raise ValueError("Cluster instance is not set. Please retrieve or create a cluster first.")
            
            if not hasattr(self, 'collection'):
                raise ValueError("Database collection is not initialized.")
            
            # Store original instance ID for safety
            original_id = self._id
            
            try:
                # Execute the original method
                result = func(self, *args)
                
                # Refresh instance from database
                updated_doc = self.db.clusters.find_one({"_id": ObjectId(original_id)})
                
                if updated_doc:
                    self.instance = clusterSchema(**updated_doc)
                    for key,value in dict(self.instance).items():
                        if (hasattr(self, key) and self[key]!= value) or not hasattr(self, key):
                            setattr(self,key,value)

                else:
                    raise ValueError(f"Cluster with ID {original_id} not found in database after update.")
                
                return result
            
            except Exception as e:
                # Log the error or handle it as needed
                print(f"Error in {func.__name__}: {e}")
                raise
    
        return wrapper
    

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
        if self.instance is not None:
            for key, value in dict(self.instance).items():
                setattr(self, key, value)
    
    