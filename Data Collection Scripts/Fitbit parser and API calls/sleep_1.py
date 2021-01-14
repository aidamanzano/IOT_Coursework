#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  7 15:44:57 2021

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

last_record = datetime.date(2021, 12, 29)
today_date = datetime.date.today()
delta = today_date - last_record
delta_days = delta.days
date_1 = datetime.date(2021, 12, 31)
#today = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y%m%d"))

#yesterday2 = str((datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"))
for i in range(0, delta_days):
    date = str((datetime.datetime.now() - datetime.timedelta(days = i)).strftime('%Y-%m-%d'))
    date_file = str((datetime.datetime.now() - datetime.timedelta(days = i)).strftime('%Y%m%d'))

    
    """Sleep data """
    fit_statsSl = auth2_client.sleep(date=date_1)
    #print(fit_statsSl)
    slevel_list = []
    sduration_list = []
    for n,j in enumerate(fit_statsSl['sleep']):
        #print(n)
        for i in fit_statsSl['sleep'][1]['levels']['summary']:
            print(i)
            
            print(fit_statsSl['sleep'][1]['levels']['summary'][str(i)]['minutes'])       
            slevel_list.append(i)
            sduration_list.append(fit_statsSl['sleep'][1]['levels']['summary'][str(i)]['minutes'])
        
        sleep_summarydf = pd.DataFrame({'State':slevel_list,
                              'Duration (seconds)':sduration_list})
        
         
        #Save as a CSV file in my directory
        sleep_summarydf.to_csv('/home/aida/IOT/IOT_CW/python-fitbit/sensed-data/sleep/' + \
                        date_file+'summary'+'.csv', \
                        columns = ['State','Duration (seconds)'],header=True, 
                        index = False)
    
