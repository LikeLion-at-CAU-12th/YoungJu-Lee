from django.urls import path
from posts.views import *

urlpatterns = [
    path('', post_list, name = "post_list"),
    path('<int:id>', post_detail, name = "post_detail"),
    path('comment/<int:id>', show_all_comments, name = "show_all_comments"),
    path('within-one-week', posts_within_one_week, name = "posts_within_one_week")
]