import requests
from steamUser import SteamUser
from steamUser import Game
#my_id = '76561198415661881'
#me = SteamUser(my_id)
#my_url = 'https://store.steampowered.com/wishlist/profiles/76561198415661881/#sort=order'
# function to get the user's steamid based on a url they input
def get_steam_id(url):
    id_start = url.find("profiles/") + 9
    id_end = id_start + 17
    steam_id = url[id_start:id_end]
    return steam_id

#this function will return a set of games from the friend's list that the user won't have
def compare_libraries(user, friend):
    user_library = user.get_user_library()
    friend_library = friend.get_user_library()
    unique_games = friend_library.difference(user_library)
    return unique_games

user_url = input("Enter any URL involving your steam profile")
user_id = get_steam_id(user_url)
steam_user = SteamUser(user_id)
steam_friend = SteamUser('76561198121248324')
different_games = compare_libraries(steam_user, steam_friend)
for i in different_games:
    i.get_game_tags()
print(f'Your Steam ID is {user_id}')
steam_user.print_friend_list()