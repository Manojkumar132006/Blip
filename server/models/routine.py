"""
Routine Model
"""
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
