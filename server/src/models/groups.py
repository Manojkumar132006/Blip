from .schemas import groupSchema,clusterSchema
from bson.objectid import ObjectId
from ..db import MongoCluster

class GroupManager(MongoCluster):
    def __init__(self,cluster_id: str = None,group_id:int=None,instance=None):
        super().__init__()
        self._id = cluster_id
        self.instance = instance
        self.group_id = group_id

    def __str__(self):
        return self.groupList.__str__()
    
    def load(self):
        if self.cluster_id and self.group_id:
            self.instance=clusterSchema(self.clusters.find_one({"_id":self.cluster_id})).groups[self.group_id]
        elif (self.cluster_id and not self.group_id) and self.instance:
            self.group_id = self.add(self.instance)
        
    def add(self, group_data: groupSchema) -> groupSchema:
        """
        Create a new group in the database.
        """
        group_data['cluster'] = str(self._id)
        new_group_data = groupSchema(**group_data)
        self.clusters.update_one({"_id": ObjectId(self._id)}, {"$push": {"groups": dict(new_group_data)}})
        self.instance = new_group_data
        return len(self.clusters.find_one({"_id":ObjectId(self._id)}).groups)-1
        
    
    def join_member(self, user_id: str) -> groupSchema:
        if user_id not in self.instance.members:
            raise ValueError(f"User {user_id} is not a member of the cluster.")
        else:
            self.instance.members.append(user_id)
            self.groups.update_one({"_id": ObjectId(self.instance.id)}, {"$set": {"members": self.instance.members}})
            self.users.update_one({"_id":ObjectId(user_id)}, {"$addToSet": {"groups": f'{self._id}.{self.group_id}'}})
    
    def remove_member(self, user_id: str) -> groupSchema:
        if user_id in self.instance.members:
            self.instance.members.remove(user_id)
            self.groups.update_one({"_id": ObjectId(self.instance.id)}, {"$set": {"members": self.instance.members}})
            self.users.update_one({"_id":ObjectId(user_id)}, {"$pull": {"groups": f'{self._id}.{self.group_id}'}})
        else:
            raise ValueError(f"User {user_id} is not a member of the group.")
            
    def add_moderator(self, user_id: str) -> groupSchema:
        if (user_id not in self.instance.moderators) and (user_id in self.instance.members):
            self.instance.moderators.append(user_id)
            self.groups.update_one({"_id": ObjectId(self.instance.id)}, {"$set": {"moderators": self.instance.moderators}})
        elif user_id not in self.instance.members:
            raise ValueError(f"User {user_id} is not a member of the group.")
    