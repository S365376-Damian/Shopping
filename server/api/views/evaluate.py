from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import Evaluate
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging

####################################################################################################

@api_view(["POST"])
def GetEvaluateList(request):
    try:
        _product_pk = RequireParamExist(request, 'product_pk')
        evaluatesTable = Evaluate.objects(product_pk = _product_pk,isDeleted=False)   

        respond = Paging(request, evaluatesTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdateEvaluate(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)
        
        _product_pk = RequireParamExist(request, 'product_pk')
        _product_name = RequireParamExist(request, 'product_name')
        _user_pk = RequireParamExist(request, 'user_pk')
        _user_name = GetParam(request, 'user_name')
        _user_phone = GetParam(request, 'user_phone')
        _content = GetParam(request, 'content')
        _point = RequireParamExist(request, 'point')


        evaluate = None
        try:
            evaluate = Evaluate.objects.get(product_pk=str(_product_pk), user_pk = str(_user_pk), isDeleted=False)
        except Evaluate.DoesNotExist:      
            pass

        if(evaluate == None):
            evaluate = Evaluate(
                timeCreate = utcnow()
                )
        evaluate.product_pk = _product_pk
        evaluate.product_name = _product_name
        evaluate.user_pk = _user_pk
        evaluate.user_name = _user_name
        evaluate.user_phone = _user_phone
        evaluate.content = _content
        evaluate.point = _point
        evaluate.timeUpdate = utcnow()
        evaluate.save()
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
    
####################################################################################################

@api_view(["POST"])
def DeleteEvaluate(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')
        evaluate = Evaluate.objects.get(pk=_pk, isDeleted=False)
        evaluate.isDeleted = True 
        evaluate.save()
        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))