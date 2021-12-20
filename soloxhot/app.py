#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

# from flask.ext.sqlalchemy import SQLAlchemy
import logging

from logging import Formatter, FileHandler

import os

import random

from datetime import date
from datetime import timedelta
from csv import writer
from csv import DictWriter

import csv


import schedule
from apiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials



SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
#KEY_FILE_LOCATION = 'gaapi-332219-9cecd4bb241a.json'
#VIEW_ID = '247863439'
KEY_FILE_LOCATION = 'gaapi-332219-f2f31b5979f7.json'
VIEW_ID = '104656524'
today = date.today()
yesterday = today - timedelta(days = 1)

def initialize_analyticsreporting():
  
    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        KEY_FILE_LOCATION, SCOPES)

    # Build the service object.
    analytics = build('analyticsreporting', 'v4', credentials=credentials)

    return analytics

def get_report(analytics):
    
    

    return analytics.reports().batchGet(
        body={
            'reportRequests': [
            {
            'viewId': VIEW_ID,
            'dateRanges': [{'startDate': str(yesterday), 'endDate': str(yesterday)}],
            'metrics': [{'expression': 'ga:sessions'}],
            #'dimensions': [{'name': 'ga:country'}]
            }]
        }
    ).execute()

def print_response(response):

    for report in response.get('reports', []):
        columnHeader = report.get('columnHeader', {})
        dimensionHeaders = columnHeader.get('dimensions', [])
        metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

        for row in report.get('data', {}).get('rows', []):
    
            dimensions = row.get('dimensions', [])
            dateRangeValues = row.get('metrics', [])

            for header, dimension in zip(dimensionHeaders, dimensions):
                print(header + ': ' + dimension)
            

            for i, values in enumerate(dateRangeValues):
                print('Date range: ' + str(i))
                for metricHeader, value in zip(metricHeaders, values.get('values')):
                    print(metricHeader.get('name') + ': ' + value)
                    print(value)
                
                    data = [str(value), str(yesterday)]

                    with open('countries.csv', 'a+', newline='', encoding='UTF8') as f:
                        writer = csv.writer(f)

                        

                        # write the data
                        writer.writerow(data)


analytics = initialize_analyticsreporting()
response = get_report(analytics)
print_response(response)
  
def job():
    print("I'm working...")

schedule.every(10).minutes.do(job)
schedule.every().hour.do(job)
schedule.every().day.at("10:30").do(job)

while 1:
    schedule.run_pending()
    time.sleep(1)
    
