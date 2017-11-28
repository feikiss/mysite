from django.http import HttpResponse
from django.template.context_processors import request
import json
from pymongo import MongoClient
from bson.objectid import ObjectId
from bson import json_util
import shortuuid
from django import forms

from django.views.decorators.csrf import csrf_exempt
from __builtin__ import str
from django.shortcuts import render, render_to_response
import time
from django.http.response import HttpResponseBadRequest
from mysite import settings



lessons_map = {}
# client_map = {} #store all the data from every client, for each client, one list is used to store. The key should be unique in global.  
# index_map = {} #store the index of each client array.

GROUP_LENGTH = 3
PAGE_DATA_KEY_PREFIX = "page_data_"
PAGE_DATA_UID_SET_PREFIX = "page_uid_"
client = MongoClient('localhost', 27017)

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

@csrf_exempt
def hello(request):
    print "get request from client."
    return HttpResponse("good")

@csrf_exempt
def insert(request):
    received_json_data = json.loads(request.body)
#     print received_json_data
#     print request.POST
    cid = received_json_data['cid']
    local_uuid = shortuuid.uuid();
    received_json_data['uuid'] = local_uuid
    insertData(received_json_data)
    db = client.test_database
    datas = db.datas
    result = datas.insert_one(received_json_data)  # Next-> we should store the message to MongoDB by MQ.
#     return HttpResponse(result.inserted_id)
    return HttpResponse(local_uuid)

# def sync_all_data(page_data):
#     for (client_id,client_data) in client_map.items():
#         index = index_map.get(client_id,0)
#         
#         while(index < len(client_data) and client_data[index] != None):
#             page_data.append(client_data[index])
#             index = index+1
#         index_map[client_id] = index;    
        
        

def insert_client_data(received_json_data, client_data):
    uid = received_json_data['uid']
    if(uid <= len(client_data) - 1):
        client_data[uid] = received_json_data
    else:
        client_data.append(None)
        insert_client_data(received_json_data, client_data)

def insertData(received_json_data):
#     lession id
    lid = str(received_json_data['lid'])
    if lid not in lessons_map:
        lessons_map[lid] = {}
    lession_data = lessons_map.get(lid)
    
    client_id = str(received_json_data['cid'])  # client id.
    
    # page id
    page_id = str(received_json_data['pid'])
    page_data_key = PAGE_DATA_KEY_PREFIX + page_id
    page_data_uid_key = PAGE_DATA_UID_SET_PREFIX + page_id
    if page_data_key not in lession_data:
        lession_data[page_data_key] = []
    if page_data_uid_key not in lession_data:
        lession_data[page_data_uid_key] = set([])
    
    page_data = lession_data[page_data_key]
    page_uid_set = lession_data[page_data_uid_key]
    
    uid = received_json_data['uid']
    if uid not in page_uid_set:
        page_uid_set.add(uid)
        page_data.append(received_json_data)
        
    
    # insert the data to the client array in client map.
#     if client_id not in client_map:
#         client_map[client_id] = []
#     client_data = client_map[client_id]
#     insert_client_data(received_json_data, client_data)
#     sync_all_data(page_data)
    
    


# Currently, no need to read from mongoDB, just read from memory, like Redis..        
def read2(request):
    lid = str(request.GET['lid'])
    if lid not in lessons_map:
        raise ValueError('lid:', lid, ' is not valid')
    
    lesson_data = lessons_map[lid]
    
    pid = PAGE_DATA_KEY_PREFIX + str(request.GET['pid'])
    if pid not in lesson_data:
        raise ValueError('pid:', pid, ' is not valid for lid:', lid)
    page_data = lesson_data[pid]
    group_num = get_group_num(len(page_data))
    
    g = int(request.GET['g'])  # get the group.
#     g = g < 0 ? 0 : g
    if (g * GROUP_LENGTH > (len(page_data) - 1)):
        return HttpResponse(None)
    if g < 0:
        g = 0
    
    result = {}
    result['last'] = group_num
    result['g'] = g
    next_index = (g + 1) * GROUP_LENGTH
    result['last'] = group_num
    if next_index > len(page_data):
        result['datas'] = page_data[g * GROUP_LENGTH:]
    else:
        result['datas'] = page_data[g * GROUP_LENGTH:next_index]
        
    
#     result = json.dumps(result, sort_keys=True, indent=4, default=json_util.default)
    result = json.dumps(result, sort_keys=True, indent=4, default=json_util.default)
    return HttpResponse(result)

def get_group_num(num):    
    if num == 0:
        return 0
    if num % GROUP_LENGTH == 0:
        return num / GROUP_LENGTH
    else:
        return num / GROUP_LENGTH + 1

@csrf_exempt
def login(request):
    if request.method == "POST":
        uf = UserFormLogin(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            password = uf.cleaned_data['password']   
            correct = False;
            if (username == 'a' and password == 'a'):
                correct = True       
            # pdb.set_trace()
            if (correct):
                return render_to_response('success.html', {'operation':"login"})
            else:
                return  HttpResponse("not existed.")
    else:
        uf = UserFormLogin()
    print 'login'
    return render_to_response("login.html", {'uf':uf})


def user_existed(username):
    db = client.test_database
    user = db.users
    return user.find_one({'username':username}) == None

@csrf_exempt
def register(request):
    curtime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime());
    print curtime
    if request.method == "POST":
        uf = UserForm(request.POST)
        if uf.is_valid():
            username = uf.cleaned_data['username']
            # pdb.set_trace()
            # try:
#             filterResult = User.objects.filter(username = username)
#             if len(filterResult)>0:
#                 return render_to_response('register.html',{"errors":"user existed"})
            if(user_existed(username)):
                return render_to_response('register.html',{"errors":"user existed"})
            else:
                password1 = uf.cleaned_data['password1']
                password2 = uf.cleaned_data['password2']
                errors = []
                if (password2 != password1):
                    errors.append("Not same with eachother!")
                    return HttpResponseBadRequest("password not same!")
#                     return render_to_response('register.html', {'errors':errors})
                password = password2
                mobile = uf.cleaned_data['mobile']
                userid = settings.SERVER_NUMBER+''
                client.test_database.users.insert()
                return HttpResponse("success")
#                 return render_to_response('success.html', {'username':username, 'operation':"register"})
    else:
        uf = UserForm()
    return render_to_response('blogin.html', {'uf':uf})    
