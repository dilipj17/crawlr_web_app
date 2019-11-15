from django.urls import path
from . import views

app_name = 'question'
urlpatterns = [
    path('api/post',views.QuestionPost,name="post_api"),
]
