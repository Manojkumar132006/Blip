"""
Cluster Controller - Handles all business logic for Cluster model
"""
from typing import List, Optional
from models.cluster import Cluster
from config.database import clusters as clusters_collection
from bson import ObjectId
import logging

logger = logging.getLogger(__name__)

class ClusterController:
    @staticmethod
    async def list_clusters() -> List[Cluster]:
        """List all clusters"""
        try:
            cursor = clusters_collection.find()
            clusters = await cursor.to_list(length=100)
            # Convert ObjectId to string for JSON serialization
            for cluster in clusters:
                cluster["_id"] = str(cluster["_id"])
            return [Cluster(**cluster) for cluster in clusters]
        except Exception as e:
            logger.error(f"Error listing clusters: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def get_cluster(cluster_id: str) -> Optional[Cluster]:
        """Get a specific cluster by ID"""
        try:
            cluster = await clusters_collection.find_one({"_id": ObjectId(cluster_id)})
            if not cluster:
                return None
            cluster["_id"] = str(cluster["_id"])
            return Cluster(**cluster)
        except Exception as e:
            logger.error(f"Error fetching cluster: {str(e)}")
            raise Exception(f"Database error: {str(e)}")

    @staticmethod
    async def create_cluster(cluster_data: dict) -> Cluster:
        """Create a new cluster"""
        try:
            # Remove _id if present in input
            cluster_data.pop('_id', None)
            result = await clusters_collection.insert_one(cluster_data)
            cluster_data["_id"] = str(result.inserted_id)
            return Cluster(**cluster_data)
        except Exception as e:
            logger.error(f"Error creating cluster: {str(e)}")
            raise Exception(f"Failed to create cluster: {str(e)}")

    @staticmethod
    async def update_cluster(cluster_id: str, cluster_data: dict) -> Optional[Cluster]:
        """Update an existing cluster"""
        try:
            cluster_data.pop('_id', None)  # Ensure _id is not updated
            result = await clusters_collection.update_one(
                {"_id": ObjectId(cluster_id)},
                {"$set": cluster_data}
            )
            if result.matched_count == 0:
                return None
            
            updated_cluster = await clusters_collection.find_one({"_id": ObjectId(cluster_id)})
            updated_cluster["_id"] = str(updated_cluster["_id"])
            return Cluster(**updated_cluster)
        except Exception as e:
            logger.error(f"Error updating cluster: {str(e)}")
            raise Exception(f"Failed to update cluster: {str(e)}")

    @staticmethod
    async def delete_cluster(cluster_id: str) -> bool:
        """Delete a cluster"""
        try:
            result = await clusters_collection.delete_one({"_id": ObjectId(cluster_id)})
            return result.deleted_count > 0
        except Exception as e:
            logger.error(f"Error deleting cluster: {str(e)}")
            raise Exception(f"Failed to delete cluster: {str(e)}")
