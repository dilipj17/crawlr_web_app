from django.urls import path
from . import views

app_name='authentication'
urlpatterns = [
    path('login/',views.logIn, name='login'),
    path('profile/',views.profileComfirm, name='profile_comfirm'),
]
