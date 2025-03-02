import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os
from dotenv import load_dotenv
load_dotenv()

ENDPOINT = "https://api.spotify.com/v1/users/smedjan/playlists"
client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRETE")

date = input("Enter a date (YYYY-MM-DD): ")
url = "https://www.billboard.com/charts/hot-100/" +date

header = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36"}
response = requests.get(url=url, headers= header )
website_data = response.text
soup = BeautifulSoup(website_data, "html.parser")
song_name = soup.select(" li ul li h3")
song = [songs.getText().split() for songs in song_name]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="Anjali Chuahan",
    )
)
user_id = sp.current_user()["id"]






song_uris = []
year = date.split("-")[0]
for songs in song:
    result = sp.search(q=f"track:{songs} year:{year}",
                        type="track",
                       market='US',
                       limit="1"
                       )

    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")
print(song_uris)
playlist = sp.user_playlist_create(user=user_id, name=f"Billboard {year}", public=False)
playlist_id = playlist["id"]

sp.playlist_add_items(playlist_id=playlist_id, items=song_uris)