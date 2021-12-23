from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import os

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
# Need to go https://developer.spotify.com/dashboard > Edit Settings > Add SPOTIPY_REDIRECT_URI to redirect URI too > Save
SPOTIPY_REDIRECT_URI = "http://example.com"

date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

response = requests.get(f"https://www.billboard.com/charts/hot-100/{date}/")
content = response.text
soup = BeautifulSoup(content, "html.parser")
songs = [song.getText().strip() for song in soup.select(selector="div ul li h3")][:100]
# Eg. 2001-12-29: ['How You Remind Me', 'U Got It Bad', 'Family Affair', 'Get The Party Started', 'Hero', 'Whenever, Wherever', 'Always On Time', 'Differences', 'My Sacrifice', "Livin' It Up", "A Woman's Worth", 'Turn Off The Light', 'Gone', "Superman (It's Not Easy)", 'Wherever You Will Go', 'Rock The Boat', 'I Do!!', "I'm Real", 'Only Time', 'Where The Stars And Stripes And The Eagle Fly', 'Butterflies', "We Thuggin'", 'Caramel', "Fallin'", '#1', 'In The End', 'Hey Baby', 'Son Of A Gun', 'Emotion', 'Where Were You (When The World Stopped Turning)', "It's Been Awhile", 'Dig In', 'I Wanna Talk About Me', 'Roll Out (My Business)', '7 Days', 'Standing Still', 'Run', 'Lights, Camera, Action!', 'Good Morning Beautiful', 'Hanging By A Moment', 'Break Ya Neck', 'Drops Of Jupiter (Tell Me)', 'Riding With Private Malone', "I'm Tryin'", 'Alive', 'Wrapped Up In You', "Bouncin' Back (Bumpin' Me Against The Wall)", 'Wrapped Around', 'You Gets No Love', 'Raise Up', 'The Whole World', 'Girls, Girls, Girls', 'No More Drama', 'Blurry', 'Lifetime', 'Bring On The Rain', "Can't Fight The Moonlight", 'Everywhere', "The World's Greatest", 'Take Away', 'Brotha', "Young'n (Holla Back)", 'Ooohhhwee', "I'm A Slave 4 U", 'Goodbye', 'The Long Goodbye', 'Love Of A Woman', "Let's Stay Home Tonight", 'Wish You Were Here', 'Welcome To Atlanta', 'With Me', 'Dance With Me', 'God Bless The USA', "Ain't It Funny", 'From Her Mama (Mama Got A**)', 'Fade', "Don't You Forget It", "Stuck In A Moment You Can't Get Out Of", 'Smooth Criminal', 'Drowning', 'Never Too Far/Hero Medley', 'AM To PM', 'Where I Come From', 'Love Of My Life', 'Part II', 'Control', 'Angry All The Time', 'Ugly', 'The Star Spangled Banner', 'You Rock My World', 'Fatty Girl', "Feelin' On Yo Booty", 'Got Ur Self A...', 'What Am I Gonna Do', "I'm A Survivor", 'Do U Wanna Roll (Dolittle Theme)', 'What If', 'Round And Round', 'God Bless America', 'Who We Be', 'Account']
# for some reason, can't extract artist name via 1.find class_ cos the variables inside depend on window size or sth, 2.selector cos div ul li span gives other info like Likes, Facebook, Share, etc irrelevant data

# Spotipy API: https://spotipy.readthedocs.io/en/2.19.0/
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_CLIENT_SECRET, redirect_uri=SPOTIPY_REDIRECT_URI, scope="playlist-modify-private", show_dialog=True, cache_path="token.txt"))
user = sp.current_user()['id']
year = date.split("-")[0]
track_uris = []
i = 0

for song in songs:
    i += 1
    try: track_uris.append(sp.search(q=f'track:{song} year:{year}', type='track')["tracks"]["items"][0]["uri"])
    except IndexError or KeyError: print(f"Number {i}: {song} not found!")
playlist_id = sp.user_playlist_create(user=user, name=f"{date} BillBoard 100", public=False, description=f"Top 100 music from {date}!")
sp.playlist_add_items(playlist_id["id"], track_uris)





