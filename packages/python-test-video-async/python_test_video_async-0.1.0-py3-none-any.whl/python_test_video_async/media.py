from .exceptions import APIError
from .api import make_request

class MediaResource:
    def __init__(self, client):
        self.client = client
    
    async def get_all(self,params):
        """Fetch all medias."""
        try:
            return await make_request(
                method="GET", 
                endpoint="/on-demand", 
                headers=self.client.headers,
                params=params
            )
        except APIError as e:
            raise APIError(f"Failed to fetch medias: {str(e)}")

    async def get_by_id(self, media_id):
        """Fetch media by its ID."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return await make_request(
                method="GET", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to fetch media: {str(e)}")

    async def update(self, media_id, data):
        """Update media by its ID."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return await make_request(
                method="PATCH", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers,
                data=data
            )
        except APIError as e:
            raise APIError(f"Failed to update media: {str(e)}")

    async def delete(self, media_id):
        """Delete media by its ID."""
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            return await make_request(
                method="DELETE", 
                endpoint=f"/on-demand/{media_id}", 
                headers=self.client.headers
            )
        except APIError as e:
            raise APIError(f"Failed to delete media: {str(e)}")

    async def create_pull_video(self, data):
        """Create an on-demand request by calling the /on-demand endpoint."""
        endpoint = "/on-demand"
        
        if "accessPolicy" not in data:
            data["accessPolicy"] = "public"
        
        try:
            response = await make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
            return response
        except APIError as e:
            raise APIError(f"Failed to create on-demand request: {str(e)}")

    async def get_presigned_url(self, data):
        """Create an on-demand presigned URL request by calling the /on-demand/uploads endpoint."""
        endpoint = "/on-demand/uploads"
        
        if "corsOrigin" not in data:
            data["corsOrigin"] = "*"
        
        try:
            response = await make_request(
                method="POST", 
                endpoint=endpoint, 
                headers=self.client.headers, 
                data=data
            )
            return response
        except APIError as e:
            raise APIError(f"Failed to create presigned URL request: {str(e)}")
    
    async def get_media_info(self, media_id):
        """Retrieve media input info by media ID."""
        endpoint = f"/on-demand/{media_id}/input-info"
        
        if not media_id:
            raise ValueError("Media ID must be provided.")
        
        try:
            response = await make_request(
                method="GET", 
                endpoint=endpoint, 
                headers=self.client.headers
            )
            return response
        except APIError as e:
            raise APIError(f"Failed to retrieve media input info: {str(e)}")
            