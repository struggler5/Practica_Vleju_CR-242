from googleapiclient.discovery import build 

with open('API.txt', 'r') as file:
    API_KEY = file.read()
youtube = build(
    "youtube",
    "v3",
    developerKey=API_KEY
)

videos = []
result_int = 10
def Video_list_Search(query):
    response = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=result_int
    ).execute()

    items = response.get("items", [])



    for item in items:
        try:
            video_id = item["id"]["videoId"]
            title = item["snippet"]["title"]
        except:
            continue

        videos.append({
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })

    return videos

def watch_later():

    PLAYLIST_ID = "PLWm3Zfuu6T3I"
    request = youtube.playlistItems().list(part="snippet,contentDetails",
                                               playlistId=PLAYLIST_ID, 
                                           maxResults=result_int)
    response = request.execute()
    print(response.get("items"))
    for item in response.get("items"):
        title = item["snippet"]["title"]
        video_id = item["snippet"]["resourceId"]["videoId"]

        videos.append({
            "title": title,
            "url": f"https://www.youtube.com/watch?v={video_id}",
        })

    return videos
