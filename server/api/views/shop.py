from rest_framework.decorators import api_view
import json
import hashlib
from datetime import datetime
from dateutil import parser
from dateutil.parser import parse
from unidecode import unidecode
from api.models import User, LoginSession, Shop
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging
from mongoengine.queryset.visitor import Q

####################################################################################################

@api_view(["POST"])
def GetShopList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)    
        _search_string = GetParam(request, 'search_string')  
        shopTable = Shop.objects(isDeleted=False) 

        if(_search_string != None and _search_string != ""):
            shopTable = shopTable(Q(phone__icontains=_search_string) |
                                        Q(name__icontains=_search_string))  
              
        respond = Paging(request, shopTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdateShop(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = GetParam(request, 'pk')
        _name = RequireParamExist(request, 'name')
        _phone = RequireParamExist(request, 'phone')
        _email = RequireParamExist(request, 'email')
        _user_pk = RequireParamExist(request, 'user_pk')
        _address = RequireParamExist(request, 'address')

        shop = None
        if(IsPk(_pk)):
            try:
                shop = Shop.objects.get(pk=_pk, isDeleted=False)
            except Shop.DoesNotExist:      
                return ErrorResponse("Không tìm thấy cửa hàng")

        if(shop == None):
            shop = Shop(timeRegister = utcnow())

        user = User.objects.get(pk = str(_user_pk), isDeleted = False)
        shop.name = _name
        shop.phone = _phone
        shop.email = _email
        shop.address = _address
        shop.user_pk = _user_pk
        shop.user_name = user.fullname
        shop.timeUpdate = utcnow()
        shop.save()
        if(user.level == 'Customer' or user.level == 'Staff'):
            user.level = 'Admin_Shop'
            user.save()
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
    
####################################################################################################

@api_view(["POST"])
def DeleteShop(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')
        shop = Shop.objects.get(pk=_pk, isDeleted=False)
        shop.isDeleted = True 
        shop.save()
        return SuccessResponse("Xóa cửa hàng thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
####################################################################################################

@api_view(["POST"])
def GetShop(request):
    try:
        _token = request.POST.get('token')
        jwt = api.auth.decode(_token)
        try:
            user = User.objects.get(phone=jwt["phone"], isDeleted=False) 
        except User.DoesNotExist:
            user = User.objects.get(email=jwt["email"], isDeleted=False) 

        try:
            shop = Shop.objects.get(user_pk = str(user.pk), isDeleted = False)
            return JsonResponse(shop.to_json())
        except Shop.DoesNotExist:
            return ErrorResponse("Bạn chưa đăng ký")

    except Exception as e:
        return ErrorResponse(str(e))