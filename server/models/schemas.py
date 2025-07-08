import uuid
from typing import Optional
from pydantic import Field,BaseModel
import datetime

class userSchema(BaseModel):
    id:str=Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field()
    email: str = Field()
    phone: str = Field()
    password: str = Field()
    tags: list[str] = Field(default_factory=list)
    clusters: list[str] = Field(default_factory=list)  # List of cluster IDs the user belongs to
    groups: list[str] = Field(default_factory=list)  # List of group IDs the user belongs to
    roles: list[str] = Field(default_factory=list)  # List of role IDs assigned
    sparks: list[str] = Field(default_factory=list)  # List of spark IDs the user is associated with
    routines: list[str] = Field(default_factory=list)  # List of routine IDs the
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())

class roleSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field()
    description: Optional[str] = Field(default=None)
    permissions: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    cluster: str = Field()  # Reference to the cluster this role belongs to

class routineSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
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
    id: str = Field(default_factory=uuid.uuid4,alias="_id")
    name: str = Field()
    description: Optional[str] = Field(default=None)
    tags: list[str] = Field(default_factory=list)
    status: str = Field(default="active")  # e.g., active, inactive, archived
    start_time: str = Field(default_factory=lambda: datetime.datetime.now().isoformat()) #including date
    end_time: str = Field() #including date
    active_duration: Optional[int] = Field(default=None)  # Duration in seconds
    total_spots: int = Field()  # Total number of spots available
    spots: int = Field()  # Number of spots currently filled
    created_by: str = Field()
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    cluster: str = Field()  # Reference to the cluster this spark belongs to
    group: Optional[str] = Field(default=None)  # Reference to the group this spark belongs to

class groupSchema(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str = Field()
    description: Optional[str] = Field(default=None)
    admin: str = Field(default_factory=uuid.uuid4)
    members: list[str] = Field(default_factory=list)
    access_role: str=Field(default_factory=None)
    moderators: list[str] = Field(default_factory=list)
    tags: list[str] = Field(default_factory=list)
    roles: list[str] = Field(default_factory=list)
    sparks: list[str] = Field(default_factory=list)
    routines: list[str] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())
    cluster: str = Field()  # Reference to the cluster this group belongs to

class clusterSchema(BaseModel):
    id:str=Field(default_factory=uuid.uuid4,alias="_id")
    name: str=Field()
    description: Optional[str] = Field(default=None)
    admin: str=Field(default_factory=uuid.uuid4)
    moderators: list[str] = Field(default_factory=list)
    members: list[str] = Field(default_factory=list)
    groups: list[groupSchema] = Field(default_factory=list)  # List of groups in the cluster
    tags: list[str] = Field(default_factory=list)
    roles: list[roleSchema] = Field(default_factory=list)
    sparks: list[sparkSchema] = Field(default_factory=list)
    routines: list[routineSchema] = Field(default_factory=list)
    created_at: str = Field(default_factory=lambda: datetime.datetime.now().isoformat())