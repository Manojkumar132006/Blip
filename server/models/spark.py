"""
Spark Model
"""
import datetime
from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List, Optional

def iso_now():
    return datetime.datetime.now().isoformat()

class Spark(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list)
    status: str = Field(default="active")
    start_time: str = Field(default_factory=iso_now)  # datetime ISO string
    end_time: str = Field()  # datetime ISO string
    active_duration: Optional[int] = Field(default=None)  # in seconds
    total_spots: int = Field()
    spots: int = Field()  # current spots filled
    cluster: str = Field()  # cluster ID
    group: Optional[str] = Field(default=None)  # group ID
    created_by: str = Field()
    created_at: str = Field(default_factory=iso_now)
    id: Optional[str] = Field(default=None)

    async def save(self):
        from config.database import sparks as sparks_collection
        if self.id:
            # Update existing document
            result = await sparks_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        else:
            # Insert new document
            result = await sparks_collection.insert_one(self.dict(exclude={"id"}))
            self.id = result.inserted_id
        return self

    @classmethod
    async def get(cls, id: str):
        from config.database import sparks as sparks_collection
        spark = await sparks_collection.find_one({"_id": ObjectId(id)})
        if spark:
            return cls(**spark)
        return None

    async def update(self):
        from config.database import sparks as sparks_collection
        result = await sparks_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        return self

    async def delete(self):
        from config.database import sparks as sparks_collection
        result = await sparks_collection.delete_one({"_id": self.id})
        return result.deleted_count