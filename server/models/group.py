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
