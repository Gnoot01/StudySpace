"""
Personally feel YT Premium > Spotify, but most around me are stuck on Spotify and lazy/unable to transfer playlists. As such, API/Scraping to convert YT<->SP playlists
YT -> Spotify: more stringent due to Spotify's search terms and verified quality songs only.
Spotify -> YT: much easier. YT API works smoother, but has a quota of 10000/day with diff cost/CRUD function. Scraping works better as CRUD via normal user interface is not limited, but impractical limiting scalability (since need to log in to clone playlist)
"pip install emoji --upgrade" to manipulate emoji unicodes: https://github.com/carpedm20/emoji,
Google API Python Client: https://github.com/googleapis/google-api-python-client
1. go https://console.cloud.google.com, create "New Project"
2. Click menu icon on top left > "API & Services" > "Enable APIS and Services" > Search "Youtube Data API" > Enable
3. YT_API_KEY: "Credentials" > "Create Credentials" + "pip install google-api-python-client" (limited functionality etc as unable to scope)
   OAuth client ID: "OAuth consent screen" (Add test user) > "External" + "Credentials" > "Create Credentials" > "Web Application", Name, Redirect_URIS: http://localhost:8080/, download client_secrets.json + "pip install google-auth" + "pip install google-auth-oauthlib", OAuth scopes: https://developers.google.com/youtube/v3/guides/auth/installed-apps

Undetected Chrome is abit quirky (requires if __name__=="__main__", must be on screen, headless mode is not undetected)
Alternative methods:
1. using Firefox. As Chrome is created by Google, allegedly Google can easily/better detect if Selenium is being used on Chrome and hence block it.
2. Logging in via StackOverflow Google Auth first: https://accounts.google.com/o/oauth2/auth/identifier?client_id=717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com&scope=profile%20email&redirect_uri=https%3A%2F%2Fstackauth.com%2Fauth%2Foauth2%2Fgoogle&state=%7B%22sid%22%3A1%2C%22st%22%3A%2259%3A3%3Abbc%2C16%3A561fd7d2e94237c0%2C10%3A1599663155%2C16%3Af18105f2b08c3ae6%2C2f06af367387a967072e3124597eeb4e36c2eff92d3eef6971d95ddb5dea5225%22%2C%22cdl%22%3Anull%2C%22cid%22%3A%22717762328687-iludtf96g1hinl76e4lc1b9a82g457nn.apps.googleusercontent.com%22%2C%22k%22%3A%22Google%22%2C%22ses%22%3A%2226bafb488fcc494f92c896ee923849b6%22%7D&response_type=code&flowName=GeneralOAuthFlow,
   then get to the actual website, authenticated.
   Poor implementation due to 1) User has to create/login StackOverflow first?? (Unintended additional permissions/side effects limits scalability) 2) Will not work if previously tried logging in via normal Selenium and gotten the "This browser or app may not be secure" page, as account already blacklisted by Google
3. Loading chrome profiles already logged into the google accounts. (chrome_options.add_argument("--user-data-dir=C:/Users/{userName}/AppData/Local/Google/Chrome/User Data/Profile {#} OR Default/")
   Poor implementation due to 1) User has to create/send over profile/log in via the local computer first? 2) Using profile already in use (opened in another chrome window) causes error

Enhancement: Instead of 3. (Formatting and checking via name), Machine Learning to recognise music tone, beat, rhythm to check if it is the same song?
"""

import datetime
import time
import os
import emoji
import chromedriver_autoinstaller
from selenium import webdriver
from selenium.common.exceptions import InvalidArgumentException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

SP_CLIENT_ID = os.environ.get("SP_CLIENT_ID")
SP_CLIENT_SECRET = os.environ.get("SP_CLIENT_SECRET")
SP_REDIRECT_URI = os.environ.get("SP_REDIRECT_URI")
# YT_API_KEY = os.environ.get("YT_API_KEY")
ARTISTS_TO_WATCH = ["IU", "BTS", "王七七"]
VERSIONS_TO_WATCH = ["instrumental", "karaoke", "piano", "violin", "cover", "acoustic", "drum"]
YT_USERNAME = os.environ.get("YT_USERNAME")
YT_PASSWORD = os.environ.get("YT_PASSWORD")


def track_format(string: str):
    return emoji.replace_emoji(string.replace('.', '').replace("_", "").replace("'", ""), replace='').strip()


