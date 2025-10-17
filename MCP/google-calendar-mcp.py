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
    calendarId: str
    timeZone: str = "Europe/Dublin"

class ListEventsRequest(BaseModel):
    calendarId: str
    timeMin: str  # ISO datetime
    timeMax: str  # ISO datetime

@app.post("/create_event")
def create_event(req: CreateEventRequest):
    event = {
        'summary': req.summary,
        'start': {'dateTime': req.start, 'timeZone': req.timeZone},
        'end': {'dateTime': req.end, 'timeZone': req.timeZone},
    }
    created = service.events().insert(calendarId=req.calendarId, body=event).execute()
    return {"message": "Event created", "event": created}


@app.get("/list_events")
def list_events(req: ListEventsRequest):
    events_result = service.events().list(
        calendarId=req.calendarId, timeMin=req.timeMin, timeMax=req.timeMax,
        singleEvents=True, orderBy='startTime').execute()
    events = events_result.get('items', [])
    return {"events": events}
