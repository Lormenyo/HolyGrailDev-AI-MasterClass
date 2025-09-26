import streamlit as st
from googleapiclient.discovery import build
from google.oauth2 import service_account
from openai import OpenAI
import datetime
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI


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
    week_later = (datetime.datetime.utcnow() +
                  datetime.timedelta(days=7)).isoformat() + 'Z'

    events_result = service.events().list(
        calendarId='primary', timeMin=now,
        timeMax=week_later, singleEvents=True,
        orderBy='startTime').execute()
    events = events_result.get('items', [])

    calendar_summary = []
    for event in events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        calendar_summary.append(f"{event['summary']} from {start} to {end}")

    # -----------------------
    # DETERMINE NEXT SUNDAY
    # -----------------------
    today = datetime.date.today()
    days_until_sunday = (6 - today.weekday()) % 7
    if days_until_sunday == 0:
        days_until_sunday = 7
    next_sunday = today + datetime.timedelta(days=days_until_sunday)
    next_sunday_str = next_sunday.strftime("%Y-%m-%d")

    # -----------------------
    # DEFINE OUTPUT SCHEMA
    # -----------------------
    response_schemas = [
        ResponseSchema(
            name="events",
            description="List of events, each with summary, start, and end times.",
        )
    ]
    output_parser = StructuredOutputParser.from_response_schemas(
        response_schemas)
    format_instructions = output_parser.get_format_instructions()

    # -----------------------
    # CREATE PROMPT
    # -----------------------
    prompt = ChatPromptTemplate.from_template(
        """You are an AI scheduling assistant.
Today's date is {today}. The start of the next week is {start_date}.
Here are my weekly goals: {goals}.
Here are my existing calendar events: {existing_events}.

Using {start_date} as the start, create an optimized weekly plan for the next 7 days.
Each event should include:
- summary
- start (ISO 8601 datetime)
- end (ISO 8601 datetime)

{format_instructions}
"""
    )

    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENAI_API_KEY,
        model="mistralai/mistral-7b-instruct", temperature=0)

    # -----------------------
    # RUN PROMPT
    # -----------------------
    input_data = {
        "today": str(today),
        "start_date": next_sunday_str,
        "goals": weekly_goals,
        "existing_events": calendar_summary,
        "format_instructions": format_instructions,
    }

    _input = prompt.format_messages(**input_data)
    response = llm.invoke(_input)

    parsed_output = output_parser.parse(response.content)

    # -----------------------
    # DISPLAY + ADD TO CALENDAR
    # -----------------------
    st.subheader("✨ Your AI-Generated Weekly Plan")
    try:
        for event in parsed_output["events"]:
            summary = event["summary"]
            start_time = event["start"]
            end_time = event["end"]

            st.write(f"- **{summary}** | {start_time} → {end_time}")

            new_event = {
                'summary': summary,
                'start': {'dateTime': start_time, 'timeZone': 'Europe/Dublin'},
                'end': {'dateTime': end_time, 'timeZone': 'Europe/Dublin'},
            }
            service.events().insert(calendarId='lormenyo.dev@gmail.com', body=new_event).execute()
        
        st.success("✅ All events have been added to your Google Calendar!")
    except Exception as e:
        st.error(f"❌ Error adding events to calendar: {str(e)}")
