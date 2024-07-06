import googleapiclient.discovery
import googleapiclient.errors
from dotenv import load_dotenv
import os
import process

load_dotenv()

api_service_name = "youtube"
api_version = "v3"

# load the api key fron the .env file
DEVELOPER_KEY = os.getenv("YSA_DATA_API_KEY")

youtube = googleapiclient.discovery.build(
    api_service_name, api_version, developerKey=DEVELOPER_KEY
)

def getComments(videoId, maxResults):
    """
    Fetches the comments from a YouTube video
    
    Parameters:
    videoId (str): The ID of the YouTube video
    maxResults (int): The maximum number of comments to fetch
    
    Returns:
    list: The comments from the video
    """
    maxResults = int(maxResults)  # Convert maxResults to an integer
    comments = []
    pageToken = None

    while len(comments) < maxResults:
        request = youtube.commentThreads().list(
            part="snippet", videoId=videoId, maxResults=min(100, maxResults - len(comments)), pageToken=pageToken
        )
        response = request.execute()

        for item in response["items"]:
            comment = (item["snippet"]["topLevelComment"]["snippet"]["textDisplay"])
            cleaned = process.cleanText(comment)
            comments.append(cleaned)

        if "nextPageToken" in response:
            pageToken = response["nextPageToken"]
        else:
            break

    return comments

def getTitle(videoId):
    """
    Fetches the title of a YouTube video
    
    Parameters:
    videoId (str): The ID of the YouTube video
    
    Returns:
    str: The title of the video
    """
    request = youtube.videos().list(part="snippet", id=videoId)
    response = request.execute()

    return response["items"][0]["snippet"]["title"]

def getCommentCount(videoId):
    """
    Fetches the comment count of a YouTube video
    
    Parameters:
    videoId (str): The ID of the YouTube video
    
    Returns:
    str: The comment count of the video
    """
    request = youtube.videos().list(part="statistics", id=videoId)
    response = request.execute()

    return response["items"][0]["statistics"]["commentCount"]

def getThumbnailURL(videoId):
    """
    Fetches the thumbnail URL of a YouTube video

    Parameters:
    videoId (str): The ID of the YouTube video

    Returns:
    str: The thumbnail URL of the video
    """
    request = youtube.videos().list(part="snippet", id=videoId)
    response = request.execute()

    # Get the default thumbnail URL
    default_thumbnail_url = response["items"][0]["snippet"]["thumbnails"]["default"][
        "url"
    ]

    # Replace "default.jpg" with "maxresdefault.jpg"
    maxres_thumbnail_url = default_thumbnail_url.replace(
        "default.jpg", "maxresdefault.jpg"
    )

    return maxres_thumbnail_url

def getChannelTitle(videoId):
    """
    Fetches the channel title of a YouTube video

    Parameters:
    videoId (str): The ID of the YouTube video

    Returns:
    str: The channel title of the video
    """
    request = youtube.videos().list(part="snippet", id=videoId)
    response = request.execute()

    return response["items"][0]["snippet"]["channelTitle"]

def getDatePublished(videoId):
    """
    Fetches the date published of a YouTube video

    Parameters:
    videoId (str): The ID of the YouTube video

    Returns:
    str: The date published of the video
    """
    request = youtube.videos().list(part="snippet", id=videoId)
    response = request.execute()

    date = response["items"][0]["snippet"]["publishedAt"]

    # Format the date
    date = date.split("T")[0]
    return date

def getLikeCount(videoId):
    """
    Fetches the like count of a YouTube video

    Parameters:
    videoId (str): The ID of the YouTube video

    Returns:
    str: The like count of the video
    """
    request = youtube.videos().list(part="statistics", id=videoId)
    response = request.execute()

    return response["items"][0]["statistics"]["likeCount"]