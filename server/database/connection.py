from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri='mongodb+srv://manojkumar132006:IFVzayTeFE0m2I9i@cluster0.832jmw7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
client = MongoClient(uri, server_api=ServerApi('1'))

db=client['db0']
users=client['db0']['users']
clusters=client['db0']['clusters']
groups=client['db0']['groups']
roles=client['db0']['roles']
routines=client['db0']['routines']
sparks=client['db0']['sparks']