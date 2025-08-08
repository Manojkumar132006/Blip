"""
MongoDB Connection Manager
"""
from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

client = MongoClient(os.getenv("MONGODB_URI"))
db = client['db0']

# Collections
users = db.users
clusters = db.clusters
groups = db.groups
roles = db.roles
routines = db.routines
sparks = db.sparks
