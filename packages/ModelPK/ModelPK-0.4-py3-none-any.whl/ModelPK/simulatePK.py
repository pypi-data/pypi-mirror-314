import numpy as np
import pandas as pd
import tellurium as te

MODEL1="1 compartment, IV"

model_1C='''
#equation for 1 compartment model (IV, mostly distributed in blood):
Ct' = -k*Ct

Ct=5.96
e=exp(1)
k=.005
'''

modellib={MODEL1:model_1C}

def findSubtherapeuticTime(findPKresult:str, subther_threshold:float,  subther_target:float, numiterations: float=1000, starttime:float=0, simendtime:float=100, numsteps:float=51, setCo:float="default", set_k:float="default", modelkey:str=MODEL1):
    """
    Takes in extracted PK parameters, Antimony model, model parameters, and values for target subtherapeutic concentration and threshold. Simulates model and returns the first timepoint at which subtherapeutic concentration is reached--please assign this result to a variable.
    This function also generates a plot of the simulation. 
    The function allows users to find i) time to subtherpeutic tail based on experimental data and ii) time to subtherpeutic tail with varying Co (here, a proxy for drug dose administered via IV bolus)

    Inputs:
    findPKresult: variable assigned to findPK results, input as a string
    subther_threshold: a percent (sign not needed) representing percent. Ex: a value of 10 should be interpreted as within 10% of target subtherapeutic concentration value
    subther_target: subtherapeutic concentration of drug
    numiterations: max number of iterations allowed for function to find the time to subtherapeutic tail; default is 1000
    starttime: Simulation start time; default is 0
    simendtime: Simulation end time; default is 100 units of time
    numsteps: Number of points to simulate from starttime to simendtime; default is 51
    setCo: if "default", Co is set to value extracted by findPK from experimental data. Otherwise, Co is any initial drug concentration in the body.
    set_k: if "default", k is set to value extracted by findPK from experimental data. Otherwise, k is any elimination rate constant. k must be positive.
    modelkey: Key from modellib entered as string.

    Output:
    A plot of the simulated change in drug concentration over time with the chosen Co
    A float representing the time (units consistent with experimental data) it takes for drug concentrations to reach subtherapeutic levels. Please assign this result to a variable.
    """
    try:
        modeltoload = modellib[modelkey]
    except KeyError:
        raise ValueError(f"Model '{modelkey}' not found in modellib.")    
    r=te.loada(modeltoload)
    r.reset()
    result=findPKresult
    if setCo=="default":
        r['Ct']=result[0]
    else:
        r['Ct']=setCo
    storeCt=r['Ct']

    if set_k=="default":
        r['k']=result[1]
    elif set_k>0:
        r['k']=set_k
    elif set_k<=0:
        print("k cannot be negative")
        return
    store_k=r['k']

    data=r.simulate(starttime,simendtime,numsteps)
    breakstatement=0
    for iteration in range(1,numiterations):
        if breakstatement==1:
            break
        else:
            for i in range(0,len(data)):
                conc=data[i,1]
                thresh=subther_target*(subther_threshold/100)
                simtime=data[i,0]
                if i==len(data)-1 and conc>subther_target:
                    r.reset()
                    r['Ct']=storeCt
                    r['k']=store_k
                    data=r.simulate(0,simtime*1.5)
                    print("Extended simulation time")
                    break
                if conc<subther_target:
                    print("Not enough steps, or simulation time too long; simulation time shortened.")
                    r.reset()
                    r['Ct']=storeCt
                    r['k']=store_k
                    data=r.simulate(0,simtime/2)
                    break
                if subther_target-thresh<=conc<=subther_target+thresh:
                    print("Found time to subtherapeutic tail")
                    subthertime=data[i,0]
                    breakstatement=1
                    r.plot(data, True, "Time","Drug Concentration")
                    break
    return subthertime