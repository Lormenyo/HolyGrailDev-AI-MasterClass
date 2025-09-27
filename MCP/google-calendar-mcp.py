from fastapi import FastAPI
from pydantic import BaseModel
from googleapiclient.discovery import build
from google.oauth2 import service_account
import datetime

app = FastAPI()

# Auth
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = '../credentials.json'

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)


class CreateEventRequest(BaseModel):
    summary: str
    start: str  # ISO datetime
    end: str
    timeZone: str = "Europe/Dublin"


@app.post("/create_event")
def create_event(req: CreateEventRequest):
    event = {
        'summary': req.summary,
        'start': {'dateTime': req.start, 'timeZone': req.timeZone},
        'end': {'dateTime': req.end, 'timeZone': req.timeZone},
    }
    created = service.events().insert(calendarId='primary', body=event).execute()
    return {"message": "Event created", "event": created}


@app.get("/list_events")
def list_events():
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    week = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'
    events_result = service.events().list(
        calendarId='primary', timeMin=now, timeMax=week,
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return {"events": events}
