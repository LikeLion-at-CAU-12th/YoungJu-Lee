from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가

# Create your views here.

def hello_world(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'data' : "Hello lielion-12th!"
        })
    
def index(request):
    my_data = {
        "name" : "이영주",
        "age" : 24,
        "major" : "Chinese Language and Literature"
    }
    friend_data = {
        "name" : "김명규",
        "age" : 24,
        "major" : "Computer Engineering"
    }

    return render(request, 'index.html', {"my_data" : my_data, "friend_data" : friend_data})
    

def printFriendData(request):
    if request.method == "GET":
        return JsonResponse({
            'status' : 200,
            'success' : True,
            'message' : '메시지 전달 성공!',
            'data' : [
                {
                    "name" : "이영주",
                    "age" : 24,
                    "major" : "Chinese Language and Literature"
                },
                {
                    "name" : "김명규",
                    "age" : 24,
                    "major" : "Computer Engineering"
                }
            ]
        })
