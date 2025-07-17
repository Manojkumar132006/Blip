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
        self.users = self.db['users']
        self.clusters = self.db['clusters']
        self.groups = self.db['groups']
        self.roles = self.db['roles']
        self.routines = self.db['routines']
        self.sparks = self.db['sparks']