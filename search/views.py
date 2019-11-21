from django.shortcuts import render,redirect
from django.http import HttpResponse,HttpResponseRedirect,Http404
from django.shortcuts import reverse
import requests as re
from crawlr_web import settings
import json

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