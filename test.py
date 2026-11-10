
from googleapiclient.discovery import build 

with open('API.txt', 'r') as file:
    API_KEY = file.read()
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)


PLAYLIST_ID = "PLWm3Zfuu6T3I"
request = youtube.playlistItems().list(part="snippet,contentDetails",
                                           playlistId=PLAYLIST_ID, maxResults=10)
response = request.execute()
for item in response.get("items"):
    title = item["snippet"]["title"]
    print(title)
