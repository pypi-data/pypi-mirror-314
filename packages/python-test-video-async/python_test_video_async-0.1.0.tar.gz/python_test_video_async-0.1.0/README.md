# Introduction:

The FastPix Python SDK simplifies integration with the FastPix platform. This SDK is designed for secure and efficient communication with the FastPix API, enabling easy management of media uploads, live streaming, and simulcasting. It is intended for use with Python 3.7 or later.

# Key Features:

- ## Media API:

  - **Upload Media**: Upload media files seamlessly from URLs or devices.
  - **Manage Media**: Perform operations such as listing, fetching, updating, and deleting media assets.
  - **Playback IDs**: Generate and manage playback IDs for media access.

- ## Live API:

  - **Create & Manage Live Streams:**: Create, list, update, and delete live streams effortlessly.
  - **Control Stream Access**: Generate playback IDs for live streams to control and manage access.
  - **Simulcast to Multiple Platforms**: Stream content to multiple platforms simultaneously.

For detailed usage, refer to the [FastPix API Reference](https://docs.fastpix.io/reference).

# Prerequisites:

## Getting started with FastPix:

To get started with the **FastPix Python SDK**, ensure you have the following:

- The FastPix APIs are authenticated using an **Access Token** and a **Secret Key**. You must generate these credentials to use the SDK.

- Follow the steps in the [Authentication with Access Tokens](https://docs.fastpix.io/docs/authentication-with-access-tokens) guide to obtain your credentials.

# Installation:

To install the SDK, you can use pip:

```bash
pip3 install python_async_api
```

# Basic Usage:

## Importing the SDK

```python
from python_async_api.client import VideoSDKClient
```

# Initialization:

Initialize the FastPix SDK with your API credentials.

```python
from python_async_api.client import VideoSDKClient

client = VideoSDKClient(username="your-access-token-id", password="your-secret-key")
```

## Example Usage:

Below is an example of configuring `FastPix Python SDK` into your project.

```python
from python_async_api.client import VideoSDKClient
 
client = VideoSDKClient(username=username, password=password)
      
try:
    media = await client.media.get_all()
    print("Media:", media)
except Exception as e:
    print(f"Error fetching media: {str(e)}")
 
if __name__ == "__main__":
    main()
```

# Usage:

## 1. Media Operations:

### 1.1. Media Uploads:

#### Upload Media from a URL:

Use the `client.media.create_pull_video` method to upload media directly from a URL. For detailed configuration options, refer to the [Create media from URL](https://docs.fastpix.io/reference/create-media) API documentation.

```python
# Define the request payload for uploading media from a URL.
mediaFromUrlRequest = {
"inputs": [{
  "type": "video", # Specifies the type of media being uploaded (e.g., "video").
  "url": "https://static.fastpix.io/sample.mp4" # URL of the media file to be uploaded.
 }],
"metadata": {
  "video_title": "Big_Buck_Bunny" # Metadata to associate with the media, such as its title.
},
"accessPolicy": "public", # Access policy for the media ("public" or "private").
"maxResolution": "1080p"
}

media_response = await client.media.create_pull_video(mediaFromUrlRequest)
print("media_response", media_response)
```

#### Upload Media from a Local Device:

Use the `client.media.get_presigned_url` method to obtain a `signedUrl` and upload media directly from a local device. For more details on configuration options, refer to the [Upload media from device](https://docs.fastpix.io/reference/direct-upload-video-media) API documentation.

```python
# Define the request payload for uploading media from a device.
mediaFromDeviceRequest = {
  "corsOrigin": "*", # Specifies the allowed origin for CORS (Cross-Origin Resource Sharing). "*" allows all origins.
  "pushMediaSettings": {
    "accessPolicy": "private", # Sets the access policy for the uploaded media (e.g., "private" or "public").
    "optimizeAudio": true, # Enables audio optimization for the uploaded media.
    "maxResolution": "1080p", # Specifies the maximum resolution allowed for the uploaded media.
  },
}

mediaFromDeviceResponse = await client.media.get_presigned_url(mediaFromDeviceRequest)
print("Upload Response:", mediaFromDeviceResponse)
```

### 1.2. Media Management:

#### Get List of All Media:

Use the `client.media.get_all` method to fetch a list of all media assets. You can customize the query by modifying parameters such as `limit`, `offset`, and `orderBy`. Refer to the [Get list of all media](https://docs.fastpix.io/reference/list-media) API documentation for the accepted values.

```python
# Define the parameters for fetching media assets in a separate variable.
media_asset_request_params = {
    "limit": 10,  # Number of media assets to fetch in one request.
    "offset": 1,  # Starting position for the list of media assets (useful for pagination).
    "orderBy": "desc",  # Sort order for the media assets ("desc" for descending, "asc" for ascending).
}

# Assuming `client` is already initialized with the proper credentials
all_media_assets = await client.media.get_all(media_asset_request_params)

# Print the fetched media assets
print("All Media Assets:", all_media_assets)
```

#### Get Media Asset by ID:

Use the `client.media.get_by_id` method to retrieve a specific media asset by its ID. Provide `mediaId`of the asset to fetch its details. Refer to the [Get a media by ID](https://docs.fastpix.io/reference/get-media) API documentation for more details.

```python
media_id = "mediaId"  # Unique identifier for the media asset to be retrieved

get_media_asset = await client.media.get_by_id(media_id)

# Print the retrieved media asset by ID
print("Retrieved media asset by ID:", get_media_asset)
```

#### Update Media Asset:

Use the `client.media.update` method to update metadata or other properties of a specific media asset. Provide the `mediaId` of the asset along with the metadata to be updated. Refer to the [Update a media by ID](https://docs.fastpix.io/reference/updated-media) API documentation for more details.

```python
media_id = "mediaId"  # Unique identifier for the media asset to be retrieved

# Define the payload with the updates to be applied to the media asset.
update_payload = {
    "metadata": {
        "key": "value",  # Replace "key" and "value" with actual metadata keys and values
    },
}

update_media_asset = await client.media.update(media_id, update_payload)

# Print the updated media asset details
print("Updated Media Asset:", update_media_asset)
```

#### Delete Media Asset:

Use the `client.media.delete` method to delete a specific media asset by its ID. Pass the `mediaId` of the asset you want to delete. Refer to the [Delete a media by ID](https://docs.fastpix.io/reference/delete-media) API documentation for more information.

```python
media_id = "mediaId"  # Unique identifier for the media asset to be retrieved

# Assuming `client` is already initialized with the necessary credentials
delete_media_asset = await client.media.delete(media_id)

# Print the response indicating the media asset has been deleted
print("Deleted Media Asset:", delete_media_asset)
```

#### Get Media Asset Info:

Use the `client.media.get_media_info` method to retrieve detailed information about a specific media asset. Pass the `mediaId` to fetch its details. Refer to the [Get info of media inputs](https://docs.fastpix.io/reference/retrievemediainputinfo) API documentation for more details.

```python
media_id = "mediaId"  # Unique identifier for the media asset to be retrieved

getMediaInfo = await client.media.get_media_info(media_id)
print("Media Asset Info:", getMediaInfo)
```

### 1.3. Manage Media Playback:

#### Generate Media Playback ID:

Use the `client.media_playback_ids.create` method to generate a playback ID for a specific media asset. You can pass an `mediaId` and configure options such as the `accessPolicy`. For detailed configuration options, refer to the [Create a playback ID](https://docs.fastpix.io/reference/create-media-playback-id) API documentation.

```python
# Define the mediaId and accessPolicy dynamically

mediaId =  "media-id", # Unique identifier for the media asset.

playbackOptions = {
  accessPolicy: "public", # Can be 'public' or 'private'.
}

playbackIdResponse = await client.media_playback_ids.create(media_id=mediaId, data=playbackOptions)

print("Playback ID Creation Response:", playbackIdResponse)
```

#### Delete Media Playback ID:

Use the `client.media_playback_ids.delete()` method to delete a playback ID for a specific media asset. You need to pass both the `mediaId` and the `playbackId` to delete the playback ID. For detailed configuration options, refer to the [Delete a playback ID](https://docs.fastpix.io/reference/delete-media-playback-id) API documentation.

```python
# Define the mediaId and playbackId dynamically
media_id = "media-id"; # The ID of the media asset for which you want to delete the playback ID.
playback_ids = ["id1", "id2"]; # The playback ID that you want to delete.

deletePlaybackResponse = await client.media_playback_ids.delete(media_id, playback_ids)

print("Playback ID Deletion Response:", deletePlaybackResponse)
```

----

## 2. Live Stream Operations:

### 2.1. Start Live Stream:

Use the `client.livestreams.create()` method to start a live stream with specific configurations. For detailed configuration options, refer to the [Create a new stream](https://docs.fastpix.io/reference/create-new-stream) API documentation.

```python
liveStreamRequest = {
  "playbackSettings": {
    "accessPolicy": "public", # Defines the access level of the live stream (public or private)
  },
  "inputMediaSettings": {
    "maxResolution": "1080p", # Set the maximum resolution of the live stream
    "reconnectWindow": 1800, # Set the duration for reconnecting the stream in seconds
    "mediaPolicy": "private", # Define media policy (private or public)
    "metadata": {
      "liveStream": "fp_livestream", # Custom metadata for the live stream
    },
    "enableDvrMode": true, # Enable DVR mode to allow viewers to rewind the live stream
  },
}

# Initiating the live stream
generateLiveStream = await client.livestreams.create(liveStreamRequest)
print("Live Stream initiated successfully:", generateLiveStream)
```

### 2.2. Live Stream Management:

#### Get List of All Live Streams:

Use the `client.livestreams.list()` method to fetch a list of all live streams. You can customize the query by modifying parameters such as `limit`, `offset`, and `orderBy`. For detailed configuration options, refer to the [Get all live streams](https://docs.fastpix.io/reference/get-all-streams) API documentation.

```python
getAllLiveStreamPagination = {
  limit: 10, # Limit the number of live streams retrieved.
  offset: 1, # Skip a specified number of streams for pagination.
  orderBy: "asc", # Order the results based on the specified criteria ("asc" or "desc").
}

const getAllLiveStreams = await client.livestreams.list(getAllLiveStreamPagination)
print("All Live Streams:", getAllLiveStreams)
```

#### Get Live Stream by ID:

Use the `client.livestreams.get()` method to retrieve a specific live stream by its ID. Provide the `streamId` of the stream you wish to fetch. For more details, refer to the [Get stream by ID](https://docs.fastpix.io/reference/get-live-stream-by-id) API documentation.

```python
streamId =  "a09f3e958c16ed00e85bfe798abd9845" # Replace with actual stream ID
getLiveStreamById = await client.livestreams.get(streamId)

print("Live Stream Details:", getLiveStreamById)
```

#### Update Live Stream:

Use the `client.livestreams.update()` method to update a live stream's configuration. Provide the `streamId` of the stream and specify the fields you want to update. For more details, refer to the [Update a stream](https://docs.fastpix.io/reference/update-live-stream) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845" # Provide the stream ID for the live stream to update
 updateLiveStreamRequest = {
  "metadata": {
    "livestream_name": "Game_streaming",
  },
  "reconnectWindow": 100,
}

updateLiveStream = await client.livestreams.update(stream_id,updateLiveStreamRequest)

print("Updated Live Stream:", updateLiveStream)
```

#### Delete Live Stream:

Use the `client.livestreams.delete()` method to delete a live stream by its ID. Provide `streamId` of the stream you want to delete. For more details, refer to the [Delete a stream](https://docs.fastpix.io/reference/delete-live-stream) API documentation.

```python
deleteLiveStream = await client.livestreams.delete("a09f3e958c16ed00e85bfe798abd9845")  # Provide the stream ID of the live stream to delete
print("Deleted Live Stream:", deleteLiveStream)
```

### 2.3. Manage Live Stream Playback:

#### Generate Live Stream Playback ID:

Use the `client.livestream_playback_ids.create()` method to generate a playback ID for a live stream. Replace `streamId` with the actual ID of the live stream and specify the desired `accessPolicy`. For more details, refer to the [Create a playback ID](https://docs.fastpix.io/reference/create-playbackid-of-stream) API documentation.

```python

stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
body = { accessPolicy: "public" }

generateLiveStreamPlaybackId = await client.livestream_playback_ids.create(stream_id, body)

print("Generated Live Stream Playback ID:", generateLiveStreamPlaybackId)
```

#### Delete Live Stream Playback ID:

Use the `client.livestream_playback_ids.delete()` method to delete a specific playback ID for a live stream. You need to provide both the `streamId` of the live stream and the `playbackId` to delete. For more details, refer to the [Delete a playback ID](https://docs.fastpix.io/reference/delete-playbackid-of-stream) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
playback_id = "632029b4-7c53-4dcf-a4d3-1884c29e90f8"  # Replace with actual playback ID

deleteLiveStreamPlaybackId = await client.livestream_playback_ids.delete(stream_id, playback_id)

print("Deleted Live Stream Playback ID:", deleteLiveStreamPlaybackId)
```

#### Get Live Stream Playback Policy:

Use the `client.livestream_playback_ids.get()` method to retrieve the playback policy for a specific live stream playback ID. Replace `streamId` with the stream's ID and `playbackId` with the actual playback ID to fetch the policy. For more details, refer to the [Get stream's playback ID](https://docs.fastpix.io/reference/get-live-stream-playback-id) API documentation.

```python
stream_id = "1c5e8abcc2080cba74f5d0ac91c7833e"  # Replace with the actual stream ID
playback_id = "95ce872d-0b58-44f3-be72-8ed8b97ee2c9"  # Replace with the actual playback ID

getLiveStreamPlaybackPolicy = await client.livestream_playback_ids.get(stream_id, playback_id)

print("Live Stream Playback Policy:", getLiveStreamPlaybackPolicy)
```

### 2.4. Manage Live Stream Simulcast:

#### Initiate Live Stream Simulcast:

Use the `client.livestreams.create_simulcast()` method to create a new simulcast for a live stream. Provide the stream ID and simulcast payload with the URL and stream key. For more details, refer to the [Create a simulcast](https://docs.fastpix.io/reference/create-simulcast-of-stream) API documentation.

```python
simulcast_payload = {
    "url": "rtmps://live.fastpix.io:443/live",
    "streamKey": "46c3457fa8a579b2d4da64125a2b6e83ka09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream key
}

stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID

generateSimulcast = await client.livestream_simulcasts.create(stream_id, simulcast_payload)

print("Generate Simulcast:", generateSimulcast)
```

#### Get Live Stream Simulcast:

Use the `client.livestreams.get_simulcast()` method to retrieve details of a specific simulcast stream. Provide the `streamId` and `simulcastId` of the simulcast you want to fetch. For more details, refer to the [Get a specific simulcast of a stream](https://docs.fastpix.io/reference/get-specific-simulcast-of-stream) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
simulcast_id = "7269209ff0299319b6321c9a6e7850ff"  # Replace with actual simulcast ID

getLiveSimulcast = await client.livestream_simulcasts.get_simulcast(stream_id, simulcast_id)

print("Live Stream Simulcast Details:", getLiveSimulcast)
```

#### Update Live Stream Simulcast:

Use the `client.livestreams.update_simulcast()` method to update the configuration of a simulcast stream. Provide the `streamId`, `simulcastId`, and the fields you want to update. For more details, refer to the [Update a specific simulcast of a stream](https://docs.fastpix.io/reference/update-specific-simulcast-of-stream) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
simulcast_id = "7269209ff0299319b6321c9a6e7850ff"  # Replace with actual simulcast ID

update_payload = {
    "isEnabled": False,  # Disable the simulcast stream (set to True to enable)
    "metadata": {
        "simulcast2": "media"  # Update the metadata as needed
    }
}

updateLiveSimulcast = await client.livestreams.update_simulcast(stream_id, simulcast_id, update_payload)

print("Updated Live Stream Simulcast:", updateLiveSimulcast)
```

#### Delete Live Stream Simulcast:

Use the `client.livestreams.delete_simulcast()` method to remove a specific simulcast from a live stream. Provide the `streamId` and `simulcastId` for the simulcast you want to delete. For more details, refer to the [Delete a simulcast](https://docs.fastpix.io/reference/delete-simulcast-of-stream) API documentation.

```python
stream_id = "a09f3e958c16ed00e85bfe798abd9845"  # Replace with actual stream ID
simulcast_id = "7269209ff0299319b6321c9a6e7850ff"  # Replace with actual simulcast ID

deleteLiveSimulcast = await client.livestreams.delete_simulcast(stream_id, simulcast_id)

print("Deleted Live Stream Simulcast:", deleteLiveSimulcast)
```

## Detailed Usage:

For a complete understanding of each API's functionality, including request and response details, parameter descriptions, and additional examples, please refer to the [FastPix API Reference](https://docs.fastpix.io/reference/signingkeys-overview).

The API reference provides comprehensive documentation for all available endpoints and features, ensuring developers can integrate and utilize FastPix APIs efficiently.
