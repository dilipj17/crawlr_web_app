from django.shortcuts import render
from crawlr_web.decorators import login_required
from django.http import HttpResponse
import requests as re
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@login_required
def QuestionList(request):
    numbers_list = range(1, 1000)

    page = request.GET.get('page', 1)

    paginator = Paginator(numbers_list, 20)
    try:
        numbers = paginator.page(page)
    except PageNotAnInteger:
        numbers = paginator.page(1)
    except EmptyPage:
        numbers = paginator.page(paginator.num_pages)

    return render(request, 'question.html', {'numbers': numbers})
