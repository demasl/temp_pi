#__author__ = 'Michael Lynch'
# Interface to Server

import urllib2
import urllib

# url of server
BASE_URL = "http://localhost:3000/"

def readTemp(roomNo):

	#Read the desired temp of a room
	data = {}

	roomNo = 'room' + str(roomNo) #need to add number to end of this string
	    
	data['data'] = roomNo #e.g. 'room1'
	urlValues = urllib.urlencode(data)

	url = BASE_URL+"getTemp.json"

	full_url = url + '?' + urlValues


	#you can read back the temp with the line below
	data = urllib2.urlopen(full_url) #data will equal temp set on showRooms page

	return data.read()

def logTemps(roomNo, reading):
	url = BASE_URL+"logTemp.json"

	#the array below reads [room, temp reading]
	values = { 'data[]': [roomNo, reading] }
	data = urllib.urlencode(values, True)

	req = urllib2.Request(url,data)
	response = urllib2.urlopen(req)
	the_page = response.read() #reads server response e.g. status 200
