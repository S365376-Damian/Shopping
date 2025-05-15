import json
from django.shortcuts import render, redirect
from django.http import HttpResponse, StreamingHttpResponse
from rest_framework.decorators import api_view
from api.models import LoginSession, Shop, User
import datetime, time
from django.conf import settings
from api.views.loginsession import FindLoginSession
import api.auth
from lib.TGMT.TGMTutil import GetSystemInfo

def changepassword(request):
    permissions = ["all"]
    return CheckToken(request, 'changepassword.html', permissions)

def histories(request):
    permissions = ["all"]
    return CheckToken(request, 'histories.html', permissions)

def activity(request):
    permissions = ["all"]
    return CheckToken(request, 'activity.html', permissions)

def wrong(request):
    permissions = ["all"]
    return CheckToken(request, '404.html', permissions)


@api_view(["POST", "GET"])
def login(request):
    permissions = ["Root", "Admin", "Staff", "Customer", "Admin_Shop"]
    return CheckToken(request, 'login.html', permissions)

def my_account(request):
    permissions = ["Root", "Admin", "Staff", "Customer", "Admin_Shop"]
    return CheckToken(request, 'my_account.html', permissions)


def logout(request):
    try:        
        _token = request.COOKIES.get('token')
        jwt = api.auth.decode(_token)
        loginSessions = LoginSession.objects(phone=jwt['phone'], isDeleted = False)
        for loginSession in loginSessions:
            loginSession.logoutTime = datetime.datetime.utcnow()
            loginSession.isDeleted = True
            loginSession.save()     
    except Exception as e:
        print(str(e))

    res = redirect('/login')
    res.delete_cookie('token')
    res.delete_cookie('phone')
    return res

def index(request):
    args = GetSystemInfo()
    
    permissions = ["Root", "Admin", "Staff"]
    return CheckToken(request, 'users.html', permissions, args)

def home(request):
    args = GetSystemInfo()
    permissions = ["Root", "Admin", "Staff", "Customer", "Admin_Shop"]
    return CheckToken(request, 'home.html', permissions, args)


def users(request):
    args = GetSystemInfo()
    permissions = ["Root", "Admin", "Staff"]
    return CheckToken(request, 'users.html', permissions)

def product(request): 
    permissions = ["Root", "Admin", "Admin_Shop"]
    return CheckToken(request, 'product.html', permissions)

def predict(request):
    permissions = ["Root", "Admin", "Staff"]
    return CheckToken(request, 'predict.html', permissions)

def profile(request):
    permissions = ["Root", "Admin", "Staff", "Customer"]
    return CheckToken(request, 'profile.html', permissions)

def types(request):
    permissions = ["Root", "Admin", "Staff"]
    return CheckToken(request, 'types.html', permissions)

def type(request):
    permissions = ["Root", "Admin", "Staff", "Customer"]
    return CheckToken(request, 'type.html', permissions)

def material(request):
    permissions = ["Root", "Admin", "Staff"]
    return CheckToken(request, 'material.html', permissions)

def blog(request):
    permissions = ["Root", "Admin", "Staff"]
    return CheckToken(request, 'blog.html', permissions)

def voucher(request):
    permissions = ["Root", "Admin", "Staff", "Admin_Shop"]
    return CheckToken(request, 'voucher.html', permissions)

def privacy(request):
    permissions = ["Root", "Admin", "Staff", "Customer"]
    return CheckToken(request, 'privacy.html', permissions)

def policy(request):
    permissions = ["Root", "Admin", "Staff", "Customer"]
    return CheckToken(request, 'policy.html', permissions)

def product_detail(request):
    permissions = ["Root", "Admin", "Staff", "Customer", "Admin_Shop"]
    return CheckToken(request, 'product_detail.html', permissions)

def blog_detail(request):
    permissions = ["Root", "Admin", "Staff", "Customer"]
    return CheckToken(request, 'blog_detail.html', permissions)

def order(request):
    permissions = ["Root", "Admin", "Staff", "Customer", "Admin_Shop"]
    return CheckToken(request, 'order.html', permissions)

def cart(request):
    permissions = ["Root", "Admin", "Staff", "Customer", "Admin_Shop"]
    return CheckToken(request, 'cart.html', permissions)

def order_review(request):
    permissions = ["Root", "Admin", "Staff", "Customer", "Admin_Shop"]
    return CheckToken(request, 'order_review.html', permissions)

def blogs(request):
    permissions = ["Root", "Admin", "Staff", "Customer"]
    return CheckToken(request, 'blogs.html', permissions)

def comment(request):
    permissions = ["Root", "Admin", "Staff", "Admin_Shop"]
    return CheckToken(request, 'comments.html', permissions)

def shops(request): 
    users = User.objects(isDeleted = False, level__nin=['Root', 'Admin'])
    args = {}
    args["users"] = users.to_json()
    permissions = ["Root", "Admin"]
    return CheckToken(request, 'shops.html', permissions, args)

def Redirect(request):
    args = {
        'authorized': False,
        'version' : settings.VERSION,
        }
    return render(request, 'redirect.html' , args)
    
def CheckToken(request, redirect_page, permissions, args = {}):    
    isValidToken = False
    user = None

    args['debug'] = settings.DEBUG
    args['authorized'] = False
    args['version'] = settings.VERSION,


    if("all" in permissions):
        isValidToken = True

    if(not isValidToken):
        loginSession = GetLoginSession(request)
        if loginSession != None:
            args['level'] = loginSession["level"]
            args['phone'] = loginSession["phone"]
            args['fullname'] = loginSession["fullname"]
            isValidToken = loginSession["level"] in permissions
            if(not isValidToken and loginSession["level"] == "Customer"):
                return render(request, 'home.html' , args)
            if(not isValidToken and loginSession["level"] == "Admin_Shop"):
                return render(request, 'product.html' , args)
    if(isValidToken or redirect_page== 'login.html'):
        args['authorized'] = True
        return render(request, redirect_page , args)
    else:        
        args['fullscreen'] = True
        response = render(request, redirect_page, args)
        response.delete_cookie('token')
        response.delete_cookie('phone')
        return response


def IsValidToken(request):
    try:
        _token = request.COOKIES.get('token')
        if(_token == None or _token == ""):
            _token = request.GET.get('token')
        if(_token == None or _token == ""):
            return False

        api.auth.decode(_token)
        return True
    except Exception as e:
        print(str(e))
        return False



def GetLoginSession(request):
    try:
        _token = request.COOKIES.get('token')
        if(_token == None or _token == ""):
            _token = request.GET.get('token')
        if(_token == None or _token == ""):
            return None

        loginSession = FindLoginSession(_token)
        return loginSession
    except Exception as e:
        print(str(e))

    return None
