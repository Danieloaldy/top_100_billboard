import requests
from bs4 import BeautifulSoup
from datetime import datetime
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://example.com/",
        client_id="YOUR_ID",
        client_secret="YOUR_ID",
        show_dialog=True,
        cache_path="Token.txt",
        username="YOUR_USERNAME"
    )
)

user_id = sp.current_user()["id"]


#

date = input("Masukkan Tahun, Bulan dan Tanggal (YYYYMMDD) : ")
date = datetime.strptime(date,'%Y%m%d')
year = date.strftime('%Y')
month = date.strftime('%m')
day = date.strftime('%d')

billboard_link = f"https://www.billboard.com/charts/hot-100/{year}-{month}-{day}/"

response = requests.get(billboard_link)

website = response.text

website_html = BeautifulSoup(website,"html.parser")

song_title = website_html.select("li ul li h3")
title = [song_names.getText().strip() for song_names in song_title]
title_link = []

playlist = sp.user_playlist_create(user=user_id, name=f"{year}-{month}-{day} Billboard 100", public=False)


for song in title:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    try:
        uri = result["tracks"]["items"][0]["uri"]
        title_link.append(uri)
    except IndexError:
        print(f"{song} tidak tersedia di Spotify, Skip.")

sp.playlist_add_items(playlist_id=playlist["id"], items=title_link)
