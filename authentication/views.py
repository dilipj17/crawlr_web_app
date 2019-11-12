from django.http import HttpResponse,Http404
from django.shortcuts import redirect,render
import requests as re
from crawlr_web import settings
import json

def logIn(request):
    if 'jwt_token' in request.session:
        return HttpResponse('home page')
    else:
        return HttpResponse('<a href="https://crawlr-api.herokuapp.com/auth/linkedin">login</a>')

def logOut(request):
    try:
        del request.session['jwt_token']
        del request.session['UserID']
    except KeyError:
        pass
    return HttpResponse("<h1>dataflair<br>Session Data cleared</h1>")

def linkedInTokenHandle(request):
    code = request.GET.get('code')
    state = request.GET.get('state')
    accessToken = '?code='+code+'&state='+state
    responce = re.post(settings.API_URL+'/auth/linkedin/callback/'+accessToken)
    if responce.status_code == re.codes.ok:
        jwt_token = responce.json()
        if 'JWT' in jwt_token.keys():
            token = jwt_token['JWT']
            UserID = jwt_token['UserID']
            request.session['jwt_token'] = token
            request.session['user_id'] = UserID
            headers = {'content-type': 'application/json','authorization':token}
            url = settings.API_URL+'/auth/test'
            responce = re.post(url,headers = headers)
            return HttpResponse(responce.status_code)
        else:
            return render(request,'profile_comfirmation.html',{'jwt_token':jwt_token})
    return redirect('/auth/login')


def profileComfirm(request):
    if request.method == 'POST':
        provider = request.POST.get('provider')
        id = request.POST.get('id')
        fullName = request.POST.get('fullName')
        image = request.POST.get('image')
        data = {'provider':provider,'id':id,'fullName':fullName,'image':image}
        headers = {'content-type': 'application/json'}
        responce = re.post(settings.API_URL+'/auth/confirm',data=json.dumps(data),headers = headers)
        print(responce.content)
        if responce.status_code == re.codes.ok:
            jwt_token = responce.json()
            if 'JWT' in jwt_token.keys():
                token = jwt_token['JWT']
                UserID = jwt_token['UserID']
                request.session['jwt_token'] = token
                request.session['user_id'] = UserID
                headers = {'content-type': 'application/json','authorization':token}
                url = settings.API_URL+'/auth/test'
                responce = re.post(url,headers = headers)
                return HttpResponse(responce.status_code)
            else:
                return Http404('something went wrong')
        if responce.status_code == 401:
            return render(request,'profile_comfirmation.html',{'jwt_token':data,'error':'Please give Valid Data'})
        return redirect('/auth/login')
    return Http404('something went wrong')
