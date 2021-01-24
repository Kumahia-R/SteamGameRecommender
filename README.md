# SteamGameRecommender
A program to search through every game of a steam user's library and a friend's library. It recommends games to the user based on what common games the user and friend have.
The API key is not included due to the private nature of it. Assuming you have a Steam account, you can find your API key at https://steamcommunity.com/dev/apikey.
You should have an API key as long as you've spent at least $5 in your Steam account. You can replace the X's with your API key and the program should work afterwards.

Regarding the "friend number", the order of your friend list is consistent but I'm not sure how Steam arranges it. My guess is that it's arranged based on the magnitude
of each friend's Steam ID. If you don't know the number of a specific friend, you can run through the program once and document what number that friend is then run the program
again using that friend's number

The program runs very slowly at the moment and the window shows that it's not responding as the program goes through each line. This is normal and you just need to wait for the
output. I will incorporate error checking but for now the code should work as intended so long as you input a valid steam URL.
