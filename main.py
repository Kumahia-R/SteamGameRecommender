import PySimpleGUI as sg
from SteamUser import SteamUser


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


sg.theme('DarkBlue')  # color of the window
layout1 = [[sg.Text('Enter Steam URL:'), sg.InputText()],  # where the user inputs their Steam URL
           [sg.Text('Enter Friend number: '), sg.InputText()],  # where the user inputs the number of their friend
           [sg.Button('Ok'), sg.Button('Cancel')],
           [sg.Output(size=(80, 10))]]  # where the program output goes

# Create the Window
window = sg.Window('Steam Game Recommender', layout1)
# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel':  # if user closes window or clicks cancel
        break
    user_id = get_steam_id(values[0])
    steam_user = SteamUser(user_id)  # creates a SteamUser object with the user's ID being the argument
    steam_user.print_friend_list()
    user_tag_list = steam_user.tags_user_plays()  # gets the tags of every game that the user has played
    friend_index = values[1]
    steam_friend = steam_user.get_friends_list()[
        int(friend_index) - 1]  # creates a new SteamUser object with the friend's ID being the argument
    different_games = find_new_games(steam_user,
                                     steam_friend)  # gets a list of every game that the friend has that the user doesn't have
    print(f'Here are some of {steam_friend.get_profile_name()}\'s games you may want to see:')
    for i in different_games:
        # the loop checks for a game's tags and then checks if every one of those tags appears in user_tag_list
        if i.get_game_tags() != {} and i.get_game_tags().issubset(user_tag_list):
            print(f'{i.name}')
            # some of the games' store page URLs send you to Steam's front page (I checked this myself)
            # which caused some errors throughout the code since no game tags are returned
            # the first condition is a check to make sure that errors don't occur
window.close()
del window
