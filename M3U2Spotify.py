import spotipy
from spotipy.oauth2 import SpotifyOAuth

username = input("Your Username: ")
scope = 'playlist-modify-private'

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# creats a list with the songs form a .m3u file
def m3u_to_list(file):

    # open m3u Playlist
    dokument = open(file, "r", encoding='utf8')
    lines_list = (dokument.readlines())

    # Create a list whith te important Infos of the .m3u file
    prozessed_lines_list = []
    for i in range(1, len(lines_list), 2):
        prozessed_lines_list.append(lines_list[i][15:-1])

    # Prozess the list to the right formate
    artist_list = []
    track_name_list = []

    for list_item in prozessed_lines_list:

        # create the list with all Artists
        def artist_list_create(list_item):
            character_number_artist = 0
            while True:
                item_character = list_item[character_number_artist]

                if item_character == "-":
                    # check if there are features in it and prozess it nice for the list
                    feature_check = check_features(
                        list_item[0:character_number_artist])
                    if feature_check == False:
                        return(list_item[0:character_number_artist])
                    else:
                        return(list_item[0:feature_check])

                character_number_artist = character_number_artist + 1

        # create the list with the songnames
        def track_list_create(list_item):
            character_number_track = 0
            while True:
                item_character = list_item[character_number_track]

                if item_character == "-":
                    return(list_item[character_number_track + 2:])

                character_number_track = character_number_track - 1

        # check if there are features
        def check_features(artist):

            for letter_nr in range(len(artist)):

                # check for features signt as "ft."
                if artist[letter_nr] == "f":
                    if artist[letter_nr+1] == "t":
                        if artist[letter_nr+2] == ".":
                            return(letter_nr)
                # check for features signt as "feat."
                if artist[letter_nr] == "f":
                    if artist[letter_nr+1] == "e":
                        if artist[letter_nr+2] == "a":
                            if artist[letter_nr+3] == "t":
                                if artist[letter_nr+4] == ".":
                                    return(letter_nr)
                # check for features signt as ","
                if artist[letter_nr] == ",":
                    return(letter_nr)

            return(False)

        # adds the artist and the songname to the list
        artist_return = artist_list_create(list_item)
        track_return = track_list_create(list_item)
        artist_list.append(artist_return)
        track_name_list.append(track_return)

    # finish the list
    l = [artist_list, track_name_list]
    return(l)


# adds songs to a playlist
def add_to_playlist(playlist_name=None,  music_list=[], playlist_id=None):

    # get the id of the target playlist
    if playlist_name != None:
        playlist_search_result = sp.search(playlist_name, limit=20, type='playlist')[
            'playlists']['items']
        playlist_search_result_item = 0
        # make sure that the playlist is the right one
        while playlist_search_result[playlist_search_result_item]['owner']['id'] != username:
            playlist_search_result_item = playlist_search_result_item+1
        playlist_id = playlist_search_result[playlist_search_result_item]['id']
    if playlist_id != None:
        playlist_id = playlist_id

    # crate the song id list
    music_list_ids = []
    for track_nr in range(len(music_list[1])):
        # create the search querry
        track_search_querry = music_list[0][track_nr] + \
            " " + music_list[1][track_nr]
        # search with the searchquerry
        track_search_result = sp.search(
            track_search_querry, limit=1, type='track')
        # append the song id to the id-list
        if track_search_result['tracks']['items'] != []:
            music_list_ids.append(
                track_search_result['tracks']['items'][0]['id'])
        else:
            print(track_search_querry +
                  " konnte leider nicht gefunden werden... Füge es manuell hinzu!")

    # adds the songs from the list to the playlist
    sp.playlist_add_items(playlist_id, music_list_ids)
    print('Finish...')


# creates a playlist and adds songs to it
def create_and_add_playlist(playlist_name, music_list):

    # create a playlist and get the id of it
    playlist_id = (sp.user_playlist_create(
        username, name=playlist_name, public=True))['id']

    # adds songs to the createt playlist
    add_to_playlist(playlist_id=playlist_id, music_list=music_list)

# makes the little program menu


def menu():

    print("\nWelcome to my little tool! \nYou have two options: ")

    while True:
        print("1. Create a new Spotify-Playlist and add songs form a .m3u Playlist to it \n2. Adds Songs to a Soptify-Playlist from a .m3u Playlist \n0. Exit")
        choice = input("\nThe number of your choice:")

        if choice == "1":
            name = input("The name of the Spotify-Playlist: ")
            path = input("The path of your .m3u Playlist: ")
            # try if the path is allright
            try:
                open(path, "r")
            except FileNotFoundError:
                print("Retry with a right path!\n")
            else:
                create_and_add_playlist(name, m3u_to_list(path))

        if choice == "2":
            name = input("The name of your Spotify-Playlist: ")
            path = input("The path of your .m3u Playlist: ")
            # try if the path is allright
            try:
                open(path, "r")
            except FileNotFoundError:
                print("Retry with a right path!\n")
            else:
                add_to_playlist(playlist_name=name,
                                music_list=m3u_to_list(path))

        if choice == "0":
            break


# strats the program
menu()
