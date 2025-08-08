"""
User Model
"""
from pydantic import BaseModel, Field
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
