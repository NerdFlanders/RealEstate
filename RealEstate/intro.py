from collections import defaultdict
import numpy

c = numpy.zeros(8)

print(c)

mylist = [1,2]
mytupel= (1,2)
mylist[1] = 3
try:
    mytupel[1] = 3
except TypeError:
    print("cannot modify tupel")


grades = {"Joel" : 80, "Tim" : 95}
print(grades["Joel"])
try:
    kates = grades["Kate"]
except KeyError:
    print("no grade for kate")

print("Joel" in grades)
print(grades.get("Joel", 0))

tweet = {
    "user" : "joelgrus",
    "text": "data science is awesome",
    "retweetCount": 100,
    "hashtags":["#data", "#science", "#datascience", "#awesome", "#yolo"]
}
keys = tweet.keys()
print(tweet.keys())
print(tweet.values())
print(tweet.items())