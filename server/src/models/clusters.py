from .schemas import clusterSchema,roleSchema,routineSchema,sparkSchema,groupSchema
from bson.objectid import ObjectId
import functools
from ..db import MongoCluster

class Cluster(MongoCluster):
    def __init__(self,id:str=None, instance:clusterSchema=None):
        super().__init__()
        self.instance = instance
        self._id = ObjectId(id) if id else None


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
                updated_doc = self.clusters.find_one({"_id": ObjectId(original_id)})
                
                if updated_doc:
                    self.instance = clusterSchema(**updated_doc)
                else:
                    raise ValueError(f"Cluster with ID {original_id} not found in database after update.")
                
                return result
            
            except Exception as e:
                # Log the error or handle it as needed
                print(f"Error in {func.__name__}: {e}")
                raise
    
        return wrapper
    

    def new(self,cluster_data:clusterSchema) -> clusterSchema:
        """
        Create a new cluster in the database.
        """
        new_cluster_data = clusterSchema(**cluster_data)
        new_cluster = self.clusters.insert_one(dict(new_cluster_data))
        return self.clusters.find_one({"_id":new_cluster.inserted_id})

    def load(self):
        if self._id is None and self.instance is None:
            return self.clusters.find()
        elif self._id is not None:
            self.instance = self.clusters.find_one({"_id": self._id})
            if not self.instance:
                raise ValueError(f"Cluster with id {self._id} not found.")
            else:
                self.instance = clusterSchema(**self.instance)
        elif self._id is None and self.instance is not None:
            self.instance = self.new(self.instance)
        if self.instance is not None:
            for key, value in dict(self.instance).items():
                setattr(self, key, value)
    
    @update
    def newRole(self, role_data:roleSchema) -> roleSchema:
        """
        Create a new role in the cluster.
        """
        if not self.instance:
            raise ValueError("Cluster instance is not set. Please retrieve or create a cluster first.")
        
        role_data['cluster'] = str(self._id)
        new_role = roleSchema(**role_data)
        new_role = self.clusters.update_one({"_id": self._id}, {"$push": {"roles": dict(new_role)}})
        return new_role
    
    @update
    def newRoutine(self, routine_data:routineSchema) -> routineSchema:
        """
        Create a new routine in the cluster.
        """
        if not self.instance:
            raise ValueError("Cluster instance is not set. Please retrieve or create a cluster first.")
        
        routine_data.cluster = self.instance._id
        new_routine = routineSchema(dict(**routine_data))
        new_routine = self.clusters.update_one({"_id": self.instance._id}, {"$push": {"routines": dict(new_routine)}})
        return new_routine
    
    @update
    def newSpark(self, spark_data:sparkSchema) -> sparkSchema:
        """
        Create a new spark in the cluster.
        """
        if not self.instance:
            raise ValueError("Cluster instance is not set. Please retrieve or create a cluster first.")
        
        spark_data.cluster = self.instance._id
        new_spark = sparkSchema(dict(**spark_data))
        new_spark = self.clusters.update_one({"_id": self.instance._id}, {"$push": {"sparks": dict(new_spark)}})
        return new_spark
    
    @update
    def newGroup(self, group_data:groupSchema) -> groupSchema:
        """
        Create a new group in the cluster.
        """
        if not self.instance:
            raise ValueError("Cluster instance is not set. Please retrieve or create a cluster first.")
        
        group_data.cluster = self.instance._id
        new_group = groupSchema(dict(**group_data))
        new_group = self.clusters.update_one({"_id": self.instance._id}, {"$push": {"groups": dict(new_group)}})

        return new_group
    
    @update
    def newMember(self, member_id: str) -> None:
        """
        Add a new member to the cluster.
        """
        if not self.instance:
            raise ValueError("Cluster instance is not set. Please retrieve or create a cluster first.")
        
        if member_id not in self.instance.members:
            self.members.append(member_id)
            self.clusters.update_one({"_id": self._id}, {"$set": {"members": self.members}})
            self.users.update_one({"_id": ObjectId(member_id)}, {"$addToSet": {"clusters": str(self._id)}})
        else:
            raise ValueError(f"Member {member_id} already exists in the cluster.")