def ceiling_hundred(a_list: list):
    return (int(len(a_list) / 100) + 2) * 100


def yt_to_sp(YT_URL: str, SP_URL: str):
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SP_CLIENT_ID, client_secret=SP_CLIENT_SECRET, redirect_uri=SP_REDIRECT_URI, scope="playlist-modify-public", show_dialog=True, cache_path="token.txt"))
    user = sp.current_user()['id']
    date = datetime.datetime.today().strftime("%d %b %Y")
    # Youtube -> Spotify
    # 1. Get Youtube songs
    chromedriver_autoinstaller.install()
    driver = webdriver.Chrome()
    try:
        driver.get(YT_URL)
    except InvalidArgumentException:
        print("Invalid link!")
        return
    yt_page = driver.find_element("tag name", "html")
    last_result = None
    new_result = 0
    while last_result != new_result:
        last_result = new_result
        new_result = driver.execute_script("return arguments[0].scrollTop = arguments[0].scrollHeight", yt_page)
        time.sleep(1)
    yt_tracks = WebDriverWait(driver, 3).until(EC.presence_of_all_elements_located(("id", 'video-title')))
    yt_tracks_iterate_copy = yt_tracks.copy()
    yt_track_uris = []
    for i in range(100, ceiling_hundred(yt_tracks_iterate_copy), 100):
        for yt_track in yt_tracks_iterate_copy[:100]:
            formatted_yt_track = track_format(yt_track.text.split("(")[0])
            # Edge case: (Lyrics) ...
            if not len(formatted_yt_track): formatted_yt_track = track_format(yt_track.text.split(")")[1])
            # [MV] IU, BTS, 王七七
            if len(formatted_yt_track) < 8:
                for word in ARTISTS_TO_WATCH:
                    if word in formatted_yt_track:
                        formatted_yt_track = track_format(yt_track.text.split(")")[1].split("(")[0])
                        break
            try:
                # Will only check top 5 results if one of VERSIONS_TO_WATCH
                yt_track_items = sp.search(f"track:{formatted_yt_track}", limit=5)["tracks"]["items"][:5]
                for yt_track_item in yt_track_items:
                    desired = True
                    for version in VERSIONS_TO_WATCH:
                        if version in yt_track_item["name"].lower():
                            desired = False
                            break
                    if desired:
                        yt_track_uris.append(yt_track_item["uri"])
                        break
            except IndexError:
                with open("yt_songs_not_found_in_spotify.txt", "w") as handler:
                    handler.write(f"Song: {formatted_yt_track}\n")
        yt_tracks_iterate_copy = yt_tracks[i:]

    # 2. Clone playlist to add to (Add to my Library)
    if SP_URL == "https://open.spotify.com/":
        sp_playlist_to_clone = input("Input a name for your Spotify Playlist!: ")
        sp_new_playlist_id = sp.user_playlist_create(user=user, name=sp_playlist_to_clone, public=True, description="Youtube -> Spotify")["id"]
    else:
        if "?" in SP_URL: SP_URL = SP_URL.split("?")[0]
        driver.get(SP_URL)
        sp_playlist_to_clone = "New " + WebDriverWait(driver, 10).until(EC.presence_of_element_located(('xpath', '//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/div/section/div[1]/div[5]/span/h1'))).text + " " + date
        # Spotipy uses pagination, default limit on 1 page = 100, so need while loop to get full list
        results = sp.playlist_items(SP_URL.split("playlist/")[1])
        sp_tracks = results["items"]
        while results['next']:
            results = sp.next(results)
            sp_tracks.extend(results['items'])
        sp_track_uris = [track["track"]["uri"] for track in sp_tracks]
        sp_track_uris_copy = sp_track_uris.copy()
        sp_track_uris_iterate_copy = sp_track_uris.copy()
        sp_new_playlist_id = sp.user_playlist_create(user=user, name=sp_playlist_to_clone, public=True, description="Youtube -> Spotify")["id"]
        for i in range(100, ceiling_hundred(sp_track_uris_iterate_copy), 100):
            sp.playlist_add_items(sp_new_playlist_id, sp_track_uris_iterate_copy[:100])
            sp_track_uris_iterate_copy = sp_track_uris[i:]

        yt_track_uris = [yt_track_uri for yt_track_uri in yt_track_uris if yt_track_uri not in sp_track_uris_copy]

    # 3. Add Youtube songs to sp_new_playlist, don't add duplicate
    yt_track_uris_iterate_copy = yt_track_uris.copy()
    for i in range(100, ceiling_hundred(yt_track_uris_iterate_copy), 100):
        sp.playlist_add_items(sp_new_playlist_id, yt_track_uris_iterate_copy[:100])
        yt_track_uris_iterate_copy = yt_track_uris[i:]

    driver.quit()
    print(f"See your created playlist at https://open.spotify.com/playlist/{sp_new_playlist_id}")
