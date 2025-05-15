import string
import re
import os
import random
from api.apps import *
from django.conf import settings
import shutil
import django

####################################################################################################
       
def GetSystemInfo():
    result = {}
    try:        
        total, used, free = shutil.disk_usage("/")

        result = {
            "totalDiskSize" : (total // (2**30)),
            "usedDiskSize" : (used // (2**30)),
            "freeDiskSize" : (free // (2**30)),
            "opencv_version" : cv2.__version__,
            "django_version" : django.VERSION,
            "cascade_loaded" : False
        }
    
        return result
    except Exception as e:
        result = {
            "error" : str(e)
        }

    return result

####################################################################################################

def urlify(s):
    s = re.sub(r"[^\w\s]", '', s)
    s = re.sub(r"\s+", '-', s)
    return s

####################################################################################################

def GenerateRandomName(name):
    fileName, fileEx = os.path.splitext(name)
    fileName = urlify(fileName)
    return fileName + '.' + GenerateRandomString() + fileEx

####################################################################################################

def GenerateRandomString():
    return ''.join(random.choices(string.ascii_lowercase + "_" + string.ascii_uppercase +  string.digits, k=10))

####################################################################################################

def GenerateRandomNumber(min, max):
    n = random.randint(min, max)
    return n
