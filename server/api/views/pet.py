from rest_framework.decorators import api_view
import json
import hashlib
import datetime
from dateutil.parser import parse
from api.models import Pet
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging

####################################################################################################

@api_view(["POST"])
def GetPetList(request):
    try:
        _token = GetParam(request, "token")
        loginSession = api.auth.decode(_token)
        _phone = GetParam(request, "phone")        
        petsTable = Pet.objects(isDeleted=False)   

        if _phone != None and _phone != "":
            petsTable = petsTable.filter(owner__icontains=_phone)
        respond = Paging(request, petsTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdatePet(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)
        
        _pk = GetParam(request, 'pk')
        _name = GetParam(request, 'name')
        _owner = RequireParamExist(request, 'owner')
        _breed = GetParam(request, 'breed')
        _color = GetParam(request, 'color')
        _gender = GetParam(request, 'gender')
        _age = GetParam(request, 'age')
        _image = GetParam(request, 'image')
        _dateStartStr = GetParam(request, 'dateStart')
        _dateStart = parse(_dateStartStr) + datetime.timedelta(hours=-7)
        _dateEndStr = GetParam(request, 'dateEnd')
        _dateEnd = parse(_dateEndStr) + datetime.timedelta(hours=-7)

        pet = None
        if(IsPk(_pk)):
            try:
                pet = Pet.objects.get(pk=_pk, isDeleted=False)
            except Pet.DoesNotExist:      
                pass

        if(pet == None):
            pet = Pet(
                dateCreate = utcnow()
                )
        pet.name = _name
        pet.owner = _owner
        pet.breed = _breed
        pet.color = _color
        pet.gender = _gender
        if _age != None and _age != "":
            pet.age = _age
        if _image != None and _image != "":
            pet.image = _image
        else:
            pet.image = settings.IMAGE_PET
        pet.dateStart = _dateStart
        pet.dateEnd = _dateEnd
        pet.dateUpdate = utcnow()
        pet.save()
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
    
####################################################################################################

@api_view(["POST"])
def DeletePet(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')
        pet = Pet.objects.get(pk=_pk, isDeleted=False)
        pet.isDeleted = True 
        pet.save()
        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))