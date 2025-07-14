from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri='mongodb+srv://manojkumar132006:IFVzayTeFE0m2I9i@cluster0.832jmw7.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0'
class MongoCluster:
    """
    A class to manage the MongoDB client and database connections.
    """
    def __init__(self):
        self.client = MongoClient(uri, server_api=ServerApi('1'))
        self.db = self.client['db0']
        self.db.users = self.db['users']
        self.db.clusters = self.db['clusters']
        self.db.groups = self.db['groups']
        self.db.roles = self.db['roles']
        self.db.routines = self.db['routines']
        self.db.sparks = self.db['sparks']