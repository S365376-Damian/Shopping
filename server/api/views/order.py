from rest_framework.decorators import api_view
import json
import hashlib
from datetime import datetime
from dateutil import parser
from dateutil.parser import parse
from unidecode import unidecode
from api.models import Shop, User, LoginSession, Order, Product
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging
from mongoengine.queryset.visitor import Q

####################################################################################################

@api_view(["POST"])
def GetOrderList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)    
        jwt = api.auth.decode(_token)
        _search_string = GetParam(request, 'search_string') 
        orderTable = Order.objects.filter(status__in=["Waiting", "Delivering", "Completed"], isDeleted=False) 
        try:
            user = User.objects.get(phone=jwt["phone"], isDeleted=False) 
        except User.DoesNotExist:
            user = User.objects.get(email=jwt["email"], isDeleted=False)
        if(user.level == "Admin_Shop"):
            shop = Shop.objects.get(user_pk=str(user.pk), isDeleted=False) 
            orderTable = orderTable.filter(shop_pk = str(shop.pk))   
 
        respond = Paging(request, orderTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def GetMyNewOrderList(request):
    try:
        user_pk = RequireParamExist(request, "user_pk")   
        orderTable = Order.objects(user_pk = user_pk, status = 'New',isDeleted=False) 

        respond = Paging(request, orderTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def GetMyOrderList(request):
    try:
        user_pk = RequireParamExist(request, "user_pk")   
        orderTable = Order.objects(user_pk = user_pk, status__in=["Waiting", "Delivering", "Completed"],isDeleted=False) 

        respond = Paging(request, orderTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdatePayOrder(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)
        _list_pk = RequireParamExist(request, 'list_pk')
        _list_quantity = RequireParamExist(request, 'list_quantity')
        list_pk = json.loads(_list_pk)
        list_quantity = json.loads(_list_quantity)

        for order_pk in list_pk:
            indexPk = list_pk.index(order_pk)
            order = Order.objects.get(pk = str(order_pk), isDeleted = False)
            product = Product.objects.get(pk = order.product_pk, isDeleted = False)
            order.quantity = int(list_quantity[indexPk])
            order.price = int(list_quantity[indexPk]) * product.price
            order.save()

        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def ConfirmOrder(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)
        _user_pk = RequireParamExist(request, "user_pk")
        _name = RequireParamExist(request, "name")
        _phone = RequireParamExist(request, "phone")
        _address = RequireParamExist(request, "address")
        _note = GetParam(request, "note")
        try:
            user = User.objects.get(phone=jwt["phone"], isDeleted=False) 
        except User.DoesNotExist:
            user = User.objects.get(email=jwt["email"], isDeleted=False)
        orders = Order.objects(user_pk = _user_pk, status = 'New',isDeleted=False) 
        for order in orders:
            order.status = "Waiting"
            order.user_name = _name
            order.user_phone = _phone
            order.address = _address
            order.note = _note
            if(user.level == "Admin_Shop"):
                shop = Shop.objects.get(user_pk=str(user.pk), isDeleted=False) 
                order.shop_pk = str(shop.pk)
                order.shop_name = shop.name
            order.save()
            
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def BuyOrder(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)
        _pk = RequireParamExist(request, 'pk')

        order = Order.objects.get(pk = _pk,isDeleted=False) 
        order.status = "Delivering"
        order.save()
            
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse(str(e)) 

####################################################################################################

@api_view(["POST"])
def    CompletedOrder(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)
        _pk = RequireParamExist(request, 'pk')

        order = Order.objects.get(pk = _pk,isDeleted=False) 
        order.status = "Completed"
        order.save()
            
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def CreateOrder(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _user_pk = RequireParamExist(request, 'user_pk')
        _user_name = RequireParamExist(request, 'user_name')
        _user_phone = RequireParamExist(request, 'user_phone')
        _product_pk = RequireParamExist(request, 'product_pk')
        _product_name = RequireParamExist(request, 'product_name')
        _price = RequireParamExist(request, 'price')
        _size = RequireParamExist(request, 'size')
        _color = RequireParamExist(request, 'color')
        _quantity = RequireParamExist(request, 'quantity')

        order = Order(timeCreate = utcnow())
        order.status = 'New'
        order.product_pk = _product_pk
        order.product_name = _product_name
        order.price = _price
        order.user_pk = _user_pk
        order.user_name = _user_name
        order.user_phone = _user_phone
        order.size = _size
        order.color = _color
        order.quantity = _quantity
        order.timeUpdate = utcnow()
        order.save()
        return SuccessResponse("Thêm vào giỏ hàng thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
    
####################################################################################################

@api_view(["POST"])
def DeleteOrder(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')
        order = Order.objects.get(pk=_pk, isDeleted=False)
        order.isDeleted = True 
        order.save()
        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))