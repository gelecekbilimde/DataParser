import time
from bs4 import BeautifulSoup
import requests
import json

with open("GbYoutubeFeedData.json", "r+", encoding="utf-8")as f:
    feedJsonData = json.loads(f.read())


def allParser(bs, div, Attributes, param):
    bsr = bs.find_all(f"{div}", {f"{Attributes}": f"{param}"})
    return bsr

# returns one data by search info (first element)


def parser(bs, div, Attributes, param):
    bsr = bs.find(f"{div}", {f"{Attributes}": f"{param}"})
    return bsr


def addDataToFile(data):
    with open("finaldata.txt", "a", encoding="utf-8") as file:
        # prevData = json.loads(file.read())
        # prevData.append(newData)
        # print(prevData)
        newData = json.dumps(data, ensure_ascii=False)
        file.write(newData)
        file.write(",")


def parseDataConvertToJson(res, i):
    bs = BeautifulSoup(res.content, 'html.parser')
    myDict = {}
    myDict["shortlinkUrl"] = None
    # shortUrl
    myDict["title"] = i["title"]
    myDict["contentType"] = i["contentType"]
    myDict["contentLink"] = i["contentLink"]
    try:
        myDict["shortlinkUrl"] = parser(
            bs, "link", "rel", "shortlinkUrl")["href"]
    except:
        print("shortlinkUrl error")
    # description
    try:
        myDict["publishDate"] = str(res.content).split('"publishDate":"')[
            1].split('",')[0]
    except:
        print("publishDate error")
    # familyfrinedly
    try:
        myDict["isFamilyFriendly"] = parser(
            bs, "meta", "itemprop", "isFamilyFriendly")["content"]
    except:
        print("isFamilyFriendly error")
    # image
    try:
        myDict["image_src"] = parser(
            bs, "link", "rel", "image_src")["href"]
    except:
        print("image_src error")
    # embedurl
    try:
        myDict["embedUrl"] = parser(bs, "link", "itemprop", "embedUrl")["href"]
    except:
        print("embedUrl error")
    # keywords
    try:
        allKeyWords = allParser(bs, "meta", "property", "og:video:tag")
        keyWordArr = []
        for i in allKeyWords:
            keyWordArr.append(i["content"])
        myDict["keywords"] = keyWordArr
    except:
        print("keywords error")
    try:
        myDict["description"] = str(res.content).split('"description":{"simpleText":"')[
            1].split("}")[0]
    except:
        print("description error")
    if(myDict["shortlinkUrl"] == None):
        print("quit")
        quit()
    addDataToFile(myDict)


processLen = len(feedJsonData)
jsonArr = []
for i in feedJsonData:

    res = requests.get(f"https://www.youtube.com{i['contentLink']}")
    parseDataConvertToJson(res, i)
    processLen -= 1
    print(f"{processLen} -> {i['title']}")
    time.sleep(0.5)


# parseDataConvertToJson()

# pureHmtlCode = requests.get("https://www.youtube.com/watch?v=Z-6MLq_DbcU")
