from django.urls import path,re_path
from . import views

app_name = 'question'
urlpatterns = [
    path('api/post',views.QuestionPost,name="post_api"),
    path('api/postreply',views.ApiReplyPost,name="reply_post_api"),
    path('api/deletereply',views.ApiReplyDelete,name="reply_delete_api"),
    re_path('reply/(?P<question>\w+)/',views.ReplyPost,name="reply"),
    re_path('delete/(?P<question>\w+)/',views.DeleteQuestion,name="delete_ques"),
]
