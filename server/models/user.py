"""
User Model
"""
from pydantic import BaseModel, Field
from bson import ObjectId
from typing import List, Optional
import datetime


def iso_now():
    return datetime.datetime.now().isoformat()


class User(BaseModel):
    name: str = Field()
    email: str = Field()
    phone: Optional[str] = Field(default=None)
    password: str = Field()  # hashed in practice
    tags: List[str] = Field(default_factory=list)
    calendar: Optional[str] = Field(default_factory=str)
    clusters: List[str] = Field(default_factory=list)  # list of cluster IDs
    groups: List[str] = Field(default_factory=list)  # list of group IDs
    roles: List[str] = Field(default_factory=list)  # list of role IDs
    sparks: List[str] = Field(default_factory=list)  # list of spark IDs
    routines: List[str] = Field(default_factory=list)  # list of routine IDs
    created_at: str = Field(default_factory=iso_now)
    id: Optional[str] = Field(default=None)

    async def save(self):
        from config.database import users as users_collection
        if self.id:
            # Update existing document
            result = await users_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        else:
            # Insert new document
            result = await users_collection.insert_one(self.dict(exclude={"id"}))
            self.id = result.inserted_id
        return self

    @classmethod
    async def get(cls, id: str):
        from config.database import users as users_collection
        user = await users_collection.find_one({"_id": ObjectId(id)})
        if user:
            return cls(**user)
        return None

    async def update(self):
        from config.database import users as users_collection
        result = await users_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        return self

    async def delete(self):
        from config.database import users as users_collection
        result = await users_collection.delete_one({"_id": self.id})
        return result.deleted_count