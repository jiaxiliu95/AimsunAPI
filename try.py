from AAPI import *

#initial_time =[]
initial = []
initial.append(0)
count_up = []
count_up.append(0)
count_down = []
change_phase = []

def AAPILoad():
	AKIPrintString( "AAPILoad" )
	return 0

def AAPIInit():
	AKIPrintString( "AAPIInit" )
	return 0

def AAPIManage(time, timeSta, timeTrans, acycle):
    AKIPrintString( "AAPIManage" )  
    
    #identify signal phase
    phase = ECIGetCurrentPhase(457)

    
    #determine which detectors to use
    if phase == 1:
        up_detector = 498
        down_detector = 497
    if phase == 3:
        up_detector = 502
        down_detector = 501
    if phase == 2 or phase == 4:
        count_up[0] = 0
        count_down[0] = 0
        return 0
    
    start = ECIGetStartingTimePhase(457)
    elemcontrol = ECIGetNumberJunctions()-1
    max_green = ECIGetActuatedParamsMaxGreen(elemcontrol, 457, phase)
    if (timeSta-start) <= max_green-3:
        num_det = AKIDetGetNbMeasuresAvailableInstantDetection()
        for i in range(0,num_det):
            endtime = AKIDetGetEndTimeMeasureAvailableInstantDetection(i)
    #        presence_up = AKIDetGetPresenceInstantDetectionbyId(up_detector,0,endtime)
    #        presence_down = AKIDetGetPresenceInstantDetectionbyId(down_detector,0,endtime)
            
    ##                presence = AKIDetGetPresenceCyclebyId(498, 0)
    #        print(str(i)+'th detection'+str(presence))
    ##                headway = AKIDetGetHeadwayInstantDetectionbyId(498,0,endtime)
    ##                print('headway'+str(headway))
            num_intervals_up = AKIDetGetNbintervalsOccupedInstantDetectionbyId(up_detector,0,endtime)
            num_intervals_down = AKIDetGetNbintervalsOccupedInstantDetectionbyId(down_detector,0,endtime)
            
#            #count the number of vehs to match two detectors
#            if count_up == []:
#                count_up.append(num_intervals_up)
#            else:
#                count_up[0] += num_intervals_up
            
            if count_down == []:
                count_down.append(num_intervals_down)
            else:
                count_down[0] += num_intervals_down
            
            if num_intervals_up == 0:
                if timeSta - initial[0] >= 4:
                    #whether the last veh in platoon arrives the downstream detector
                    if count_down[0] == count_up[0] and count_up[0]!=0:
#                        print(count_down)
#                        print(count_up)
                        #change phase to yellow
                        if phase == 1:
                            ECIChangeDirectPhase(457, 2, timeSta, time, acycle, 3)
                        if phase == 3:
                            ECIChangeDirectPhase(457, 4, timeSta, time, acycle, 3)

                if timeSta - initial[0] < 4:
                    return 0
            else:
                if timeSta - initial[0] >= 4:
                     if count_down[0] == count_up[0]:
                        #change phase to yellow
                        if phase == 1:
                            ECIChangeDirectPhase(457, 2, timeSta, time, acycle, 3)
                        if phase == 3:
                            ECIChangeDirectPhase(457, 4, timeSta, time, acycle, 3)
                else:
                    initial[0] = timeSta
                    count_up[0] += num_intervals_up
                    #extend
                    new_duration = timeSta-start+3
                    ECIChangeTimingPhase(457, phase, new_duration, timeSta)
#                
            
                    
                    
        
#        print(num_intervals_up)
        
#        for j in range(0,num_intervals_up):
#            if initial == 0:
#                initial = timeSta+AKIDetGetIniTimeOccupedInstantDetectionbyId(498,j,0,endtime)
        
#            initial_time.append(timeSta+AKIDetGetIniTimeOccupedInstantDetectionbyId(498,j,0,endtime))

    

#        print(timeSta)
#        n=AKIDetGetNumberDetectors()
#        vehpos = AKIVehGetVehTypeInternalPosition(53)
##        print(vehpos)
#        instant = AKIDetGetCycleInstantDetection()
##        print(instant)
        
##        print(num_det)

##        for i in range(0,n):
##                detid=AKIDetGetIdDetector(i)
##                print(detid)
##
##                if detid == 498:
##                        num = AKIDetGetCounterCyclebyId(detid, vehpos)
####                        headway = AKIDetGetFinTimeOccupedCyclebyId(detid,i,0)
##                        print(str(num))
    return 0

def AAPIPostManage(time, timeSta, timeTrans, acycle):
##	AKIPrintString( "AAPIPostManage" )
	return 0

def AAPIFinish():
	AKIPrintString( "AAPIFinish" )
	return 0

def AAPIUnLoad():
	AKIPrintString( "AAPIUnLoad" )
	return 0
	
def AAPIPreRouteChoiceCalculation(time, timeSta):
	AKIPrintString( "AAPIPreRouteChoiceCalculation" )
	return 0

def AAPIEnterVehicle(idveh, idsection):
	return 0

def AAPIExitVehicle(idveh, idsection):
	return 0

def AAPIEnterPedestrian(idPedestrian, originCentroid):
	return 0

def AAPIExitPedestrian(idPedestrian, destinationCentroid):
	return 0

def AAPIEnterVehicleSection(idveh, idsection, atime):
	return 0

def AAPIExitVehicleSection(idveh, idsection, atime):
	return 0
