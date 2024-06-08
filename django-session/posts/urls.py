from django.urls import path
from posts.views import *

urlpatterns = [
   
    # path('create', create_post, name = "게시글 작성"),
    # path('', post_list, name = "post_list"),
    # path('<int:id>', post_detail, name = "post_detail"),
    # path('comment/<int:id>', show_all_comments, name = "show_all_comments"),    # path('within-one-week', posts_within_one_week, name = "posts_within_one_week")

    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('comment/', CommentList.as_view()),
    path('comment/<int:id>', CommentDetail.as_view()),
    # path('', PostList.as_view()),
    # path('<int:id>/', PostDetail.as_view()),
    # path('', PostList_GenericAPIView.as_view()),
    # path('<int:pk>/', PostDetail_GenericAPIView.as_view()),
    # path('comment/', CommentList.as_view()),
    # path('comment/<int:id>/', CommentDetail.as_view()),

]