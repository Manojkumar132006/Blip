```
"""
Role Model
"""
import datetime
from pydantic import BaseModel, Field
from typing import List, Optional

def iso_now():
    return datetime.datetime.now().isoformat()

class Role(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    permissions: List[str] = Field(default_factory=list)
    cluster: str = Field()  # cluster ID
    created_at: str = Field(default_factory=iso_now)
    id: Optional[str] = Field(default=None)

    async def save(self):
        from config.database import roles as roles_collection
        if self.id:
            # Update existing document
            result = await roles_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        else:
            # Insert new document
            result = await roles_collection.insert_one(self.dict(exclude={"id"}))
            self.id = str(result.inserted_id)
        return self

    @classmethod
    async def get(cls, id: str):
        from config.database import roles as roles_collection
        role = await roles_collection.find_one({"_id": id})
        if role:
            return cls(**role)
        return None

    async def update(self):
        from config.database import roles as roles_collection
        result = await roles_collection.update_one({"_id": self.id}, {"$set": self.dict(exclude={"id"})})
        return self

    async def delete(self):
        from config.database import roles as roles_collection
        result = await roles_collection.delete_one({"_id": self.id})
        return result.deleted_count

