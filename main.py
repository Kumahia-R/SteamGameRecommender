from SteamUser import SteamUser
# This program will prompt a user to enter a Steam URL that contains their ID and will recommend games to the user
# based on which friend they want to compare their library to

# function to get the user's steamid based on a url they input
def get_steam_id(url):
    id_start = url.find("profiles/") + 9
    id_end = id_start + 17
    steam_id = url[id_start:id_end]
    return steam_id


# this function will return a set of games from the friend's list that the user doesn't have
def find_new_games(user, friend):
    user_library = user.get_user_library()
    friend_library = friend.get_user_library()
    unique_games = friend_library.difference(user_library)
    return unique_games


user_url = input("Enter any URL involving your steam profile")
user_id = get_steam_id(user_url)
steam_user = SteamUser(user_id) # creates a SteamUser object with the user's ID being the argument
user_tag_list = steam_user.tags_user_plays() # gets the tags of every game that the user has played
steam_user.print_friend_list()
friend_index = input("Choose which friend you want to compare your library to (Enter the corresponding number):")
steam_friend = steam_user.get_friends_list()[int(friend_index) - 1] # creates a new SteamUser object with the friend's ID being the argument
different_games = find_new_games(steam_user, steam_friend) # gets a list of every game that the friend has that the user doesn't have
print(f'Here are some of {steam_friend.get_profile_name()}\'s games you may want to see:')
for i in different_games:
    # the loop checks for a game's tags and then checks if every one of those tags appears in user_tag_list
    if i.get_game_tags() != {} and i.get_game_tags().issubset(user_tag_list):
        # some of the games' store page URLs send you to Steam's front page (I checked this myself)
        # which caused some errors throughout the code since no game tags are returned
        # the first condition is a check to make sure that errors don't occur
        print(f'{i.name}')