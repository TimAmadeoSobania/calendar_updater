# This script is used to update the google calendar with the events from the website of the 'Gruene Bielefefd'
# Author: Tim Sobania (tim.sob25@gmail.com)
# Date: 2025-01-14

import requests
import time
from ics import Calendar
import googleapiclient
import json

import setup_calendar


with open('endpoints.json', 'rb') as json_data:
    endpoints = json.load(json_data)
    json_data.close()

client = setup_calendar.get_calendar_service()


def main():
    print("Deleting all events")
    delete_all_events(endpoints['cal_id'])
    print(f"Getting calendar from website: {endpoints['cal_id']}")
    calendar = get_calendar_from_website(endpoints['url'])
    print("Creating events")
    create_events(calendar, endpoints['cal_id'])
    print("Done")

def delete_all_events(cal_id:str, retry:int=20):
    try:
        all_events = client.events().list(calendarId=cal_id, singleEvents=True).execute()
        for event in all_events['items']:
            client.events().delete(calendarId=cal_id, eventId=event['id']).execute()
    except googleapiclient.errors.HttpError as e:
        if retry > 0:
            print(f"Failed to delete all events, retrying in 10 seconds. Number of events: {len(all_events['items'])}")
            time.sleep(10)
            delete_all_events(cal_id, retry-1)
        else:
            raise e

def get_calendar_from_website(url:str):
    return Calendar(str(requests.get(url).content, "utf-8", errors='ignore'))

def create_events(calendar, cal_id):
    for event in calendar.events:
        client.events().insert(calendarId=cal_id, body={
            'summary': event.name,
            'description': event.description,
            'location': event.location,
            'start': {'dateTime': event.begin.isoformat()},
            'end': {'dateTime': event.end.isoformat()},
        }).execute()

if __name__ == '__main__':
    main()