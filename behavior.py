from AAPI import *
from scipy.stats import norm
import numpy as np


track_stop = []
track_proc = []

acce = []
dece = []

start_yellow = []
dur_yellow = []

def AAPILoad():
	AKIPrintString( "AAPILoad" )
	return 0

def AAPIInit():
	AKIPrintString( "AAPIInit" )
	return 0

def AAPIManage(time, timeSta, timeTrans, acycle):
    	AKIPrintString( "AAPIManage" )
        nba = AKIInfNetNbSectionsANG()
        # read the number of road setions


        #for every section, determine the light state and get the information of vehicles
        for i in range(0,nba):
                #id of section
                id_section = AKIInfNetGetSectionANGId(i)
                #read the state of light at every line
        
                #read current phase
                phase = ECIGetCurrentPhase(457)
        
                #number of traffic lights at 1 section
#                num_light = ECIGetNumberSem(id_section, 1, timeSta)
                
                if id_section == 453 or id_section == 455 or id_section == 448 or id_section == 450:
                        num_light = 1
                else:
                        num_light = 0
                
                for j in range(0, num_light):
#                        light = ECIGetStateSem(id_section, 1, j, timeSta)
#                        light = 2
                        #change behavior if it's the beginning time of yellow
                        start_time = ECIGetStartingTimePhase(457)
#                        if light == 2 and timeSta == start_time:
                        if (phase == 2 or phase == 4) and timeSta == start_time:
                                #read the duration of yellow
                                pdur = doublep()
                                pcmax = doublep()
                                pcmin = doublep()
                                ECIGetDurationsPhase(457, phase, timeSta, pdur, pcmax, pcmin)
                                dur = pdur.value()
#                                print('time '+str(timeSta)+' and dur '+str(dur))
                                if start_yellow == []:
                                    start_yellow.append(timeSta)
                                if dur_yellow == []:
                                    dur_yellow.append(dur)
                
                                #number of vehicles in the section
                                if phase == 2 and (id_section == 448 or id_section == 453):
                                    num_veh = AKIVehStateGetNbVehiclesSection(id_section,True)
                                elif phase == 4 and (id_section == 450 or id_section == 445):
                                    num_veh = AKIVehStateGetNbVehiclesSection(id_section,True)
                                else:
                                    break
                                #read the info for every vehicles
                                for m in range(0,num_veh):
                                        #read info of vehicels
                                        veh = AKIVehStateGetVehicleInfSection(id_section, m)
                                        AKIVehSetAsTracked(veh.idVeh)
                                        infStatic = AKIVehTrackedGetStaticInf (veh.idVeh)
                    
                                        #probability of choosing to stop
#                                        print('spped'+str(veh.CurrentSpeed))
                                        X = (5.28*veh.distance2End/veh.CurrentSpeed-3.9-0.0174*veh.CurrentSpeed)/1.55
                                        prob = norm.cdf(X)
                    
                                        #generate random decisino variable
                                        decision = np.random.binomial(1,prob,1)
                    
                                        #classify vehicles by their choice
                                        if decision == 1:
                                                track_stop.append(veh)
                                                t_reaction = infStatic.reactionTimeAtTrafficLight
                                                v = veh.CurrentSpeed/3.6
                                                min_deceleration = 2*(v*(t_reaction+dur)-veh.distance2End)/(dur**2)
                                                deceleration = np.random.uniform(min_deceleration,infStatic.maxDeceleration)
                                                dece.append(deceleration)
                                        else:
                                                track_proc.append(veh)
                                                t_reaction = infStatic.reactionTimeAtTrafficLight
                                                v = veh.CurrentSpeed/3.6
                                                min_acceleration = 2*(veh.distance2End-v*(t_reaction+dur))/(dur**2)
                                                acceleration = np.random.uniform(min_acceleration,infStatic.maxAcceleration)
                                                acce.append(acceleration)
        #modify speed for next time step
#        print('start yellow '+str(start_yellow))
#        print('duration yellow '+ str(dur_yellow))
        if start_yellow != [] and (timeSta-start_yellow[0] <= dur_yellow[0]):
#                print(timeSta)
#                print('modify sets')

                if track_stop != []:
                        for i in range(0, len(track_stop)):
                                veh = track_stop[i]
                                current_speed = veh.CurrentSpeed
                                AKIVehTrackedModifySpeed(veh.idVeh, current_speed - dece[i])
                if track_proc != []:
                        for j in range(0, len(track_proc)):
                                veh = track_proc[j]
                                current_speed = veh.CurrentSpeed
                                AKIVehTrackedModifySpeed(veh.idVeh, current_speed + acce[j])
                if timeSta - start_yellow[0] == dur_yellow[0]:
                        del start_yellow[:]
                        del dur_yellow[:]
                        del track_stop[:]
                        del track_proc[:]              
#        print(start_yellow)
#        print(dur_yellow)
        return 0

def AAPIPostManage(time, timeSta, timeTrans, acycle):
	AKIPrintString( "AAPIPostManage" )
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