#############################################################################################################################################################################################
def add_to_yt_playlist(uc_driver, playlist_name: str):
    yt_playlists = WebDriverWait(uc_driver, 3).until(EC.presence_of_all_elements_located(("css selector", '#playlists #checkbox')))
    for i in range(0, len(yt_playlists), 2):
        if yt_playlists[i].find_element("id", "label").text == playlist_name and "checked" not in yt_playlists[i].find_element("css selector", "#checkbox").get_attribute("class"):
            yt_playlists[i].click()
            break


def sp_to_yt(YT_URL: str, SP_URL: str):
    # Spotify -> Youtube
    # 1. Get Spotify songs
    sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SP_CLIENT_ID, client_secret=SP_CLIENT_SECRET, redirect_uri=SP_REDIRECT_URI, scope="playlist-modify-public", show_dialog=True, cache_path="token.txt"))
    try:
        results = sp.playlist_items(SP_URL.split("playlist/")[1])
    except IndexError:
        print("Invalid link!")
        return
    sp_tracks = results["items"]
    while results['next']:
        results = sp.next(results)
        sp_tracks.extend(results['items'])
    sp_tracks = [f'{track["track"]["name"]} by {", ".join([artist["name"] for artist in track["track"]["artists"]])}' for track in sp_tracks]

    # 2. Clone existing playlist to add to (Authorise script to log in)
    date = datetime.datetime.today().strftime("%d %b %Y")
    credentials = None

    # retrieves token.pickle from previously successful logins' user's credentials
    if os.path.exists('token.pickle'):
        print('Loading Credentials From File...')
        with open('token.pickle', 'rb') as token: credentials = pickle.load(token)

    # If there are no valid credentials available, then either refresh the token or log in.
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            print('Refreshing Access Token...')
            credentials.refresh(Request())
        else:
            print('Fetching New Tokens...')
            flow = InstalledAppFlow.from_client_secrets_file("client_secrets.json", scopes=["https://www.googleapis.com/auth/youtube.force-ssl"])

            # prompt needed as sometimes only access tokens (short lifespan) are issued, vs refresh tokens which can refresh them
            # will open up the page to log in and authorize scope
            flow.run_local_server(port=8080, prompt="consent", authorization_prompt_message="")
            credentials = flow.credentials

        # Save the credentials for next run
        with open('token.pickle', 'wb') as file:
            print('Saving Credentials for Future Use...')
            pickle.dump(credentials, file)

    # YT_API_KEY: (..., developerKey=YT_API_KEY)
    with build("youtube", "v3", credentials=credentials) as yt:
        if YT_URL == "https://youtube.com": yt_playlist_to_clone = input("Input a name for your Youtube Playlist!: ")
        else:
            # res = req.execute()
            yt_playlist_to_clone = f'New {[yt_playlist["snippet"]["title"] for yt_playlist in yt.playlists().list(part="snippet", mine=True).execute()["items"] if yt_playlist["id"] == YT_URL.split("list=")[1]][0]} {date}'

        # part contains a playlist resource: https://developers.google.com/youtube/v3/docs/playlists#resource
        yt_new_playlist_id = (yt.playlists().insert(
            part="snippet,status",
            body={
                "snippet": {
                    "title": yt_playlist_to_clone,
                    "description": "Spotify to Youtube",
                    "defaultLanguage": "en"
                },
                "status": {
                    "privacyStatus": "unlisted"
                }
            }
        ).execute())["id"]

        # # A: Scraping to clone playlist
        if __name__ == "__main__":
            uc_driver = uc.Chrome(use_subprocess=True)
            uc_driver.get(YT_URL)
            WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("xpath", '//*[@id="buttons"]/ytd-button-renderer'))).click() # Sign In Button
            WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("css selector", '#identifierId'))).send_keys(YT_USERNAME)
            uc_driver.find_element("css selector", "#identifierNext").click()
            time.sleep(1)
            WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("xpath", '//*[@id="password"]/div[1]/div/div[1]/input'))).send_keys(YT_PASSWORD)
            uc_driver.find_element("css selector", "#passwordNext").click()
            if YT_URL != "https://youtube.com":
                WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("css selector", 'button .ytd-menu-renderer'))).click() # ... menu
                WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("xpath", '//*[@id="items"]/ytd-menu-service-item-renderer[2]/tp-yt-paper-item/yt-formatted-string'))).click() # Add all to...
                add_to_yt_playlist(uc_driver, yt_playlist_to_clone)

        # # B: YT API to clone playlist
        # results = yt.playlistItems().list(part="snippet", playlistId=yt_new_playlist_id, maxResults=50).execute()
        # yt_tracks = results["items"]
        # while results.get('nextPageToken'):
        #     results = yt.playlistItems().list(part="snippet", playlistId=yt_new_playlist_id, maxResults=50, pageToken=results["nextPageToken"]).execute()
        #     yt_tracks.extend(results['items'])
        # yt_tracks_resources = [yt_track["snippet"]["resourceId"] for yt_track in yt_tracks]
        # for yt_tracks_resource in yt_tracks_resources:
        #     yt.playlistItems().insert(
        #         part="snippet",
        #         body={
        #             "snippet": {
        #                 "playlistId": yt_new_playlist_id,
        #                 "resourceId": yt_tracks_resource
        #             }
        #         }
        #     ).execute()

        # 3. Add Spotify songs to yt_new_playlist, don't remove already added (duplicate searches)
            for sp_track in sp_tracks:
                search_bar = WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("css selector", "#search-form #search")))
                search_bar.send_keys(sp_track)
                search_bar.send_keys(webdriver.Keys.ENTER)
                time.sleep(2)
                search_bar.send_keys(webdriver.Keys.CONTROL + "a")
                search_bar.send_keys(webdriver.Keys.DELETE)
                WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("css selector", '#title-wrapper #button #button'))).click() # : menu
                WebDriverWait(uc_driver, 3).until(EC.presence_of_element_located(("xpath", '//*[@id="items"]/ytd-menu-service-item-renderer[3]/tp-yt-paper-item/yt-icon'))).click() # Save to playlist
                time.sleep(2)
                add_to_yt_playlist(uc_driver, yt_playlist_to_clone)
                time.sleep(1)
                uc_driver.find_element("css selector", '#close-button').click() # X btn to close "Save to..." menu

        # # Alternative: YT API to iterate thru playlist so duplicates in sp_tracks are not added, then search & add to playlist
        # yt_search_resources = [yt.search().list(part="snippet", q=sp_track, type="video", maxResults=5).execute()["items"][0]["id"] for sp_track in sp_tracks]
        # for yt_search_resource in yt_search_resources:
        #     print(yt_search_resource)
        #     if yt_search_resource not in yt_tracks_resources:
        #         yt.playlistItems().insert(
        #                     part="snippet",
        #                     body={
        #                         "snippet": {
        #                             "playlistId": "yt_new_playlist_id",
        #                             "resourceId": yt_search_resource
        #                         }
        #                     }
        #                 ).execute()

        print(f"See your created playlist at https://www.youtube.com/playlist?list={yt_new_playlist_id}")


while True:
    conversion_way = input("Input 1 for YT->SP playlist, or 2 for SP->YT playlist: ")
    want_to_add_to_existing = input("Input y if you want to add to an existing playlist, or n if otherwise: ").lower()
    SP_URL = "https://open.spotify.com/"
    YT_URL = "https://youtube.com"
    if conversion_way == "1":
        YT_URL = input("Paste the link of the YT playlist to import here: ")
        if want_to_add_to_existing in ["y", "yes"]: SP_URL = input("Paste the link of your existing SP playlist here: ")
        yt_to_sp(YT_URL, SP_URL)
        break
    elif conversion_way == "2":
        SP_URL = input("Paste the link of the SP playlist to import here: ")
        if want_to_add_to_existing in ["y", "yes"]: YT_URL = input("Paste the link of your existing YT playlist here: ")
        sp_to_yt(YT_URL, SP_URL)
        break
    else: print("Invalid inputs!")
