from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import User, LoginSession
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth

####################################################################################################

@api_view(["POST"])
def GetLoginSession(request):
    try:
        _user_id = request.POST.get('user_id') 
        _userID = request.POST.get('userID')
        _building_id = request.POST.get('building_id')
        _fromDateStr = request.POST.get("fromDate")
        _toDateStr = request.POST.get("toDate")

        if(_fromDateStr == None or _fromDateStr == "" or
            _toDateStr == None or _toDateStr == "" or
            _building_id == None or _building_id == "" or
            _userID == None or _userID == ""):
            return ErrorResponse("Thiếu tham số")

        _fromDate = parse(_fromDateStr)
        _toDate = parse(_toDateStr) +  datetime.timedelta(days=1)

        if(_fromDate == None or _toDate == None):
            return ErrorResponse("Thiếu ngày ")

        if(_building_id == "all"):
            histories = LoginSession.objects(loginTime__gte=_fromDate, loginTime__lt=_toDate)
        else:
            histories = LoginSession.objects(building_id = _building_id, loginTime__gte=_fromDate, loginTime__lt=_toDate)

        if(_userID != "all"):
            histories = histories(user_id=_userID)


        return JsonResponse(histories.to_json())
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

#demo how to verify token
@api_view(["POST"])
def verifyToken(request):
    try:
        _token = request.POST.get('token')
        loginSession = FindLoginSession(_token)
        return JsonResponse(loginSession.to_json())
    except Exception as e:        
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

@api_view(["POST"])
def Redirect(request):
    try:
        _token = GetParam(request, 'token')
        if _token == None or _token == "":
            return ErrorResponse("missing value")

        loginSession = LoginSession.objects.get(pk = _token, isDeleted=False)
        if(loginSession.purpose == "ConfirmEmail"):
            user = User.objects.get(email=loginSession["email"], isDeleted=False)
            user.status = "Verified"
            user.save()
            
            message = "Xác nhận email thành công, chúng tôi sẽ chuyển bạn đến trang chủ"


            result = {
                "redirectlink" : "/login",
                "Success" : message,
                "token" : GenerateJwtToken(user)
            }

            loginSession.isDeleted = True
            loginSession.save()
            
            return ObjResponse(result)
    except Exception as e:        
        return ErrorResponse(str(e))

####################################################################################################

def FindLoginSession(token):
    jwtDecoded = api.auth.decode(token)
    return jwtDecoded