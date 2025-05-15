# from django.shortcuts import render
# from rest_framework.views import APIView
# from rest_framework.decorators import api_view
# import json
# import hashlib
# import datetime
# from dateutil.parser import parse
# from api.models import Activity, User
# from api.apps import *
# from mongoengine.queryset.visitor import Q
# from api.auth import *
# from lib.TGMT.TGMTpaging import Paging

# ####################################################################################################

# def AddActivity(email, activity, value):
#     try:
#         activity = Activity(
#             email=email,
#             activity=activity,
#             value=value,
#             timeCreate = utcnow()
#         )
#         activity.save()
#         return True    
#     except Exception as e:
#         return False

# ####################################################################################################

# @api_view(["POST"])           
# def GetActivityList(request):
#     try:
#         _token = request.POST.get("token")
#         loginSession = api.auth.decode(_token)

#         RequireLevel(loginSession, ["Root", "Admin"])            

#         _fromDateStr = request.POST.get("fromDate")
#         _toDateStr = request.POST.get("toDate")

#         _fromDate = parse(_fromDateStr) + datetime.timedelta(hours=-7)
#         _toDate = parse(_toDateStr) + datetime.timedelta(days=1) + datetime.timedelta(hours=-7)

#         activities = Activity.objects(timeCreate__gte=_fromDate, timeCreate__lt=_toDate, isDeleted=False)
            

#         _search_string = GetParam(request, "search_string")
#         if(_search_string != None and _search_string != ""):
#             if(IsPk(_search_string)):
#                 activities = activities(person_pk=_search_string)
#             else:
#                 activities = activities.filter(Q(email__icontains=_search_string) |
#                                                 Q(activity__icontains=_search_string) |
#                                                 Q(value__icontains=_search_string))
                                                

#         _order_by = request.POST.get('order_by')
#         if(_order_by != None and _order_by == "desc"):
#             activities = activities.order_by("-timeCreate")
#         respond = Paging(request, activities)

#         return ObjResponse(respond)
#     except Exception as e:
#         return ErrorResponse("Có lỗi: " + str(e))

####################################################################################################
