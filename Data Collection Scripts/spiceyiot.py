#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Nov 14 13:38:45 2020

@author: aida
"""
import fitbit
import gather_keys_oauth2 as Oauth2
import pandas as pd 
import datetime
CLIENT_ID = '22C3XC'
CLIENT_SECRET = '89abee7d73d52607b4d8f4652243e733'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
auth2_client = fitbit.Fitbit(CLIENT_ID, CLIENT_SECRET, oauth2=True, 
                             access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)

last_record = datetime.date(2020, 12, 28)
today_date = datetime.date.today()
delta = today_date - last_record
delta_days = delta.days

#today = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))

#yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))

for i in range(0, delta_days):
    date = str((datetime.datetime.now() - datetime.timedelta(days = i)).strftime('%Y-%m-%d'))
    date_file = str((datetime.datetime.now() - datetime.timedelta(days = i)).strftime('%Y%m%d'))

    """Sleep data """
    fit_statsSl = auth2_client.sleep(date= date)
    """Steps Data"""
    steps_intraday = auth2_client.intraday_time_series('activities/steps', base_date=date)
   
    #Varibales of sleep
    stime_list = []
    slevel_list = []
    sduration_list = []
    
    #Variables of steps
    time_list = []
    value_list = []
     
    #Iterate through sleep data and append time, sleep level and number of seconds in that level
    for n,j in enumerate(fit_statsSl['sleep']):
        for i in fit_statsSl['sleep'][n]['levels']['data']:
            stime_list.append(i['dateTime'][-12:-4])
            slevel_list.append(i['level'])
            sduration_list.append(i['seconds'])
    
        #Create the dataframe    
        sleepdf = pd.DataFrame({'State':slevel_list,
                             'Time':stime_list,
                             'Duration (seconds)':sduration_list})
        
       #Save as a CSV file in my directory
        sleepdf.to_csv('/home/aida/IOT/IOT_CW/python-fitbit/sensed-data/sleep2/' + \
                       date_file+'sleep'+'.csv', \
                       columns = ['Time','State','Duration (seconds)'],header=True, 
                       index = False)
        
    #Iterate through step data and append time and step count
    for i in steps_intraday['activities-steps-intraday']['dataset']:
        print(i['time'])
        time_list.append(i['time'])
        value_list.append(i['value'])

    #Create the dataframe  
    #why is this also sleepdf???
    stepsdf = pd.DataFrame({'Time':time_list,
                         'Step count':value_list})
    
   #Save as a CSV file in my directory
    stepsdf.to_csv('/home/aida/IOT/IOT_CW/python-fitbit/sensed-data/steps2/' + \
                   date_file+'steps'+'.csv', \
                   columns = ['Time','Step count'],header=True, 
                   index = False)
