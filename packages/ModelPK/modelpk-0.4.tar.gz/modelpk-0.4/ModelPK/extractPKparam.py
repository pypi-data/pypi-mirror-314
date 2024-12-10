import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression

MODEL1="1 Compartment, IV"

def LoadData(filepath:str):
    """
    LoadData takes in a filename and loads the data into a dataframe. Only Excel (.xlsx) and CSV (.csv) files are accepted; other formats will return an error message. 
    Older Excel (.xls) files may be supported, but may require installation of dependency 'xlrd'.
    
    Input:
    filepath: the path of the file containing experimental data. Include the file extension. Please note, data should be formatted with time and concentration in columns; all datapoints in a column should have the same units. See Test_PK.xlsx for example

    Output:
    Returns a dataframe containing raw experimental data. Please assign a name for this dataframe outside of the function.
    """
    if ".csv" in filepath:
        dataframe=pd.read_csv(str(filepath))
    if ".xls" in filepath:
        dataframe=pd.read_excel(str(filepath)) 
    else:
        return print("File in wrong format") 
    return dataframe

def PrepData(dataframe:str,concentration:str,lnConc:str):
    """
    PrepData makes a copy of a dataframe, log transforms data from a column of interest, removes any rows with null values in the log transformed data, and returns a new dataframe
    containing the original data as well as a new column with log transformed data.

    Inputs:
    dataframe: the name assigned to the dataframe containing your raw data
    concentration: the name of the dataframe column containing concentration data
    lnConc: the desired name of a dataframe column containing log transformed concentration data

    Output:
    A new dataframe containing the original data containing the original data as well as a new column with log transformed data. Please assign a name to this dataframe outside of the function.
    """
    tempdf=dataframe.copy()
    ln_list=[]
    for i in dataframe.index:
        if dataframe[concentration][i]!=np.nan:
            ln_list.append(np.log(dataframe[concentration][i]))
        else:
            ln_list.append(np.nan)
    tempdf[lnConc]=ln_list
    tempdf.dropna(subset=[lnConc],inplace=True)
    tempdf.reset_index(drop=True,inplace=True)
    return tempdf

def findCmax(dataframe:str,time:str, concentration:str)->float:
    """
    This function takes in a dataframe and columns of interest, identifies the highest drug concentration in the data, and then identifies the first timepoint at which that drug concentration is measured.

    Inputs:
    dataframe: name of the dataframe containing log transformned concentration data
    time: name of dataframe column containing time data
    concentration: name of dataframe column containing concentration data

    Outputs:
    Returns a 1x2 tuple containing the values for Cmax and Tmax.
    """
    for i in dataframe.index:
        if dataframe[concentration][i]==np.nanmax(dataframe[concentration]):
            if i==0:
                Cmax=dataframe[concentration][i]
                max_idx=i
                Tmax=dataframe[time][max_idx]
                return Cmax, Tmax
            elif dataframe[concentration][i]!=dataframe[concentration][i-1]:
                Cmax=dataframe[concentration][i]
                max_idx=i
                Tmax=dataframe[time][max_idx]
    print("Cmax=",Cmax)
    print("Tmax=",Tmax)
    return Cmax, Tmax

def findT_half(dataframe:str, time:str, concentration:str, thalf_threshold:float)->float:
    """
    This takes in a dataframe, columns of interest, and a threshold expressed as a percent. Scans the data to find timepoints at which drug concentration has decreased by roughly 50%.
    Note: Since data might be sparse, drug concentration at the latter time point can fall within the percent_threshold of the target value.

    Inputs:
    dataframe: name of the dataframe containing log transformned concentration data
    time: name of dataframe column containing time data
    concentration: name of dataframe column containing concentration data
    thalf_threshold: a percent (sign not needed) representing percent. Ex: a value of 10 should be interpreted as within 10% of target value

    Outputs:
    A float that represents the time it takes for drug concentration to decrease by roughly 50%. Units are the same as the units of the time data.
    """
    t_half="Not Assigned, consider adjusting threshold"
    for i in dataframe.index:
        if dataframe[concentration][i]==np.nanmax(dataframe[concentration]):
            if i==0:
                max_idx=i
            elif dataframe[concentration][i]!=dataframe[concentration][i-1]:
                max_idx=i
        for j in dataframe.index:
            if i > max_idx and j>i:
                thresh=dataframe[concentration][j]*(thalf_threshold/100)
                if dataframe[concentration][i]/2 >= dataframe[concentration][j]-thresh and dataframe[concentration][i]/2 <= dataframe[concentration][j]+thresh:
                    t_half=dataframe[time][j]-dataframe[time][i]
                    break
    return t_half

def findCo(dataframe:str,time:str,lnConc:str, model:str=MODEL1) -> float:
    """
    This function takes in a dataframe with a column for time and a column with ln(drug concentration), fits a PK model, and returns the elimination constant k and the drug concentration at t=0.
    This function is currently only built for a 1 compartment model for IV bolus drug administration.
    
    Input:
    dataframe: name of the dataframe containing log transformned concentration data
    time: the name of dataframe column containing time data
    lnConc: the name of the dataframe column with ln(drug concentration)

    Output:
    Returns a 1x2 tuple with values for Co and k.
    """
    x = []
    y = []
    if model == MODEL1:
        testmodel = LinearRegression()
    for i in dataframe.index:
        tempvalue = dataframe[time][i]
        templist = []
        templist.append(tempvalue)
        x.append(templist)
        tempvalue2 = dataframe[lnConc][i]
        templist2 = []
        templist2.append(tempvalue2)
        y.append(templist2)
    testmodel.fit(x,y)
    lnCo = float(testmodel.intercept_)
    Co = np.exp(lnCo)
    k = float(-1*testmodel.coef_)
    return Co,k

def findPK(dataframe:str,time:str, concentration:str,lnConc:str, thalf_threshold:float, model:str=MODEL1)->float:
    """
    This function takes in a dataframe, the names of any columns of interest, a percent threshold, and the desired PK model to be fit. It passes these arguments to the functions findCo, findCmax, and findT_half, and returns a 1x5 tuple with the collected function outputs.

    Inputs:
    dataframe: name of the dataframe containing log transformned concentration data
    time: the name of dataframe column containing time data
    concentration: name of dataframe column containing concentration data
    lnConc: the name of dataframe column with ln(drug concentration)
    thalf_threshold: a percent (sign not needed) representing percent. Ex: a value of 10 should be interpreted as within 10% of target value
    model: keyword for the PK model to be applied.

    Outputs:
    Returns a 1x5 tuple with values for Co, k, Cmax, Tmax, t_half
    """
    result1 = findCo(dataframe, time, lnConc, model)
    result2 = findCmax(dataframe,time, concentration)
    result3 = findT_half(dataframe, time, concentration, thalf_threshold)
    k = result1[1]
    Co = result1[0]
    Cmax = result2[0]
    Tmax = result2[1]
    t_half = result3

    return Co,k,Cmax,Tmax,t_half