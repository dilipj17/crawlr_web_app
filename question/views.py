from django.shortcuts import render
from crawlr_web.decorators import login_required
from django.http import HttpResponse,Http404
import requests as re
from crawlr_web import settings
import json
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

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
        return render(request, 'question.html', {'question': data,'pageNo':pageNo,'next':next,'user':request.session.get('UserID')})
    raise Http404('some error occurred')
    # return render(request,'question.html',{'question':'spdofsdopf','pageNo':0,'next':False})

@login_required
@csrf_exempt
def QuestionPost(request):
    if request.is_ajax():
        question = request.POST['question']
        try:
            responce = re.post(settings.API_URL+'/question',data={'question':question},headers={'authorization':request.session['jwt_token']})
        except error as e:
            print(e)
            messages.error(request,'some error occurred',extra_tags= 'alert alert-danger')
            return HttpResponse(json.dumps({'status':500}))
        if responce.status_code == 200:
            messages.success(request,'your question successfully added!',extra_tags= 'alert alert-info')
            return HttpResponse(json.dumps({'status':200}))
        else:
            messages.error(request,'some error occurred',extra_tags= 'alert alert-danger')
            return HttpResponse(json.dumps({'status':500}))
    messages.error(request,'some error occurred',extra_tags= 'alert alert-danger')
    return HttpResponse(json.dumps({'status':500}))
