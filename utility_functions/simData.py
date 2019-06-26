import pandas as pd
import numpy as np
import random

def simData(df, VarName, Dist, nRows): 
    '''
    input: 
          df = a given data frame, also the output data frame
          Dist   = a list of positive numbers sum to 1, for the distribution
                   of the new categorical variable.
          nRows  = an integer for the number of observations in case df is empty; 
                   otherwise, not used  
          VarName = list of Variable name, for instance ['race']                   
    '''
    #checking if df is an empty dataframe
    if df.empty:
        print('Input DataFrame is empty. Still proceed ahead.')
        # now will create a new dataframe based on given information
        # checking if Dist is a distribution       
        if sum(1 for number in Dist if number <= 0) > 0 or sum(Dist) != 1:  
            print("Your Dist contains non-positive number(s) or it doesn't sum up to 1")
            return
        rowNumber = nRows
    else:
        rowNumber = df.shape[0]
    type = np.transpose(np.arange(len(Dist)))
    df[VarName] =  np.matmul(np.random.multinomial(1, Dist, size=rowNumber), type)   
    return df       
        