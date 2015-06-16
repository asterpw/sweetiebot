import time
from sweetiebot import *
count = 0
while True:
	time.sleep(1)
	servers, message = getServerStatusMessage()
	count = count + 1
	print "Count: ", servers, count
	if servers > 6:
		print "##########!!!!!!!!!!!!!!###############\n"*20