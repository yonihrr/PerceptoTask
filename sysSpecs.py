import platform
import cpuinfo
import psutil
import json
import sys
from socket import *
from datetime import timedelta
import time
import argparse

PORT=8021

#parser = argparse.ArgumentParser()

def server():		
	
	while True:
		try:
			data=getValues()
		except:
			print ("Faild to aquire values")
		print ("Sending...")		
		sendValues(data)
		time.sleep(2) # delays for 2 seconds
		
	
def client():
	# Create a TCP/IP socket
	#sock = socket(AF_INET, SOCK_DGRAM)

	# Bind the socket to the port
	server_address = ('', PORT)
	print >>sys.stderr, 'starting up on %s port %s' % server_address
	sock.bind(server_address)


	while True:
		print >>sys.stderr, '\nwaiting to receive message'
		data, address = sock.recvfrom(4096)
		#strData=json.loads(data)
		print >>sys.stderr, 'received %s bytes from %s' % (len(data), address)
		print >>sys.stderr, data
		
		#if data:
			#sent = sock.sendto(data, address)
		   # print >>sys.stderr, 'sent %s bytes back to %s' % (sent, address)




# psutil installation:
#sudo apt-get install gcc python-dev python-pip
#pip install psutil

def getValues():
	
	info = cpuinfo.get_cpu_info()
	model=info['brand'] #print('Model: {0}'.format(info['brand']))   #cpuinfo - model
	clockSpeed=info['hz_actual'] #print('Clock Speed: {0}'.format(info['hz_actual'])) #cpu info - clock speed
	cpuLoad = psutil.cpu_percent(interval=1)  #psutil - cpu load in percent
	totalMem=psutil.virtual_memory().total #total memory
	virtualMem=psutil.virtual_memory().percent
	numCore=psutil.cpu_count(logical=False) #Number of cores without logical
	kernel=platform.platform()
	#uptime
	with open('/proc/uptime', 'r') as f:
		uptime_seconds = float(f.readline().split()[0])
		uptime_string = str(timedelta(seconds = uptime_seconds))

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
	return data


def sendValues(data):
	
	
	#server_address = ('localhost', 8021)
	server_address = ('<broadcast>', PORT)
	sock.setsockopt(SOL_SOCKET, SO_BROADCAST, 1) #Configure BroadCast
	message = json.dumps(data)
	try:

		# Send data
		print >>sys.stderr, 'sending "%s"' % message
		sock.sendto(message, ('255.255.255.255', PORT)) #Broadcast Transmission
		# Receive response
		#print >>sys.stderr, 'waiting to receive'
		#data, server = sock.recvfrom(4096)
		#print >>sys.stderr, 'received "%s"' % data

	except:
		print ('Sending Failure')
	return;


try:
	sock = socket(AF_INET, SOCK_DGRAM) #working with ipv4 and UDP Protocol
except:
	print("Open Socket Failure");

print(sys.argv[1])

try:
	if sys.argv[1]=="server":
		server()
	elif sys.argv[1]=="client":
		client()
	else:
		print("Argument Wrong")
except:
	sock.close()
	print("Socket Close, GoodBye")
	





#print(uptime_string)
#json_str = json.dumps(data) #encode string into json ??
#print(json_str)
#print('....After....')
#data = json.loads(json_str)	#decode json into string ??
#json, json.dumps(), json.loads()
#json.dumps(['table',{"name":"yoni,"surname":"harir","phone":"0542290705"}])
#Sending Over UDP
# Create a UDP socket



