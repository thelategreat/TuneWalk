#!/usr/bin/python
import urllib, MySQLdb, sys, traceback
#basic idea
#get playlists
stations = ['http://tunein.com/radio/KEXP-FM-903-s32537/', 'http://tunein.com/radio/SomaFM-Indie-Pop-Rocks-s2592/',\
	'http://tunein.com/radio/New-Normal-Music-s126192/','http://tunein.com/radio/WFMU-911-s28808/']
class tw_db():
	def __init__(self):
		self.conn = MySQLdb.connect (host = "beatloaf.net",
							user = "beatloaf_tw",
                           passwd = "twcradle69",
                           db = "beatloaf_BNM")
		self.cursor = self.conn.cursor ()
	def query(self,sql):
		self.cursor.execute (sql)
		return self.cursor.fetchall()
	

def get_artists(station):
	#print station
	artist_list=[]
	playlist=urllib.urlopen(station).read().split('"dateCol">')#.split("See stations that play ")
	#print playlist
	
	for line in playlist[1:]:
		#print line
		try:
			date = line.split('</td>')[0]
			try:
				artist = line.split('<td class="artistCol">')[1].split('<h3><a href=')[1].split('>')[1].split('</a')[0]
			except:
				try:
					artist = line.split('<td class="artistCol">')[1].split(">")[0]
				except:
					print "get artist error"
			#print artist
			artist = urllib.quote(artist).lower()
			id = get_id(artist,db)
			#print artist, ":", date
			artist_list.append({'id':id,'artist':artist, "date":date})
		except:
			print "artist error ",line
			traceback.print_exc()
			sys.exit()
	print len(artist_list)," in playlist"
	return artist_list

def log_artists(artists,db):
	depth=3
	added=0
	dupes=0
	for i,artist in enumerate(artists):
		for j in range(1,depth+1):
			try:
				sug=artists[i+j]
				try:
					key=str(artist['id'])+str(sug['id'])+str(artist['date'])
					sql = "Insert into twlog(idtwlog,idmain,idsug,score) values('"\
					+key+"','"+artist['id']+"','"+sug['id']+"','"+str((depth+1-abs(j)))+"')"
					#print sql
					res=db.query(sql)
					added=added+1
				except:
					#print "DB error ",artist, sug
					dupes=dupes+1
					#traceback.print_exc()
					#sys.exit()
			except:
				print "array error"
	print added," added, ",dupes," dupes"
		#add row to table with key artist, related artist, points, date, and station
		

def get_id(artist,db):
		#sys.setrecursionlimit(3)
		#print artist
		res = db.query("select idtwartist from twartist where artist like '"+artist+"'")
		#print res
		if len(res) == 0:
			#print "not found ",artist
			res = db.query("INSERT into twartist(artist) values('"+artist+"')")
			#print "added ",artist
			id = get_id(artist,db)
		else:
			#print "found ",artist
			id = str(res[0][0])
		return id
			
db = tw_db()
for station in stations:
	artists=get_artists(station)
	log_artists(artists,db)