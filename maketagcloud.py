#!/usr/bin/python
from pytagcloud import create_tag_image, make_tags, create_html_data
from pytagcloud.lang.counter import get_tag_counts
import pytagcloud
import uploadimage
import os
import textanalyzer


def getColors():
	colors = "B719B4|A476FB|7230F3|7777CC|D17FFA"
	hexColors = [(int(c[0:2], 16), int(c[2:4], 16), int(c[4:6], 16)) for c in colors.split("|")]	
	return hexColors

def sqrtscale(count, mincount, maxcount, minsize, maxsize):
    if maxcount == mincount:
        return int((maxsize - minsize) / 2.0 + minsize)
    return max(int(minsize + (maxsize - minsize) * 
               (((count * 1.0 - mincount / 2.0) / (maxcount - mincount)) ** 0.5)), 1)
               
def makeFunc(wordCounts):
    maxcount = 0
    mincount = 999999999
    totalCount = 0
    totalLength = 0
    for word,count in wordCounts:
        maxcount = max(maxcount, count)
        mincount = min(mincount, count)
        totalCount += count
        totalLength += count*len(word)

    def customscale(count, mincount, maxcount, minsize, maxsize, exp):
       if maxcount == mincount:
           return int((maxsize - minsize) / 2.0 + minsize)
       return max(int(minsize + (maxsize - minsize) * 
                  (((count * 1.0 - mincount / 2.0) / (maxcount - mincount)) ** exp)), 1)

    return lambda c, mnc, mxc, mns, mxs: customscale(c, mnc, mxc, 1, 50, 0.5)
    #def scale
    

def getImageCloudForText(text, filename='cloud.png'):
    wordCounts = text[:120]
    func = makeFunc(wordCounts)
    
    tags = make_tags(wordCounts, maxsize=50, minsize=1, colors=getColors(), scalef=func)
#    fd = cStringIO.StringIO()

    create_tag_image(tags, filename, size=(500,300), background=(0x1c, 0x1b, 0x1f), layout=pytagcloud.LAYOUT_MIX, fontname='PT Sans Regular', rectangular=False)
    if __name__!="__main__":
        cloudfile = open(filename, 'rb')
        data = cloudfile.read()
        cloudfile.close()
        os.remove(filename)
        #data = fd.getvalue()
    
        return uploadimage.uploadImage(data)
    
if __name__=="__main__":    
    text = '\n'.join(open('data/textSample.txt').readlines())
    getImageCloudForText(textanalyzer.calcStats(text)['favoritewords0'])