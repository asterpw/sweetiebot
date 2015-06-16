#!/usr/bin/python
import urllib, urllib2, cookielib
import base64
import xml.dom.minidom
import pygame
import StringIO, os

def uploadImage(data):
	encoded = base64.b64encode(data)
	opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))
	params = {"image" : encoded, "key": "2745111ddbbf7e814e4237882e9dead8" }
	response=opener.open("http://api.imgur.com/2/upload.xml", urllib.urlencode(params))
	xmlstr = response.read()
	return xml.dom.minidom.parseString(xmlstr).getElementsByTagName('original')[0].firstChild.data

def rehostImage(url):
	data = urllib.urlopen(url).read()
	return uploadImage(data)
	
def isMostlyWhite(image):
	whitePixels = pygame.transform.threshold(image, image.copy(), (255,255,255), (0,0,0), (0x1e, 0x17, 0x13), 0)
	return whitePixels > image.get_width()*image.get_height()*.3

def fastFlipColors(image):
	inv = pygame.Surface(image.get_rect().size, pygame.SRCALPHA)
	inv.fill((255,255,255,255))
	inv.blit(image, (0,0), None, pygame.BLEND_RGB_SUB)
	image.fill((0x1e, 0x17, 0x13))
	inv.blit(image, (0,0), None, pygame.BLEND_RGB_MAX)
	return inv
	
def slowFlipColors(image):
	#pixelarray = pygame.PixelArray(image)
	pixels = pygame.surfarray.pixels3d(image)
	for r in pixels:
		for c in r:
			p = c[:]
			if p[0] == 255 and p[1] == 255 and p[2] == 255:
				c[0] = 0x1e
				c[1] = 0x17
				c[2] = 0x13
			else:
				color = pygame.Color(int(c[0]), int(c[1]), int(c[2]))
				hsva = color.hsva[:]
				color.hsva = ((hsva[0]+180)%360 , hsva[1], hsva[2], hsva[3])
				c[0] = 255 - color.r
				c[1] = 255 - color.g
				c[2] = 255 - color.b
					
def recolorImage(url):
	data = urllib.urlopen(url).read()
	dataBuffer = StringIO.StringIO(data)
	image = pygame.image.load(dataBuffer, url)
	if isMostlyWhite(image):
		image = fastFlipColors(image)
		pygame.image.save(image, 'upload.png')
		imgfile = open('upload.png', 'rb')
		data = imgfile.read()
		imgfile.close()
		os.remove('upload.png')
	return uploadImage(data)
	
def recolorPalette(url):
	data = urllib.urlopen(url).read()
	dataBuffer = StringIO.StringIO(data)
	image = pygame.image.load(dataBuffer, url)
	if isMostlyWhite(image):
		slowFlipColors(image)
		pygame.image.save(image, 'upload.png')
		imgfile = open('upload.png', 'rb')
		data = imgfile.read()
		imgfile.close()
		os.remove('upload.png')
	return uploadImage(data)
	
if __name__ == "__main__":
	print recolorPalette('http://i.imgur.com/ON8evPg.gif')