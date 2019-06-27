import pandas as pd
import numpy as np
import random
import os
import argparse

import matplotlib.pyplot as plt
import matplotlib.ticker as mtick

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
    # for now, only race, gender and age
    df = pd.DataFrame(np.arange(1, samplesize+1), columns=['person_id'])
    Dist = [.1, .05, .4, .3, .01,.04, .1]
    label={0 : "African American", 1 : "Asian", 2 : "White", 3 : "Hispanic", 4 : "Native American",  
           5 : "Pacific Islander", 6 : "Other"}
     # adding new variable of race
    df = simData(df, 'Race', Dist, samplesize)
    # create a categorical version of race, by applying the dictionary
    df['race_cat']=df.Race.map(label)
    df = simData(df, 'Male', [.47, .53], samplesize)
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


    # creating a fake longitudinal data, a person could have multiple rows
    # this is not useful for the time being, but the technique might be, so the code stays
    transportation = df
    transportation.drop('Race', axis=1, inplace=True)

    # expanding the data by the size of window for each person
    transportation['window'] = np.random.randint(1, 10, size=samplesize)
    transportation = transportation.reindex(transportation.index.repeat(transportation.window))
    transportation['time'] = transportation.groupby(level=0).cumcount()+1
    transportation.drop('window', axis=1, inplace=True)

    # transportation type
    transportation = simData(transportation, 'type', [.30, .70], samplesize) 
    type_label = {0 : "Diabetes-related", 1 : "Not Diabetes-related"}
    transportation['diabetes_related']=transportation.type.map(type_label)

    # creating a baseline survey data, cross-sectional
    mts = pd.DataFrame(np.arange(1, samplesize+1), columns=['person_id'])
    mts = simData(mts, 'diab_related', [.30, .70], samplesize) 
    mts['n_appointment'] = np.random.randint(0, 5, size=samplesize)
    mts['n_missed_apmt'] = mts["n_appointment"].apply(lambda x: random.randrange(x) if x > 0 else 0)
    mts['n_diab_visits'] = mts["n_appointment"].apply(lambda x: random.randrange(x) if x > 0 else 0)
    
    mts['n_er_visits'] = np.random.randint(0, 3, size=samplesize)
    mts = simData(mts, 'diabetes_related', [.30, .70], samplesize) 
    type_label = {0 : "Diabetes-related", 1 : "Not Diabetes-related"}
    mts['diabetes_related']=mts.diabetes_related.map(type_label)

    mts.to_csv(os.path.join(csvpath,r'mts.csv'))

    # merging demographic data with baseline survey data
    mts_and_demo = pd.merge(df, mts, on='person_id')
    print(mts_and_demo.head())

    mts_and_demo.to_csv(os.path.join(csvpath,r'mts_and_demo.csv'))


    #plotting, this code below could be split into a couple of steps...
    #if matplotlib doesn't exist, one has to install it, say via "pip install matplotlib"
    race_gender = mts_and_demo.groupby(['Male', 'race_cat']).size().groupby(level=0).apply(
                  lambda x: 100*x/x.sum()).unstack().plot(kind='bar', stacked=True)
    plt.gca().yaxis.set_major_formatter(mtick.PercentFormatter())
    plt.savefig(os.path.join(csvpath,r'race_gender.png'))

if (__name__ == '__main__'):
    main()
        
        