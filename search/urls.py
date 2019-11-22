from django.urls import path
from . import views

app_name = 'search'
urlpatterns = [
    path('result/',views.resultpage,name='result'),
    path('api/result/',views.ResultApi,name='result_api')
]
