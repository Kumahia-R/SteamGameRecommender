import requests
from SteamUser import SteamUser
from SteamUser import Game


# function to get the user's steamid based on a url they input
def get_steam_id(url):
    id_start = url.find("profiles/") + 9
    id_end = id_start + 17
    steam_id = url[id_start:id_end]
    return steam_id


# this function will return a set of games from the friend's list that the user won't have
def compare_libraries(user, friend):
    user_library = user.get_user_library()
    friend_library = friend.get_user_library()
    unique_games = friend_library.difference(user_library)
    return unique_games


user_url = input("Enter any URL involving your steam profile")
user_id = get_steam_id(user_url)
steam_user = SteamUser(user_id)
steam_user.print_friend_list()
friend_index = input("Choose which friend you want to compare your library to (Enter the corresponding number):")
steam_friend = steam_user.get_friends_list()[int(friend_index) - 1]
different_games = compare_libraries(steam_user, steam_friend)
index = 0
for i in different_games:
    i.get_game_tags()
    print(index)
    index += 1