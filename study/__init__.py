# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# print '''line1
# ...line2
# ...line3'''
# print None
# a = 1
# print a
# a = '1234' 
# print a
# 
# classmates = ('Michael', 'Bob', 'Tracy')
# print classmates[1]
# 
# age = 3
# if age >= 18:
#     print 'your age is', age
#     print 'adult'
# else:
#     print 'your age is', age
#     print 'teenager'
# 
# def haha():
#     return 'haha'
# a = haha
# print a
# print a()
# 
# a = ['a','b','c','d','e']
# b = a[::3]
# print b
# 
# d = {'a': 1, 'b': 2, 'c': 3}
# for a in d:
#     print a , d[a]
#     
# print [x * x for x in range(1, 11)]
# 
# L = ['Hello', 'World', 'IBM', 'Apple']
# print [s.lower() for s in L]
# 
# class students(object):
#     def __init__(self, name, score):
#         self.name = name
#         self.score = score
#     def hey(self):
#         print 'hey %s' %self.name
# c = students('fly','100')
# print c.score
# c.hey()


from pymongo import MongoClient
client = MongoClient('localhost', 27017)
db = client.test_database
import datetime
post = {"author": "Mike","text":"My first blog post!","tags":["mongodb", "python", "pymongo"],"date":datetime.datetime.utcnow()}
print 'abc'
posts = db.datas
# post_id = posts.insert_one(post).inserted_id
# print post_id,'aa' 

print db.collection_names(include_system_collections=False)

# new_posts = [{"author": "Mike",
# 
# "text": "Anotherpost",
# 
# "tags":["bulk", "insert"],
# 
# "date":datetime.datetime(2009, 11, 12, 11, 14)},
# 
# {"author":"Eliot",
# 
# "title": "MongoDB isfun",
# 
# "text":"and pretty easy too!",
# 
# "date":datetime.datetime(2009, 11, 10, 10, 45)}]
# 
# result = posts.insert_many(new_posts)
# print result.inserted_ids
# p_id = posts.insert_one({"b":"bb"}).inserted_id
print 'aa'

from bson.objectid import ObjectId
p_id = ObjectId('59ff3c17567c708550aa61a9')
print posts.find_one({"_id":p_id})

for post in posts.find():
    print post
