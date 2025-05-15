import datetime
import json
# from api.views.patrol import GenerateTaskPatrol
# from api.views.asset import GenerateTaskCheckAsset
# from api.views.schedule import GenerateScheduleTask

####################################################################################################

def ScheduleJob():
    f = open("crontime.txt", "w")
    f.write(str(datetime.datetime.utcnow()))
    f.close()
    # GenerateTaskPatrol()
    # GenerateTaskCheckAsset()
    # GenerateScheduleTask()
