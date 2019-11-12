from django.shortcuts import render
from crawlr_web.decorators import login_required
from django.http import HttpResponse,Http404
import requests as re
from crawlr_web import settings

@login_required
def QuestionList(request):
    pageNo = request.GET.get('page')
    if pageNo == None:
        pageNo = 1
    else:
        pageNo = int(pageNo)
    if pageNo < 0 or pageNo == 0:
        pageNo = 1
    headers = {'content-type': 'application/json','authorization':request.session.get('jwt_token')}
    params = {'pageNo':pageNo}
    try:
        responce = re.get(settings.API_URL+'/question/all',params=params,headers=headers)
    except re.ConnectionError as e:
        raise Http404('Check internet connection')
    except re.Timeout as e:
        raise Http404('Connection Timeout')
    except re.RequestException as e:
        raise Http404('Something went wrong')
    except KeyboardInterrupt:
        raise Http404('Someone closed the program')
    if responce.status_code == 200:
        json_res = responce.json()
        data = json_res['data']
        if data:
            pageNo += 1
            next = True
        else:
            next = False
        return render(request, 'question.html', {'question': data,'pageNo':pageNo,'next':next})
    return Http404('some error occurred')
