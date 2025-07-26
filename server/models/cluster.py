"""
Cluster Model (College/Workplace)
"""
import datetime
from pydantic import BaseModel, Field
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
    groups: List[Group] = Field(default_factory=list)
    tags: List[str] = Field(default_factory=list)
    roles: List[Role] = Field(default_factory=list)
    sparks: List[Spark] = Field(default_factory=list)
    routines: List[Routine] = Field(default_factory=list)
    created_at: str = Field(default_factory=iso_now)
