from django.urls import path,include,re_path
from authentication.views import linkedInTokenHandle
from . import settings
from django.conf.urls.static import static
from question.views import QuestionList

urlpatterns = [
    path('auth/',include('authentication.urls',namespace='auth')),
    path('ques/',include('question.urls',namespace='ques')),
    re_path('login/',linkedInTokenHandle),
    path('',QuestionList,name="homepage")
]
if settings.DEBUG:
    urlpatterns = urlpatterns +  static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns = urlpatterns +  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
