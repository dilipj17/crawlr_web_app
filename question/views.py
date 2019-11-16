from django.shortcuts import render, redirect
from crawlr_web.decorators import login_required
from django.http import HttpResponse, Http404
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
    headers = {'content-type': 'application/json','authorization': request.session.get('jwt_token')}
    params = {'pageNo': pageNo}
    try:
        responce = re.get(settings.API_URL + '/question/all',params=params, headers=headers)
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
        return render(request, 'question.html', {'question': data, 'pageNo': pageNo, 'next': next, 'user': request.session['user_id']})
    raise Http404('some error occurred')
    # return render(request,'question.html',{'question':'spdofsdopf','pageNo':0,'next':False})

@login_required
def DeleteQuestion(request,question):
    print(request.session['jwt_token'])
    headers = {'content-type': 'application/json','authorization': request.session.get('jwt_token')}
    params = {'QuestionID': question}
    try:
        responce = re.delete(settings.API_URL+'/question?QuestionID='+question,data=json.dumps(params),headers=headers)
    except Exception as e:
        print(e)
        raise Http404('someting went wrong ')
    if responce.status_code == 401:
        return redirect('auth:login')
    if responce.status_code == 200:
        messages.success(request, 'your question successfully deleted !', extra_tags='alert alert-info')
        return redirect('homepage')
    print(responce.status_code)
    raise Http404('something went wrong')

@login_required
def ReplyPost(request, question):
    pageNo = request.GET.get('page')
    question_text = request.GET.get('question')
    if pageNo == None:
        pageNo = 1
    else:
        pageNo = int(pageNo)
    if pageNo < 0 or pageNo == 0:
        pageNo = 1
    headers = {'content-type': 'application/json','authorization': request.session.get('jwt_token')}
    params = {'pageNo': pageNo, 'questionID': question}
    try:
        responce = re.get(settings.API_URL + '/reply',params=params, headers=headers)
    except Exception as r:
        print(r)
        raise Http404('something went wring')
    if responce.status_code == 200:
        json_res = responce.json()
        data = json_res['data']
        if data:
            pageNo += 1
            next = True
        else:
            next = False
        return render(request, 'reply.html', {'question': question_text,'question_id':question, 'reply': data, 'pageNo': pageNo, 'next': next, 'user': request.session['user_id']})

    if responce.status_code == 401:
        return redirect('auth:login')
    raise Http404('something went wrong')
    # return render(request, 'reply.html', {'question': '', 'reply': '', 'pageNo': '', 'next': False, 'user': request.session.get('UserID')})


@login_required
@csrf_exempt
def QuestionPost(request):
    if request.is_ajax():
        question = request.POST['question']
        try:
            responce = re.post(settings.API_URL + '/question', data={'question': question}, headers={'authorization': request.session['jwt_token']})
        except Exception as e:
            print(e)
            messages.error(request, 'some error occurred',extra_tags='alert alert-danger')
            return HttpResponse(json.dumps({'status': 500}))
        if responce.status_code == 200:
            messages.success(request, 'your question successfully added!', extra_tags='alert alert-info')
            return HttpResponse(json.dumps({'status': 200}))
        else:
            messages.error(request, 'some error occurred',extra_tags='alert alert-danger')
            return HttpResponse(json.dumps({'status': 500}))
    messages.error(request, 'some error occurred',extra_tags='alert alert-danger')
    return HttpResponse(json.dumps({'status': 500}))

@login_required
@csrf_exempt
def ApiReplyPost(request):
    if request.is_ajax():
        question = request.POST['questionid']
        reply = request.POST['reply']
        try:
            responce = re.post(settings.API_URL + '/reply', data={'QuestionID': question,'reply':reply}, headers={'authorization': request.session['jwt_token']})
        except Exception as e:
            print(e)
            messages.error(request, 'some error occurred',extra_tags='alert alert-danger')
            return HttpResponse(json.dumps({'status': 500}))
        if responce.status_code == 200:
            messages.success(request, 'your reply successfully added!', extra_tags='alert alert-info')
            return HttpResponse(json.dumps({'status': 200}))
        else:
            messages.error(request, 'some error occurred',extra_tags='alert alert-danger')
            return HttpResponse(json.dumps({'status': 500}))
    messages.error(request, 'some error occurred',extra_tags='alert alert-danger')
    return HttpResponse(json.dumps({'status': 500}))
