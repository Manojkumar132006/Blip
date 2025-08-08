"""
Routine Model
"""
import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

def iso_now():
    return datetime.datetime.now().isoformat()

class Routine(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    tags: List[str] = Field(default_factory=list)
    status: str = Field(default="active")
    start_time: str = Field(default_factory=iso_now)  # time-only ISO string
    end_time: str = Field()  # time-only ISO string
    cluster: str = Field()  # cluster ID
    group: Optional[str] = Field(default=None)  # group ID
    created_at: str = Field(default_factory=iso_now)
    id: Optional[str] = Field(default=None)

    async def save(self):
        from config.database import routines as routines_collection
        if self.id:
            # Update existing document
            result = await routines_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        else:
            # Insert new document
            result = await routines_collection.insert_one(self.dict(exclude={"id"}))
            self.id = str(result.inserted_id)
        return self

    @classmethod
    async def get(cls, id: str):
        from config.database import routines as routines_collection
        routine = await routines_collection.find_one({"_id": id})
        if routine:
            return cls(**routine)
        return None

    async def update(self):
        from config.database import routines as routines_collection
        result = await routines_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        return self

    async def delete(self):
        from config.database import routines as routines_collection
        result = await routines_collection.delete_one({"_id": self.id})
        return result.deleted_count