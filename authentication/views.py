from django.http import HttpResponse,Http404
from django.shortcuts import redirect,render
import requests as re
from crawlr_web import settings
import json
from crawlr_web.decorators import login_required

@login_required
def homepage(request):
    return render(request,'index.html')

def logIn(request):
    if 'jwt_token' in request.session:
        headers = {'content-type': 'application/json','authorization':request.session['jwt_token']}
        url = settings.API_URL+'/auth/test'
        responce = re.post(url,headers = headers)
        if responce.status_code == 200:
            return redirect('homepage')
        return render(request,'login.html')
    return render(request,'login.html')

def logOut(request):
    try:
        del request.session['jwt_token']
        del request.session['UserID']
    except KeyError:
        pass
    return redirect('auth:login')

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
            return redirect('homepage')
        else:
            return render(request,'profile_comfirmation.html',{'jwt_token':jwt_token})
    return redirect('auth:login')


def profileComfirm(request):
    if request.method == 'POST':
        provider = request.POST.get('provider')
        id = request.POST.get('id')
        fullName = request.POST.get('fullName')
        email = request.POST.get('email')
        image = request.POST.get('image')
        data = {'provider':provider,'id':id,'fullName':fullName,'image':image,'email':email}
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
                return redirect('homepage')
            else:
                raise Http404('something went wrong')
        if responce.status_code == 401:
            return render(request,'profile_comfirmation.html',{'jwt_token':data,'error':'Please give Valid Data'})
        return redirect('auth:login')
    raise Http404('something went wrong try to login again')
