#!/bin/python3
import requests
import json
import sys

api_key = input("Please provide your last.fm api key: ")
user = input("Please provide the username you want to get data for: ")

# last.fm scrobbling data api url
recent_tracks_url = f"https://ws.audioscrobbler.com/2.0/?method=user.getrecenttracks&user={user}&api_key={api_key}&extended=true&format=json"

# top albums by user
top_ablums_url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopalbums&user={user}&api_key={api_key}&format=json"

# top artists by user
top_artists_url = f"https://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={user}&api_key={api_key}&format=json"

# top tracks by user
top_tracks_url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettoptracks&user={user}&api_key={api_key}&format=json"



# file to write data to
#filename = "lastfm_recent_tracks.json"

# Select the total number of pages
#total_pages = data["recenttracks"]["@attr"]["totalPages"] 

# function to make a call to the api enpoint provided
def api_call(url, page):
	# add page to url
	url = f"{url}&page={page}"
	# get initail repsonse
	response = requests.get(url)
	# parse response data as json
	data = json.loads(response.text)
	return data

# Function to get individual track data from recent_tracks_url api respnse
def get_track_data(item) :
	artist = item['artist']['name']
	track = item['name']
	playcount = item['playcount']
	return artist, track, playcount

# function to pull out relevant data from  top_artistts_url api response
def get_artist_data(item):
	artist = item['name']
	playcount = item['playcount']
	return artist, playcount

# function to pull out relevant data from  top_albums_url api response
def get_album_data(item):
	artist = item['artist']['name']
	album = item['name']
	playcount = item['playcount']
	return artist, album, playcount


# Function to write each items data to file
def write_json_file(input, filename):
	with open(filename, 'a') as file:
		file.write(json.dumps(input))
		file.write(",\n")

# function to write a variable to a new line in a file.
def write_list_file(input, filename):
	with open(filename, 'a') as file:
		file.write(input)
		file.write("\n")

# Get total number of pages from an api response
#total_pages = api_call(url, 1)["recenttracks"]["@attr"]["totalPages"]

# For the following functions.
# period can be one of the following strings:
# overall | 7day | 1month | 3month | 6month | 12month
# Number can be any integer from 1 to 200

# get top track data
def get_tracks_chart(url, number, period):
	url = url + f"&limit={number}&period={period}"
	response = api_call(url, 1)
	print(f"Top {number} Tracks listened to in 2025:\n")
	print(f"{'Artist':<30}{'Track':<50}Playcount\n")
	for item in response['toptracks']['track']:
		params = get_track_data(item)
		print(f"{params[0]:<30}{params[1]:<50}{params[2]}")

# get top data for either aritsts, albums or tracks
def get_artist_chart(url, number, period):
	url = url + f"&limit={number}&period={period}"
	response = api_call(url, 1)
	print(f"Top {number} Artists listened to in 2025:\n")
	print(f"{'Artist':<30}Playcount\n")
	for item in response['topartists']['artist']:
		params = get_artist_data(item)
		print(f"{params[0]:<30}{params[1]}")

def get_album_chart(url, number, period):
	url = url + f"&limit={number}&period={period}"
	response = api_call(url, 1)
	print(f"Top {number} Albums listened to in 2025:\n")
	print(f"{'Artist':<30}{'Album':.50}Playcount\n")
	for item in response['topalbums']['album']:
		params = get_album_data(item)
		print(f"{params[0]:<30}{params[1]:<50}{params[2]}")


get_artist_chart(top_artists_url, 25, "12month")
get_album_chart(top_ablums_url, 25, "12month")
get_tracks_chart(top_tracks_url, 100, "12month")
