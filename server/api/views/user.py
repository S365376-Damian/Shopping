from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import User, LoginSession, Pet
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging
from lib.TGMT.TGMTemail import SendEmailAsync
from mongoengine.queryset.visitor import Q

from lib.TGMT.TGMTutil import GenerateRandomString, GenerateRandomNumber


####################################################################################################

@api_view(["POST"])
def login(request):
    _typeLogin = GetParam(request, 'typeLogin')
    _email = GetParam(request, 'email')
    _phone = GetParam(request, 'phone').lower().strip()
    _nameLogin = GetParam(request, 'nameLogin')
    _password = request.POST.get('password')
    if _phone != None and _phone != '':
        _phone = _phone.lower().strip()

    if _typeLogin == "google" and _email != None:
        try:
            _user = User.objects.get(email=_email, isDeleted=False)
        except User.DoesNotExist:
            return ErrorResponse("Có lỗi khi đăng nhập với Google")
    else:
        try:
            hashed_password = HashPassword(_password)
            _user = User.objects.get(phone=_phone, isDeleted=False)
            if(_user.password != hashed_password):
                return ErrorResponse("Không đúng tài khoản/password")
        except User.DoesNotExist:
            try:
                _user = User.objects.get(nameLogin=_nameLogin, isDeleted=False)
            except User.DoesNotExist:
                return ErrorResponse("Không đúng tài khoản/password")

    try:
        login_session = LoginSession(phone = _user.phone,
                                    fullname = _user.fullname,
                                    level = _user.level,                                    
                                    loginTime = utcnow()
                                    )
        payload = {
            'phone': _user.phone,
            'email': _email,
            'fullname' : _user.fullname,
            'level' : _user.level,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=365),
            'loginSession_pk' : str(login_session.pk)
        }

        jwt_token = api.auth.encode(payload)

        login_session.token = "" #jwt_token['token']

        login_session.save()

        _user.password = ""
        result = json.loads(_user.to_json())
        result["token"] = jwt_token['token']

        return ObjResponse(result)
    except Exception as e:
        return ErrorResponse('Có lỗi: ' + str(e))

####################################################################################################

@api_view(["POST"])
def logout(request):
    try:
        _token = request.POST.get('token')
        jwt = api.auth.decode(_token)
        loginSessions = LoginSession.objects(phone = jwt["phone"], isDeleted = False)

        for loginSession in loginSessions:
            loginSession.logoutTime = datetime.datetime.utcnow()
            loginSession.isDeleted = True
            loginSession.save()

        return SuccessResponse('Logout thành công')

    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

def HashPassword(password):
    hash_routine = 5
    hashed_password = password
    while hash_routine != 0 :
       hashed_password = hashlib.sha224(hashed_password.encode('utf-8')).hexdigest()
       hash_routine = hash_routine - 1
    return hashed_password

####################################################################################################

@api_view(["POST"])
def GetUser(request):
    try:
        _token = request.POST.get('token')
        jwt = api.auth.decode(_token)
        try:
            user = User.objects.get(phone=jwt["phone"], isDeleted=False) 
        except User.DoesNotExist:
            user = User.objects.get(email=jwt["email"], isDeleted=False) 
        pets = Pet.objects(owner = user.phone, isDeleted = False)
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)

        if user.level == "Customer":
            user.viewAble = False
            for pet in pets:
                if pet.dateStart + datetime.timedelta(hours=7) <= now <= pet.dateEnd + datetime.timedelta(hours=7):
                    user.viewAble = True
                    break
                else:
                    user.viewAble = False
            user.save()
        else: 
            user.viewAble = True
            user.save()

        return JsonResponse(user.to_json())
    except Exception as e:
        return ErrorResponse(str(e))

####################################################################################################

@api_view(["POST"])
def GetUserList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)       

        _level = GetParam(request, 'level')
        _search_string = GetParam(request, 'search_string')
        
        userTable = User.objects(level__ne="Root", isDeleted=False).exclude("password")  

        if _level == 'Admin':
            userTable = userTable(level__ne="Admin")
        elif _level == "Staff":
            userTable = userTable(level = "Customer")

        if(_search_string != None and _search_string != ""):
            userTable = userTable.filter(Q(phone__icontains=_search_string) |
                                        Q(fullname__icontains=_search_string))

        respond = Paging(request, userTable)

        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))

####################################################################################################

