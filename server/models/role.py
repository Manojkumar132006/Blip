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
