"""
Spark Model
"""
import datetime
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