@api_view(["POST"])
def MissPassword(request):
    try:
        _email = GetParam(request, "email")
        try:
            user = User.objects.get(email=_email, isDeleted=False)
        except User.DoesNotExist:
            return ErrorResponse("Không tìm thấy tài khoản với email này")

        codeOTP = str(GenerateRandomNumber(100000, 999999))
        user.codeOTP = codeOTP
        user.save()
        print(codeOTP)

        SendEmailAsync("Mã xác thực tài khoản",
                    "<!DOCTYPE html>" +
                    "<html><head></head><body>" +
                    "<p>Mã OTP của bạn là: " + codeOTP + "</p>" +		
                    "<p>Đây là email tự động, vui lòng không reply.</p>" +
                    "</body></html>",
                    [_email]
        )
        
        return SuccessResponse("Gửi thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
####################################################################################################

@api_view(["POST"])
def CheckOTPPassword(request):
    try:
        _otp = GetParam(request, "otp")
        try:
            user = User.objects.get(codeOTP=_otp, isDeleted=False)
        except User.DoesNotExist:
            return ErrorResponse("Mã xác thực sai")

        password = str(GenerateRandomNumber(100000, 999999))
        user.password = HashPassword(password)
        user.save()

        SendEmailAsync("Mật khẩu mới",
                    "<!DOCTYPE html>" +
                    "<html><head></head><body>" +
                    "<p>Mật khẩu mới của bạn là: " + password + "</p>" +		
                    "<p>Đây là email tự động, vui lòng không reply.</p>" +
                    "</body></html>",
                    user.email
        )
        print(password)
        return SuccessResponse("Gửi thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

@api_view(["POST"])
def ChangePassword(request):
    try:
        _token = request.POST.get("token") 
        loginSession = api.auth.decode(_token)
    
        _phone = loginSession["phone"]
        _password = request.POST.get('password')
        hashed_password = HashPassword(_password)
        _newPassword = request.POST.get('newPassword')

        user = User.objects.get(phone=_phone, isDeleted=False)

        if(user.password != hashed_password):
            return ErrorResponse("Password cũ không đúng")
        
        hashed_newpassword = HashPassword(_newPassword)
        user.password = hashed_newpassword
        user.save()
        
        return SuccessResponse("Đổi mật khẩu thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################

@api_view(["POST"])
def ResetPassword(request):
    try:
        _username = request.POST.get('username')
        _password = _username
        try:
            user = User.objects.get(username=_username, isDeleted=False)
        except User.DoesNotExist:
            return Response(
                {'Error': "Không tìm thấy user: "+ _username},
                status=ERROR_CODE,
                content_type="application/json"
            )
        if user:
            hashed_newpassword = HashPassword(_password)
            user.password = hashed_newpassword
            user.isPasswordChanged = False
            user.save()
            return Response(
                {'Success': "Đổi mật khẩu thành công"},
                status=SUCCESS_CODE,
                content_type="application/json"
            )
    except Exception as e:
        return Response(
            {'Error': "Thông tin không đúng, lỗi: " + str(e)},
            status=ERROR_CODE,
            content_type="application/json"
            )


####################################################################################################

@api_view(["POST"])
def Register(request):
    try:
        _email = request.POST.get('email').lower()
        _name = request.POST.get('name')
        _position = request.POST.get('position')
        _password = request.POST.get('password').lower()
        _phone = request.POST.get('phone')
        
        user = None
        try:
            user =  User.objects.get(email=_email, isDeleted=False)
            already_existed = True
        except User.MultipleObjectsReturned:
            already_existed = True
        except User.DoesNotExist:
            already_existed = False
        
        hashed_password = HashPassword(_password)
        
        if(user == None):
            user = User(email = _email)
        else:
            if(user.status != "Invited"):
                return ErrorResponse("Email này đã được đăng ký")

        user.fullname = _name
        user.password = hashed_password
        user.phone = _phone        
    
       
        user.timeUpdate = datetime.datetime.utcnow()

        user.save()

        #create login session
        login_session = LoginSession(email = _email,
                                    fullname = user.fullname,
                                    level = user.level,
                                    purpose = "ConfirmEmail",
                                    loginTime = datetime.datetime.utcnow(),
                                    validTo = datetime.datetime.utcnow() + datetime.timedelta(days=7)
                                    )
        login_session.save()

        SendEmailAsync("Xác nhận đăng ký tài khoản",
                    "<!DOCTYPE html>" +
                    "<html><head></head><body>" +
                    "<p>Xin chào bạn</p>" +		
                    "<p>Bạn nhận được email vì đã đăng ký sử dụng dịch vụ tại " + settings.HOST + ". </br>" + 
                    "Nếu đúng là bạn thì click vào link bên dưới để xác nhận email, nếu không phải bạn xin vui lòng bỏ qua email này.</p> </br>" +
                    "<p>" + settings.HOST + "/redirect?token=" + str(login_session.pk) + "</p>" +
                    "<p>Đây là email tự động, vui lòng không reply.</p>" +
                    "</body></html>",
                    _email
                )

        return SuccessResponse("Đăng ký thành công, vui lòng kiểm tra email để xác nhận")
    except Exception as e:
            return ErrorResponse("Có lỗi: " + str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdateUser(request):
    try:
        _pk = GetParam(request, 'pk')
        _phone = GetParam(request, 'phone')
        _email = GetParam(request, 'email')
        _fullname = GetParam(request, 'fullname')
        _address = GetParam(request, 'address')
        _nameLogin = GetParam(request, 'nameLogin')
        _level = GetParam(request, 'level')
        _password = request.POST.get('password')
        _newPassword = request.POST.get('newPassword')
        _newPasswordConfirm = request.POST.get('newPasswordConfirm')
        _typeLogin = GetParam(request, 'typeLogin')
        addUser = True


        if(IsPk(_pk)):
            user = User.objects.get(pk=_pk, isDeleted=False)  
            addUser = False   
            if(_newPassword != None and _newPassword != ""):
                if(_newPassword != _newPasswordConfirm):
                   return ErrorResponse("Mật khẩu mới và mật khẩu xác nhận không trùng khớp") 
            if(_password != None and _password != ""):
                hashed_password = HashPassword(_password)
                if(user.password != hashed_password):
                    return ErrorResponse("Password cũ không đúng")
                if(_newPassword != None and _newPassword != ""):
                    hashed_newpassword = HashPassword(_newPassword)
                    user.password = hashed_newpassword
        elif(_typeLogin != None and _typeLogin == "google"):
            try:
                user = User.objects.get(email=_email, isDeleted=False)
                return JsonResponse(user.to_json())  
            except User.DoesNotExist:
                try:
                    userDeleted = User.objects.get(email=_email, isDeleted=True)
                    userDeleted.email = GenerateRandomString() + "deleted"
                    userDeleted.save()
                except User.DoesNotExist:
                    pass
                user = User()
                user.email = _email
                user.password = HashPassword('123456789')
                user.level = _level
                user.fullname = _fullname
                user.timeRegister = utcnow()
                user.save()
                return JsonResponse(user.to_json())
        else:
            users = User.objects(phone=_phone, isDeleted=False)
            if len(users) > 0:
                return ErrorResponse("Số điện thoại này đã được đăng ký")
            else:
                users = User.objects(nameLogin=_nameLogin, isDeleted=False)
                if len(users) > 0:
                    return ErrorResponse("Tên đăng nhập này đã được đăng ký")
                else:
                    user = User() 
                    user.timeRegister = utcnow()
                    if(_password != None and _password != ""):
                        hashed_password = HashPassword(_password)
                        user.password = hashed_password
                    else:
                        return ErrorResponse("Chưa nhập mật khẩu")
                
        if _phone != None and _phone != '':
            user.phone = _phone
        if _email != None and _email != '':
            user.email = _email
        if _fullname != None and _fullname != '':
            user.fullname = _fullname
        if _address != None and _address != '':
            user.address = _address
        if _nameLogin != None and _nameLogin != '':
            user.nameLogin = _nameLogin
        if _level != None and _level != '':
            user.level = _level
        user.timeUpdate = utcnow()
        user.save()
        if addUser:
            return SuccessResponse("Thêm User thành công")
        return SuccessResponse("Cập nhật User thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
####################################################################################################

@api_view(["POST"])
def DeleteUser(request):
    try:
        _token = GetParam(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')
        _level = RequireParamExist(request, 'level')
        if _level != "Root" and _level != "Admin":
            return ErrorResponse("Bạn không có quyền xóa")
        if(IsPk(_pk)):
            user = User.objects.get(pk=_pk, isDeleted=False)  
        else:
            return ErrorResponse("Không tìm thấy người dùng")
        user.isDeleted = True
        user.save()
        return SuccessResponse("Xóa User thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
####################################################################################################

@api_view(["POST"])
def CheckViewAbleUser(request):
    try:
        _token = request.POST.get('token')
        jwt = api.auth.decode(_token)

        user = User.objects.get(phone=jwt["phone"], isDeleted=False) 
        pets = Pet.objects(owner = user.phone, isDeleted = False)
        now = datetime.datetime.utcnow() + datetime.timedelta(hours=7)
        viewAble = False

        if user.level == "Customer":
            for pet in pets:
                if pet.dateStart + datetime.timedelta(hours=7) <= now <= pet.dateEnd + datetime.timedelta(hours=7):
                    viewAble = True
                    break
                else:
                    viewAble = False
        else: 
            viewAble = True
        obj = {
        "viewAble" : viewAble,
        "phone" : jwt["phone"],
        'now' : now
        }
        return ObjResponse(obj)
    except Exception as e:
        return ErrorResponse(str(e))