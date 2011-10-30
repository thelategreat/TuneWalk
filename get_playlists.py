import urllib
#basic idea
#get playlists
def get_artists():
	artist_list=[]
	playlist=urllib.urlopen('http://tunein.com/radio/KEXP-FM-903-s32537/').read().split("See stations that play ")
	#print playlist
	
	for line in playlist:
		#print line
		artist = line.split('"')[0]
		#print artist
		artist_list.append(artist)
	print artist_list
#parse artist

#put in db if neccessary

#make table with 2x before, 2x after, date, station

get_artists()