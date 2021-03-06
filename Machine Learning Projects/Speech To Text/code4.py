from __future__ import print_function
import datetime
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import time
import playsound
import speech_recognition as sr
import pyttsx3
import pytz

# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']
MONTHS=["january","february","march","april","may","june","july","august","september","october","november","december"]
DAYS=["monday","tuesday","wednesday","thursday","friday","saturday","sunday"]
DAYS_EXTENSIONS=["rd","th","st","nd"]

def speak(text):
    engine=pyttsx3.init()
    engine.say(text)
    engine.runAndWait()



def get_audio():
    r=sr.Recognizer()
    with sr.Microphone() as source:
        audio=r.listen(source)
        said=""
        try :
            said=r.recognize_google(audio)
            print(said)
        except Exception as e:
            print("Exception"+str(e))
    return said

text=get_audio()

            





def authenticate_google():
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    service = build('calendar', 'v3', credentials=creds)
    return service

def get_events(day,service):
    date=datetime.datetime.combine(day,datetime.min.time())
    end_date=datetime.datetime.combine(day,datetime.max.time())
    utc=pytz.UTC
    date=date.astimezone(utc)
    end_date=date.astimezone(utc)
    # Call the Calendar API
    now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
    print(f'Getting the upcoming {n} events')
    events_result = service.events().list(calendarId='primary', timeMin=date.isoformat(),timeMax=end_date.isoformat(),
                                         singleEvents=True,
                                        orderBy='startTime').execute()
    events = events_result.get('items', [])

    if not events:
        print('No upcoming events found.')
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        print(start, event['summary'])
    
def get_date(text):
    text=text.lower()
    today=datetime.date.today()

    if text.count("today") >0:
        return today
    day=-1
    day_of_week=-1
    month=-1
    year=today.year

    for word in text.split():
        if word in MONTHS:
            month=MONTHS.index(word)+1
        elif word in DAYS:
            day_of_week=DAYS.index(word)
        elif word.isdigit():
            day=int(word)
        else:
            for ext in DAYS_EXTENSIONS:
                found=word.find(ext)
                if found>0:
                    try:
                        day=int(word[:found])
                    except:
                        pass
    if month<today.month and month!=-1:
        year=year+1
    if day<today.day and month==-1 and day!=-1:
        month=month+1
    if month==-1 and day==-1 and day_of_week!=-1:
        #only for some random day and month with only day of week input
        current_day_of_week=today.weekday()
        dif=day_of_week-current_day_of_week

        if dif<0:
            dif==7
            if text.count("next")>=1:
                dif==7
        return today+datetime.timedelta(dif)
    return datetime.date(month==month,day==day,year==year)
        
SERVICE=authenticate_google()
get_events(get_date(text),SERVICE)


