from django.shortcuts import render
from django.http import JsonResponse # 추가 
from django.shortcuts import get_object_or_404 # 추가
from django.views.decorators.http import require_http_methods
from posts.models import *
import json
from datetime import datetime,timedelta

@require_http_methods(["POST", "GET"])
def post_list(request):

    if request.method == "POST":
        body = json.loads(request.body.decode('utf-8'))
        
        user_id = body.get('user_id')
        user = User.objects.get(pk=user_id)


        new_post = Post.objects.create(
            title = body['title'],
            content = body['content'],
            user_id = user,   
            category = body['category']
        )


        new_post_json = {
            "id": new_post.id,
            "title" : new_post.title,
            "content" : new_post.content,
            "user_id" : new_post.user_id.id,
            "user_username" : new_post.user_id.username,
            "category" : new_post.category 
        }

        return JsonResponse({
            'status' : 200,
            'message' : '게시글 생성 성공',
            'data' : new_post_json
        })
    
    if request.method == "GET":
        post_all = Post.objects.all()

        post_json_all = []

        for post in post_all:
            post_json = {
                "id" : post.id,
                "title" : post.title,
                "content" : post.content,
                "user_id" : post.user_id.id,
                "user_username" : post.user_id.username,
                "category" : post.category,
            }
            post_json_all.append(post_json)

        return JsonResponse({
            'status' : 200,
            'message' : '게시글 목록 조회 성공',
            'data' : post_json_all
        }) 


@require_http_methods(["GET", "PATCH", "DELETE"])
def post_detail(request, id):
    if request.method == "GET" :
        post = get_object_or_404(Post,pk=id)

        post_json = {
            "id" : post.id,
            "title" : post.title,
            "content" : post.content,
            "user_id" : post.user_id.id,
            "user_username" : post.user_id.username,
            "category" : post.category
        }

        return JsonResponse({
            'status' : 200,
            'message' : '개별 게시글 조회 성공',
            'data' : post_json
        })
    
    if request.method == "PATCH":
        body = json.loads(request.body.decode('utf-8'))
        update_post = get_object_or_404(Post, pk=id)

        update_post.title = body['title']
        update_post.content = body['content']
        update_post.category = body['category']

        update_post.save()

        update_post_json = {
            "id" : update_post.id,
            "title" : update_post.title,
            "content" : update_post.content,
            "user_id" : update_post.user_id.id,
            "user_username" : update_post.user_id.username,
            "category" : update_post.category
        }

        return JsonResponse({
            'status' : 200,
            'message' : '게시글 수정 성공',
            'data' : update_post_json
        }) 
    
    if request.method == "DELETE":
        delete_post = get_object_or_404(Post,pk=id)
        delete_post.delete()

        return JsonResponse({
            'status' : 200,
            'message' : '게시글 삭제 성공',
            'data' : None
        })
    
@require_http_methods(["GET"])
def show_all_comments(request, id):
    comment_all = Comment.objects.filter(post_id_id=id)

    comment_json_all = []

    for comment in comment_all:
        comment_json={
            "id" : comment.id,
            "comments" : comment.comments,
            "post_id" : comment.post_id.id,
            "user_id" : comment.user_id.id,
            "user_username" : comment.user_id.username,
            "is_secret" : comment.is_secret
        }

        comment_json_all.append(comment_json)

    return JsonResponse({
        'status' : 200,
        'message' : '게시물에 달린 모든 댓글 보기',
        'data' : comment_json_all
    })

@require_http_methods(["GET"])
def posts_within_one_week(request):
    request_date = datetime.now()
    target_date = request_date - timedelta(days=7)

    filtered_posts_all = Post.objects.filter(created_at__range=(target_date, request_date)).order_by('-created_at')
    
    filtered_posts_json_all = []

    for filtered_post in filtered_posts_all:
        filtered_post_json = {
            "created_at" : filtered_post.created_at,
            "id" : filtered_post.id,
            "title" : filtered_post.title,
            "content" : filtered_post.content,
            "user_id" : filtered_post.user_id.id,
            "user_username" : filtered_post.user_id.username,
            "category" : filtered_post.category
        }

        filtered_posts_json_all.append(filtered_post_json)
    

    return JsonResponse({
        'status' : 200,
        'message': '일주일 내의 모든 게시물(생성시각 순)',
        'data' : filtered_posts_json_all
    })
  
@require_http_methods(["POST"])
def create_post(request):

    user_id = request.POST.get('user_id')
    user = User.objects.get(pk=user_id)

    new_post = Post.objects.create(
        title = request.POST['title'],
        content = request.POST['content'],
        user_id = user,
        category = request.POST['category'],
        image = request.FILES['image']
    )

    new_post_json = {
        "id" : new_post.id,
        "title" : new_post.title,
        "content" : new_post.content,
        "user_id" : new_post.user_id.id,
        "user_username" : new_post.user_id.username,
        "category": new_post.category,
        "image" : new_post.image.name
    }

    return JsonResponse({
        'status' : 200,
        'message' : '게시글 생성 성공',
        'data' : new_post_json
    })
