from AAPI import *
import scipy as sc
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
                phase = ECIGetCurrentPhase(idJunction)
        
                #number of traffic lights at 1 section
                num_light = ECIGetNumberSem(id_section, 1, timeSta)
                for j in range(0, num_light):
                        light = ECIGetStateSem(id_section, 1, j, timeSta)
                        #change behavior if it's the beginning time of yellow
                        start_time = ECIGetStartingTimePhase(457)
                        if light == 2 and timeSta == start_time:
                                #read the duration of yellow
                                pdur = doublep()
                                pcmax = doublep()
                                pcmin = doublep()
                                ECIGetDurationsPhase(457, phase, timeSta, pdur, pcmax, pcmin)
                                dur = pdur.value()
                                start_yellow.append(timeSta)
                                dur_yellow.append(dur)
                
                                #number of vehicles in the section
                                num_veh = AKIVehStateGetNbVehiclesSection(id_section,True)
                                #read the info for every vehicles
                                for m in range(0,num_veh):
                                        #read info of vehicels
                                        veh = AKIVehStateGetVehicleInfSection(id_section, m)
                                        infVeh = AKIVehSetAsTracked(veh.idVeh)
                                        infStatic = AKIVehTrackedGetStaticInf (veh.idVeh)
                    
                                        #probability of choosing to stop
                                        X = (5.28*infVeh.distance2End/infVeh.CurrentSpeed-3.9-0.0174*infVeh.CurrentSpeed)/1.55
                                        prob = sc.stats.norm.cdf(X)
                    
                                        #generate random decisino variable
                                        decision = np.random.binomial(1,prob,1)
                    
                                        #classify vehicles by their choice
                                        if decision == 1:
                                                track_stop.append(infVeh)
                                                t_reaction = infStatic.reactionTimeAtTrafficLight
                                                v = infVeh.CurrentSpeed/3.6
                                                min_deceleration = 2*(v*(t_reaction-dur)-infVeh.distance2End)/(t**2)
                                                decelaration = np.random.uniform(min_deceleration,infStatic.maxDeceleration)
                                                dece.append(deceleration)
                                        else:
                                                track_proc.append(infVeh)
                                                t_reaction = infStatic.reactionTimeAtTrafficLight
                                                v = infVeh.CurrentSpeed/3.6
                                                min_acceleration = 2*(infVeh.distance2End-v*(t_reaction-dur))/(t**2)
                                                accelaration = np.random.uniform(min_acceleration,infStatic.maxAcceleration)
                                                acce.append(acceleration)
        #modify speed for next time step
        if start_yellow != [] and (timeSta-start_yellow[0] <= dur_yellow[0]):
                if track_stop != []:
                        for i in range(0, len(track_stop)):
                                veh = track_stop[i]
                                current_speed = veh.CurrentSpeed
                                AKIVehTrackedModifySpeed(veh.idVeh, current_speed - dece[i])
                if track_proc != []:
                        for j in range(0, len(track_proc)):
                                veh = trackprocp[i]
                                current_speed = veh.CurrentSpeed
                                AKIVehTrackedModifySpeed(veh.idVeh, current_speed + acce[i])
                if timeSta - start_yellow[0] == dur:
                    start_yellow.clear()
                    dur_yellow.clear()
                    track_stop.clear()
                    track_proc.clear()
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
