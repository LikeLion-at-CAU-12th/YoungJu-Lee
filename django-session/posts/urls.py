from django.urls import path
from posts.views import *

urlpatterns = [
    path('', post_list, name = "post_list"),
    path('<int:id>', post_detail, name = "post_detail"),

]