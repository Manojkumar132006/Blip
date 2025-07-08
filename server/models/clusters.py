from schemas import clusterSchema,roleSchema,routineSchema,sparkSchema,groupSchema
from database.connection import clusters

class Cluster:
    def __init__(self,id:str=None, instance:clusterSchema=None):
        self.instance = None
        self.id = id
        if id:
            self.instance = clusters.find_one({"_id": id})
            self.instance = clusterSchema(**self.instance)
        if instance:
            self.new(instance)
            for key, value in instance.items():
                setattr(self, key, value)
    
    def __call__(self, *args, **kwds):
        pass

    def update(self,func):
        self.instance = clusterSchema(**clusters.find_one({"_id": self.instance._id}))
    
    def get(self,id:str = None) -> list[clusterSchema] | clusterSchema:
        """
        Retrieve all clusters from the database if no id is provided,
        or a specific cluster instance by its id.
        """
        if id:
            self.instance = Cluster(clusters.find_one({"_id": id}))
            return self.instance
        return list(clusters.find())
    
    def new(cluster_data:clusterSchema) -> clusterSchema:
        """
        Create a new cluster in the database.
        """
        new_cluster = clusterSchema(dict(**cluster_data))
        new_cluster = clusters.insert_one(dict(new_cluster))
        return new_cluster
    
    @update
    def newRole(self, role_data:roleSchema) -> roleSchema:
        """
        Create a new role in the cluster.
        """
        if not self.instance:
            raise ValueError("Cluster instance is not set. Please retrieve or create a cluster first.")
        
        role_data.cluster = self.instance.instance._id
        new_role = roleSchema(dict(**role_data))
        new_role = clusters.update_one({"_id": self.instance.instance._id}, {"$push": {"roles": dict(new_role)}})
        return new_role