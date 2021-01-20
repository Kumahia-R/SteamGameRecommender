import requests
import json
API_Key = 'XXXXXXXXXXXXXXXXX'
from steamUser import SteamUser
from steamUser import Game
steamid = '76561198415661881'
GetOwnedURL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'
userList = requests.get(GetOwnedURL, params={'key': API_Key, 'steamid': int(steamid), 'include_appinfo': True, 'include_played_free_games':True})
listPython = userList.json()
for i in listPython["response"]["games"]:
    print(i["name"])
me = SteamUser(steamid)
print("This is your friend list")

#def compare_libraries(user, friend):