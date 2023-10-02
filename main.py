from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date_input = input("what year you would like to travel to in YYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date_input}/")
contents = response.text

soup = BeautifulSoup(contents, "html.parser")

song_names = soup.select("li ul li h3")

song_list = [song.getText().strip() for song in song_names]

# -------------------------------------- Spotify Authorisation -------------------------------------------------------

client_id = "0d489c731f9544f7b0e490b5aba6c54b"
client_secret = "7f71b164a72e4a0397134513dd760784"
scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="https://www.billboard.com/",
        client_id=client_id,
        client_secret=client_secret,
        show_dialog=True,
        cache_path="token.txt",
        username="31357mm5v2xrh7gndtprogapuqla",
    )
)

user_id = sp.current_user()["id"]

# -------------------------------------- Making the playlist itself ---------------------------------------------------

song_uris = []
year = date_input.split("-")[0]
for song in song_list:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

play_id = sp.user_playlist_create(user=user_id, name=f"{date_input} Billboard 100",public=False)

sp.playlist_add_items(playlist_id=play_id["id"], items=song_uris)
