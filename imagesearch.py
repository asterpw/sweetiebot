#!/usr/bin/python
import json
import urllib
import random 
import uploadimage


def imageSearch(text):
	searchurl='https://ajax.googleapis.com/ajax/services/search/images?v=1.0&'
	query = urllib.urlencode({'q': text})
	url = searchurl + query
	search_response = urllib.urlopen(url)
	search_results = search_response.read()
	results = json.loads(search_results)
	if 'responseData' in results and 'results' in results['responseData']:
		hits = results['responseData']['results']
		if len(hits) > 0:
			random.shuffle(hits)
			for hit in hits:
				try:
					print "Found Url: %s" % hit['url']
					url = uploadimage.rehostImage(hit['url'])
					return url
				except:
					print "Got Url Error: %s" % hit['url']
					continue
			return ''
		else:
			return ''
	else:
		return ''
	
if __name__ == "__main__":
	print imageSearch("Kangaroo")