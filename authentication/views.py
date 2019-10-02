from django.http import HttpResponse
from django.shortcuts import redirect
import requests as re
from crawlr_web import settings

def logIn(request):
     return HttpResponse('<a href="https://crawlr-api.herokuapp.com/auth/linkedin">login</a>')

def linkedInTokenHandle(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    accessToken = '?code='+code+'&state='+state
    responce = re.post(settings.API_URL+'/auth/linkedin/callback/'+accessToken)
    if responce.status_code == re.codes.ok:
        jwt_token = responce.json()
        if 'JWT' in jwt_token.keys():
            token = jwt_token['JWT']
            headers = {'content-type': 'application/json','authorization':token}
            url = settings.API_URL+'/auth/test'
            responce = re.post(url,headers = headers)
            return HttpResponse(responce.status_code)
        else:
            return HttpResponse(jwt_token)
    else:
        return redirect('/auth/login')
    return HttpResponse('kk')
