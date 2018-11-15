from AAPI import *
import scipy as sc


track_stop = []
track_proc = []

acce = []
dece = []

def AAPILoad():
	AKIPrintString( "AAPILoad" )
	return 0

def AAPIInit():
	AKIPrintString( "AAPIInit" )
	return 0

def AAPIManage(time, timeSta, timeTrans, acycle):
	AKIPrintString( "AAPIManage" )
    
    #get the number of road setions
    nba = AKIInfNetNbSectionsANG()
    
    #for every section, determine the light state and get the information of vehicles
    for i in range(0,nba):
        #id of section
        id_section = AKIInfNetGetSectionANGId(i)
        #read the state of light at every line
        
        #number of traffic lights at 1 section
        num_light = ECIGetNumberSem(id_section, 1, timeSta)
        for j in range(0, num_light):
            light = ECIGetStateSem(id_section, 1, j, timeSta)
            
            #change behavior if it's the beginning time of yellow
            start_time = ECIGetStartingTimePhase(457)
            if light == 2 and timeSta == start_time:
                #number of vehicles in the section
                num_veh = AKIVehStateGetNbVehiclesSection(id_section,True)
                for m in range(0,num_veh):
                    #read info of vehicels
                    infVeh = AKIVehStateGetVehicleInfSection(id_section, m)
                    
                    #probability of choosing stop
                    X = 
                    prob = sc.stats.norm.cdf()
                
    
    
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
