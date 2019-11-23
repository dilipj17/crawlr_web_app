from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import reverse
import requests as re
from crawlr_web import settings
import json
from crawlr_web.decorators import login_required

@login_required
def resultpage(request):
    query = request.POST['q']
    if len(query) == 0:
        return HttpResponseRedirect(reverse('homepage'))
    try:
        responce = re.post(settings.API_URL+'/search',data=json.dumps({'searchQuery':query}),headers={'authorization':request.session['jwt_token'],'content-type':'application/json'})
    except Exception as e:
        print(e)
        raise Http404('somerthing went wrong')
    if responce.status_code == 200:
        return render(request,'result.html',{'Question_id':responce.json()['id']})
    if responce.status_code == 401:
        return redirect('auth:login')
    raise Http404('something went wrong')
    # return render(request,'result.html',{'Question_id':'5dd780c85ddf35001749ff73'})


@login_required
def ResultApi(request):
    id = request.GET['id']
    try:
        responce = re.get(settings.API_URL+'/search',params={'searchID':id},headers={'content-type':'application/json','authorization':request.session['jwt_token']})
    except Exception as e:
        print(e)
        return HttpResponse(json.dumps({'code':400}))
    if responce.status_code == 200:
        res = responce.json()
        return HttpResponse(json.dumps(res))
    if responce.status_code == 401:
        return HttpResponse(json.dumps({'code':401}))
    return HttpResponse(json.dumps({'code':400}))
