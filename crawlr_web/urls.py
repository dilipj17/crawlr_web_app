from django.urls import path,include,re_path
from authentication.views import linkedInTokenHandle

urlpatterns = [
    path('auth/',include('authentication.urls',namespace='auth')),
    re_path('login/',linkedInTokenHandle)
]
