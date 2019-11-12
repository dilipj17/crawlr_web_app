from django.shortcuts import render
from crawlr_web.decorators import login_required
from django.http import HttpResponse
import requests as re

@login_required
def QuestionList(request):
    return HttpResponse('sdkjlfnslj')
