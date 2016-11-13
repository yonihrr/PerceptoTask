import platform
import cpuinfo
import psutil
import json
import sys
from socket import *
from datetime import timedelta
import time
import argparse
import netifaces
import os


PORT=8021


def server():# Server responsible for aquiring and broadcasting the information	
	while True:
		try:
			data=getValues()
		except:
			print ("Faild to aquire values")
		print ("Sending...")		
		sendValues(data)
		time.sleep(2) # delays for 2 seconds
		
	
def client(): # Client simulate a listenr on the selected port, also in broadcasting,printing the aquired json
	# Bind the socket to the port
	server_address = ('', PORT)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	sock.bind(server_address)
	counter=0

	while True:
		
		print >>sys.stderr, '\nwaiting to receive message...'
		data, address = sock.recvfrom(4096) #Listeninig 4096 bytes
		os.system('clear') #clear screen
		data=json.loads(data) #back to dictionary
		counter=counter+1; #counter numbers of recieving
		print ("Information Recieved #%d\n"%counter)	
		print >>sys.stderr, 'received %s bytes from %s\n' % (len(data), address)				
		print "{:<13} {:<20}".format('Key','Label') #printing as table
		print "{:<13} {:<20}".format('---','---')
		for key, label in data.iteritems():
			print "{:<13} {:<20}".format(key, label)
		


def getValues(): #A function that concentrade all the data gathering
	
	try:
		info = cpuinfo.get_cpu_info()
	except:
		print ("cant get cpu values - cpuinfo lib")
	
	model=info['brand'] #cpuinfo - model
	clockSpeed=info['hz_actual']#cpu info - clock speed
	cpuLoad = psutil.cpu_percent(interval=1)  #psutil - cpu load in percent
	totalMem=psutil.virtual_memory().total #total memory
	virtualMem=psutil.virtual_memory().percent #Memory loadm, Percentage
	numCore=psutil.cpu_count(logical=False) #Number of cores without logical
	kernel=platform.platform() # kernel version
	#uptime
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
		uptime_string = str(timedelta(seconds = uptime_seconds))
	# saving data as dictionary, for future transfer as json
	data = {
		'Model' : model,
		'Clock' : clockSpeed,
		'Cpu' : cpuLoad,
		'totalMem':totalMem,
		'virtualMem':virtualMem,
		'numCore':numCore,
		'uptime':uptime_string,
		'kernel':kernel
   
	}
	dic=getInterfaces()
	data.update(dic) #fusing the two dictionaries into one for sending
	return data

def getInterfaces(): #Return Dictionary with Iterfaces and thier MAC's
	data= netifaces.interfaces()
	dic={}
	for x in data:
		addrs = netifaces.ifaddresses(x)
		entry=addrs[netifaces.AF_LINK]
		dic[x] = entry
	return dic


def sendValues(data): #Launch Values over UDP broadcast
	
	
	#server_address = ('localhost', 8021)
	server_address = ('<broadcast>', PORT)
	sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #Configure BroadCast
	message = json.dumps(data)
	try:

		# Send data
		print >>sys.stderr, 'sending "%s"' % message
		sock.sendto(message, ('255.255.255.255', PORT)) #Broadcast Transmission


	except:
		print ('Sending Failure')
	return;


try:
	sock = socket(AF_INET, SOCK_DGRAM) #working with ipv4 and UDP Protocol
except:
	print("Open Socket Failure");

print(sys.argv[1])

try:
	if sys.argv[1]=="server": #value from shell, activate accourdingly
		server()
	elif sys.argv[1]=="client":
		client()
	else:
		print("Argument Wrong")
except:
	sock.close()
	print("Socket Close, GoodBye")

