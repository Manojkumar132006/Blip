"""
Cluster Model (College/Workplace)
"""
import datetime
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional
from .group import Group
from .role import Role
from .routine import Routine
from .spark import Spark


def iso_now():
    return datetime.datetime.now().isoformat()


class Cluster(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    admin: str = Field()  # user ID
    moderators: List[str] = Field(default_factory=list)
    members: List[str] = Field(default_factory=list)
    calendar: Optional[str] = Field(default_factory=str)
    groups: List[Group] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    roles: List[str] = Field(default_factory=list)
    sparks: List[str] = Field(default_factory=list)
    routines: List[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=iso_now)
    id: Optional[str] = Field(default=None)

    async def save(self):
        from config.database import clusters as clusters_collection
        if self.id:
            # Update existing document
            result = await clusters_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        else:
            # Insert new document
            result = await clusters_collection.insert_one(self.dict(exclude={"id"}))
            self.id = result.inserted_id
        return self

    @classmethod
    async def get(cls, id: str):
        from config.database import clusters as clusters_collection
        cluster = await clusters_collection.find_one({"_id": ObjectId(id)})
        if cluster:
            return cls(**cluster)
        return None

    async def update(self):
        from config.database import clusters as clusters_collection
        result = await clusters_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        return self

    async def delete(self):
        from config.database import clusters as clusters_collection
        result = await clusters_collection.delete_one({"_id": self.id})
        return result.deleted_count