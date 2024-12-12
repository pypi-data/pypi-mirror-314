########################
# WEB Module
# fetch resources from the internet
########################

from urllib.request import urlopen
from mio.storage import parseJson


def isWebsite(website):
    try:
        return (urlopen(website).status == 200)
    except:
        return False


def requestText(website):
    return urlopen(website).read().decode('utf8')

def requestJson(website):
    data = requestText(website)
    if data==None: return None
    return parseJson(data)
