```
"""
Group Model
"""
import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

def iso_now():
    return datetime.datetime.now().isoformat()

class Group(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    admin: str = Field()  # user ID
    members: List[str] = Field(default_factory=list)
    moderators: List[str] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    calendar: Optional[str]=Field(default_factory="")
    roles: List[str] = Field(default_factory=list)
    sparks: List[str] = Field(default_factory=list)
    routines: List[str] = Field(default_factory=list)
    cluster: str = Field()  # cluster ID
    created_at: str = Field(default_factory=iso_now)
    id: Optional[str] = Field(default=None)

    async def save(self):
        from config.database import groups as groups_collection
        if self.id:
            # Update existing document
            result = await groups_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        else:
            # Insert new document
            result = await groups_collection.insert_one(self.dict(exclude={"id"}))
            self.id = str(result.inserted_id)
        return self

    @classmethod
    async def get(cls, id: str):
        from config.database import groups as groups_collection
        group = await groups_collection.find_one({"_id": id})
        if group:
            return cls(**group)
        return None

    async def update(self):
        from config.database import groups as groups_collection
        result = await groups_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        return self

    async def delete(self):
        from config.database import groups as groups_collection
        result = await groups_collection.delete_one({"_id": self.id})
        return result.deleted_count

