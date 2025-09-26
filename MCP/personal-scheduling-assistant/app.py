import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
from openai import OpenAI
import datetime
import json

today = datetime.datetime.now().strftime("%Y-%m-%d")

# Load API key from Streamlit secrets
OPENAI_API_KEY = st.secrets["OPENAI_API_KEY"]

# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY,
                base_url="https://openrouter.ai/api/v1",)

# -----------------------
# GOOGLE CALENDAR SETUP
# -----------------------
SCOPES = ['https://www.googleapis.com/auth/calendar']
SERVICE_ACCOUNT_FILE = '../../credentials.json'  

creds = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES)
service = build('calendar', 'v3', credentials=creds)

# -----------------------
# STREAMLIT UI
# -----------------------
st.title("📅 AI Google Calendar Assistant")
st.write("Balance your work, health, fun, rest, and learning goals automatically.")

# Weekly goals input
work = st.text_input("Work goal", "20 hours coding this week")
health = st.text_input("Health goal", "3 gym sessions")
fun = st.text_input("Fun goal", "2 social activities")
rest = st.text_input("Rest goal", "1 evening off per week")
learning = st.text_input("Learning goal", "5 hours AI study")

if st.button("Generate & Add Weekly Plan"):
    weekly_goals = {
        "work": work,
        "health": health,
        "fun": fun,
        "rest": rest,
        "learning": learning
    }

    # -----------------------
    # FETCH CALENDAR EVENTS
    # -----------------------
    now = datetime.datetime.utcnow().isoformat() + 'Z'
    week_later = (datetime.datetime.utcnow() + datetime.timedelta(days=7)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        timeMax=week_later, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    # Summarize busy times
    calendar_summary = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        calendar_summary.append(f"{event['summary']} from {start} to {end}")

    # -----------------------
    # LLM PLANNING (Structured JSON)
    # -----------------------
    st.write("🧠 Generating your structured weekly plan with AI...")

    response = client.chat.completions.create(
        model="mistralai/mistral-7b-instruct",
        messages=[
            {"role": "system", "content": "You are a helpful scheduling assistant."},
            {"role": "user", "content": f"My weekly goals: {weekly_goals}. "
                                        f"Here are my existing events: {calendar_summary}. "
                                        f"Please generate an optimized weekly plan as a JSON list of events with fields: summary, start, end. "
                                        f"Use ISO 8601 datetime format (YYYY-MM-DDTHH:MM:SS). Limit to the next 7 days."}
        ]
    )

    try:
        plan_json = response.choices[0].message.content
        print("AI Response:", plan_json)  # Debugging line
        plan = json.loads(plan_json)  # Expecting JSON from AI
    except Exception as e:
        st.error("⚠️ Could not parse AI response as JSON. Check output.")
        st.text(plan_json)
        st.stop()

    # -----------------------
    # ADD EVENTS TO GOOGLE CALENDAR
    # -----------------------
    st.subheader("✨ Your AI-Generated Weekly Plan")
    for event in plan:
        st.write(f"- {event['summary']} | {event['start']} → {event['end']}")

        new_event = {
            'summary': event['summary'],
            'start': {'dateTime': event['start'], 'timeZone': 'Europe/Dublin'},
            'end': {'dateTime': event['end'], 'timeZone': 'Europe/Dublin'},
        }
        service.events().insert(calendarId='primary', body=new_event).execute()

    st.success("✅ All events have been added to your Google Calendar!")
