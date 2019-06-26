import pandas as pd
import numpy as np
import random
import os
import argparse
from utility_functions.simData import simData 
import pdb # for debugging purpose 

def main():
    cmd_parse = argparse.ArgumentParser(description = 'Abbott', formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # sample size argument
    cmd_parse.add_argument('-s', '--samplesize', default = 100, required = True, help = 'Number of observations, when making fake file')
    cmd_parse.add_argument('-path', '--csvpath', required = False, help = 'Specify path to csv output files')

    cmd_args = cmd_parse.parse_args()

    # read in sample size information
    samplesize = int(cmd_args.samplesize)

    # creating a fake data with demographic information
    df = pd.DataFrame(np.arange(1, samplesize+1), columns=['person_id'])
    Dist = [.2, .6,.2]
    label={0:"Latino",1:"White", 2:"Other"}
     # adding new variable of race
    df = simData(df, 'Race', Dist, 100)
    df['race_cat']=df.Race.map(label)
    df = simData(df, 'Male', [.47, .53], 100)
    df['age'] = np.random.randint(18, 64, size=samplesize)
    #print(df.head())

    #writing out as csv file to a specific path
    csvpath = cmd_args.csvpath

    curr_path = os.path.abspath(__file__)
    curr_path = os.path.dirname(curr_path)
    
    if csvpath is None: #no path specified, setting to the out_files folder
        csvpath= os.path.join(str(curr_path), 'out_files')
    if not os.path.exists(csvpath):
        os.makedirs(csvpath)
    df.to_csv(os.path.join(csvpath,r'demo.csv'))

    # creating a fake transportation data
    
if (__name__ == '__main__'):
    main()
        
        