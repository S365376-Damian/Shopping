from rest_framework.decorators import api_view
import json
import hashlib
from datetime import datetime
from dateutil import parser
from dateutil.parser import parse
from unidecode import unidecode
from api.models import User, LoginSession, Voucher
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging
from mongoengine.queryset.visitor import Q

####################################################################################################

@api_view(["POST"])
def GetVoucherList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)    
        _search_string = GetParam(request, 'search_string')  
        voucherTable = Voucher.objects(isDeleted=False) 

        if(_search_string != None and _search_string != ""):
            voucherTable = voucherTable(Q(nameSlug__icontains=_search_string))    
        respond = Paging(request, voucherTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdateVoucher(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = GetParam(request, 'pk')
        _name = RequireParamExist(request, 'name')
        _code = RequireParamExist(request, 'code')
        _type = RequireParamExist(request, 'type')
        _value = RequireParamExist(request, 'value')

        voucher = None
        if(IsPk(_pk)):
            try:
                voucher = Voucher.objects.get(pk=_pk, isDeleted=False)
            except Voucher.DoesNotExist:      
                return ErrorResponse("Không tìm thấy voucher")

        if(voucher == None):
            voucher = Voucher(timeCreate = utcnow())
        voucher.name = _name
        voucher.nameSlug = unidecode(_name)
        voucher.code = _code
        voucher.type = _type
        voucher.value = int(_value)
        voucher.timeUpdate = utcnow()
        voucher.save()
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
    
####################################################################################################

@api_view(["POST"])
def DeleteVoucher(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')
        material = Voucher.objects.get(pk=_pk, isDeleted=False)
        material.isDeleted = True 
        material.save()
        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))