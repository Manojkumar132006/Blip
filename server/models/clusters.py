from schemas import clusterSchema,roleSchema,routineSchema,sparkSchema,groupSchema
from database.connection import clusters

class Cluster:
    def __init__(self, instance:clusterSchema=None):
        self.instance = None
    
    def get(self,id:str = None) -> list[clusterSchema]:
        """
        Retrieve all clusters from the database.
        """
        if id:
            self.instance = Cluster(clusters.find_one({"_id": id}))
            return self.instance
        return list(clusters.find())
    
    def new(self, cluster_data:clusterSchema) -> clusterSchema:
        """
        Create a new cluster in the database.
        """
        new_cluster = clusterSchema(dict(**cluster_data))
        new_cluster = clusters.insert_one(dict(new_cluster))
        self.instance = Cluster(new_cluster)
        return self.instance
    