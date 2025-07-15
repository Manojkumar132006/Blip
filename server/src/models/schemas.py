import uuid
from typing import Optional
from pydantic import Field,BaseModel
import datetime

class userSchema(BaseModel):
    name: str = Field()
    email: str = Field()
    phone: str = Field(default_factory=None)
    password: str = Field()
    tags: list[str] = Field(default_factory=list)
    clusters: list[str] = Field(default_factory=list)  # list of cluster IDs the user belongs to
    groups: list[str] = Field(default_factory=list)  # list of group IDs the user belongs to
    roles: list[str] = Field(default_factory=list)  # list of role IDs assigned
    sparks: list[str] = Field(default_factory=list)  # list of spark IDs the user is associated with
    routines: list[str] = Field(default_factory=list)  # list of routine IDs the
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class roleSchema(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    permissions: list[str] = Field(default_factory=list)
    cluster: str = Field()  # Reference to the cluster this role belongs to
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class routineSchema(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    tags: list[str] = Field(default_factory=list)
    status: str = Field(default="active")  # e.g., active, inactive, archived
    start_time: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())  # only time so as to apply to all days
    end_time: str = Field()  # only time so as to apply to all days
    cluster: str = Field()  # Reference to the cluster this routine belongs to
    group: Optional[str] = Field(default=None)  # Reference to the group this routine belongs to    
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class sparkSchema(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    tags: list[str] = Field(default_factory=list)
    status: str = Field(default="active")  # e.g., active, inactive, archived
    start_time: str = Field(default_factory=lambda: datetime.datetime.now().isoformat()) #including date
    end_time: str = Field() #including date
    active_duration: Optional[int] = Field(default=None)  # Duration in seconds
    total_spots: int = Field()  # Total number of spots available
    spots: int = Field()  # Number of spots currently filled
    cluster: str = Field()  # Reference to the cluster this spark belongs to
    group: Optional[str] = Field(default=None)  # Reference to the group this spark belongs to
    created_by: str = Field()
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class groupSchema(BaseModel):
    name: str = Field()
    description: Optional[str] = Field(default=None)
    admin: str = Field()
    members: list[str] = Field(default_factory=list)
    moderators: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    sparks: list[str] = Field(default_factory=list)
    routines: list[str] = Field(default_factory=list)
    cluster: str = Field()  # Reference to the cluster this group belongs to
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class clusterSchema(BaseModel):
    name: str=Field()
    description: Optional[str] = Field(default=None)
    admin: str=Field()
    moderators: list[str] = Field()
    members: list[str] = Field()
    groups: list[groupSchema] = Field(default_factory=list)  # list of groups in the cluster
    tags: list[str] = Field(default_factory=list)
    roles: list[roleSchema] = Field(default_factory=list)
    sparks: list[sparkSchema] = Field(default_factory=list)
    routines: list[routineSchema] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())