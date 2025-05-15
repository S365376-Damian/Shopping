import os
from rest_framework.decorators import api_view
import json
import hashlib
from datetime import datetime, timedelta
from dateutil import parser
from dateutil.parser import parse
from api.models import Shop, User, LoginSession, Product
from django.core.exceptions import MultipleObjectsReturned, ObjectDoesNotExist
from api.apps import *
import api.auth
from django.conf import settings
from lib.TGMT.TGMTpaging import Paging
from lib.TGMT.TGMTfile import MkDir
from lib.TGMT.TGMTimage import SaveImageFromRequest

####################################################################################################

@api_view(["POST"])
def GetProductList(request):
    try:
        _token = GetParam(request, "token")
        jwt = api.auth.decode(_token)
        _pk = GetParam(request, "pk")    
        _all = GetParam(request, "all")      
        try:
            user = User.objects.get(phone=jwt["phone"], isDeleted=False) 
        except User.DoesNotExist:
            user = User.objects.get(email=jwt["email"], isDeleted=False)
        productTable = Product.objects(isDeleted=False)   
        if(user.level == "Admin_Shop" and _all != "all"):
            shop = Shop.objects.get(user_pk=str(user.pk), isDeleted=False) 
            productTable = productTable.filter(shop_pk = str(shop.pk))   
      
        if(_pk != None and _pk != ''):
            productTable = Product.objects(pk = _pk, isDeleted=False)  
        respond = Paging(request, productTable)
        return ObjResponse(respond)
    except Exception as e:
        return ErrorResponse(str(e))
    
####################################################################################################

@api_view(["POST"])
def UpdateProduct(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = GetParam(request, 'pk')
        _product_code = GetParam(request, 'product_code')
        _product_name = GetParam(request, 'product_name')
        _price = GetParam(request, 'price')
        _size = GetParam(request, 'size')
        _group = GetParam(request, 'group')
        _type = GetParam(request, 'type')
        _material = GetParam(request, 'material')
        _color = GetParam(request, 'color')
        _describe = GetParam(request, 'describe')
        _check = GetParam(request, 'check')
        _image = GetParam(request, 'image')
        
        shop = None
        try:
            user = User.objects.get(phone=jwt["phone"], isDeleted=False) 
        except User.DoesNotExist:
            user = User.objects.get(email=jwt["email"], isDeleted=False)
        if(user.level == "Admin_Shop"):
            shop = Shop.objects.get(user_pk=str(user.pk), isDeleted=False) 

        product = None
        if(IsPk(_pk)):
            try:
                product = Product.objects.get(pk=_pk, isDeleted=False)
            except Product.DoesNotExist:      
                pass
        
        if(product == None):
            product = Product(dateCreate = utcnow())
        if(_product_code != None and _product_code != ''):
            product.product_code = _product_code
        if _product_name != None and _product_name != "":
            product.product_name = _product_name
        if _price != None and _price != '':
            product.price = _price
        product.size = _size
        product.group = _group
        product.type = _type
        product.material = _material
        product.color = _color
        product.describe = _describe
        if(_check == "True"):
            product.check = True
        else:
            product.check = False
        if _image != None and _image != "":
            product.image = _image
        product.dateUpdate = utcnow()

        if(shop != None):
            product.shop_pk = str(shop.pk)
            product.shop_name = shop.name
        product.save()
        folder = os.path.join("product", str(product.pk))
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, "product", str(product.pk))):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, "product", str(product.pk)))
        else:
            product.imagePaths = None
            for filename in os.listdir(os.path.join(settings.MEDIA_ROOT, "product", str(product.pk))):
                file_path = os.path.join(os.path.join(settings.MEDIA_ROOT, "product", str(product.pk)), filename)
                try:
                    # Kiểm tra xem đây có phải là tệp không và xóa tệp
                    if os.path.isfile(file_path):
                        print(file_path)
                        os.remove(file_path)
                except Exception as e:
                    print(f"Không thể xóa tệp {file_path}. Lỗi: {e}")
        MkDir(os.path.join(settings.MEDIA_ROOT, folder))
        imgList = SaveImageFromRequest(request, folder)

        if(len(imgList) > 0):
            product.imageDir = folder                
            product.imagePaths += imgList
        product.save()
        return SuccessResponse("Cập nhật thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))
    
    
####################################################################################################

@api_view(["POST"])
def DeleteProduct(request):
    try:
        _token = RequireParamExist(request, "token")
        jwt = api.auth.decode(_token)

        _pk = RequireParamExist(request, 'pk')
        if jwt["level"] not in ["Root", "Admin"]:
            return ErrorResponse("Bạn không có quyền xóa!")
        product = Product.objects.get(pk=_pk, isDeleted=False)
        product.isDeleted = True 
        product.save()
        return SuccessResponse("Xóa thành công")
    except Exception as e:
        return ErrorResponse("Có lỗi: " + str(e))