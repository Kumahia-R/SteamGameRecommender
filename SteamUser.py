import requests
from bs4 import BeautifulSoup

API_KEY = 'XXXXXXXXXXXXXXXXXXXXXXXXXXX'  # key to access any of the steam APIs
# Following URLs are the Steam API URLs
GetFriendsURL = 'https://api.steampowered.com/ISteamUser/GetFriendList/v1/'  # Returns user's friend list and their information, we're specifically looking for their steamids
GotOwnedURL = 'https://api.steampowered.com/IPlayerService/GetOwnedGames/v1/'  # Returns user's owned games
GetPlayerSummariesURL = 'https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/'  # Returns a myriad of the user's information but we're only using this to get the user's profile name


class SteamUser:
    # class based on the Steam User
    # contains any information I may need for this project, such as their profile name and friend list
    def __init__(self, userID):
        # constructor accesses user data such as list of games played and friends
        self.userID = userID
        # using the Steam APIs to get the user's information
        self.user_summary = requests.get(GetPlayerSummariesURL, params={'key': API_KEY, 'steamids': userID}).json()
        self.friendList = requests.get(GetFriendsURL, params={'key': API_KEY, 'steamid': int(userID)}).json()
        self.user_list = requests.get(GotOwnedURL,
                                      params={'key': API_KEY, 'steamid': int(userID), 'include_appinfo': True,
                                              'include_played_free_games': True}).json()

    def get_user_library(self):
        # returns the names of the user's games in a set
        game_list = set()
        for i in self.user_list["response"]["games"]:
            new_game = Game(i['appid'], i['name'], i['playtime_forever'])
            game_list.add(new_game)
        return game_list

    def get_profile_name(self):
        # returns the profile name of the user (will make displaying it easier)
        profile_name = self.user_summary['response']['players'][0]['personaname']
        return profile_name

    def get_friends_list(self):
        # Returns the user's friend list
        friend_names = []
        for i in self.friendList["friendslist"]["friends"]:
            # this loop will make a new SteamUser object with each friend's steamid being the argument
            # then will add the new SteamUser to the list
            new_friend = SteamUser(i['steamid'])
            friend_names.append(new_friend)
        return friend_names

    def print_friend_list(self):
        # prints the names of the user's friends
        print("This is your friend list:")
        friend_index = 0  # index to access one friend per loop iteration
        friends_print = self.get_friends_list()  # gets the list of friends as SteamUsers
        for i in friends_print:
            # since the friends are already listed as SteamUsers
            # we just need to get their names using get_profile_name()
            print(f'{friend_index + 1}. {i.get_profile_name()}')
            friend_index += 1


class Game:
    # Game class, will have all the necessary info for a game so it can be readily accessed
    def __init__(self, app_id, name, play_time):
        self.app_id = app_id  # Every Steam game has a unique ID
        self.name = name  # The title of the game, not unique
        self.play_time = play_time  # amount of time the user has played the game

    def get_store_page(self):
        # method to get the url of the game's store page
        store_page_url_base = "https://store.steampowered.com/app/" # URL base
        store_page_url = store_page_url_base + str(self.app_id) + "/" + self.name + "/"  # gets the rest of the page URL
        return store_page_url

    def get_game_tags(self):
        # method to get the tags(genres) associated with the steam game
        page_url = self.get_store_page()
        page_html_text = requests.get(page_url).text  # gets the Steam page's HTML as text
        soup = BeautifulSoup(page_html_text, 'html.parser')  # turns the HTML into an object that makes parsing through it easier
        tag_html = soup.find("div", attrs={"class": "glance_tags popular_tags"})  # gets the section of the HTML that contains the game's tags
        if tag_html == None:
            return
        game_tags = tag_html.find_all("a")  # further filters the HTML to make getting only the tags easier
        tag_list = []
        for i in game_tags:
            # adds the game's tags as an str to the list tag_list
            tag_list.append(i.text.replace('\n', ' ').strip())  # there's lots of whitespace around the actual tage name so this is to exclude it
        return tag_list

    def __eq__(self, other):  # compares the appids of 2 Game objects
        # appid is the only completely unique variable in the object so it'll be the one compared
        self_id = self.app_id
        other_id = other.app_id
        return self_id == other_id

    def __hash__(self):
        # had to overload the hashing method to only hash the appid int (causes an error otherwise)
        return hash(self.app_id)