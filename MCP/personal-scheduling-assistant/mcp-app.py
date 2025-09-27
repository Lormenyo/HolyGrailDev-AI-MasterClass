import streamlit as st
import datetime
import json
import requests
from langchain.output_parsers import StructuredOutputParser, ResponseSchema
from langchain.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

# MCP Server URL (your FastAPI app)
MCP_SERVER_URL = "http://localhost:8000"  # Make sure your mcp_server.py is running here

# -----------------------
# STREAMLIT UI
# -----------------------
st.title("📅 AI Google Calendar Assistant (MCP Powered)")
st.write("Balance your work, health, fun, rest, and learning goals — all added via MCP Server!")

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
    # GET EXISTING EVENTS VIA MCP
    # -----------------------
    st.write("📡 Fetching existing events via MCP...")
    try:
        resp = requests.get(f"{MCP_SERVER_URL}/list_events")
        existing_events = resp.json().get("events", [])
    except Exception as e:
        st.error(f"Failed to connect to MCP server: {e}")
        st.stop()

    # Summarize busy times
    calendar_summary = []
    for event in existing_events:
        start = event['start'].get('dateTime', event['start'].get('date'))
        end = event['end'].get('dateTime', event['end'].get('date'))
        calendar_summary.append(f"{event.get('summary', 'No Title')} from {start} to {end}")

    # -----------------------
    # DETERMINE NEXT SUNDAY
    # -----------------------
    today = datetime.date.today()
    days_until_sunday = (6 - today.weekday()) % 7 or 7
    next_sunday = today + datetime.timedelta(days=days_until_sunday)
    next_sunday_str = next_sunday.strftime("%Y-%m-%d")

    # -----------------------
    # DEFINE OUTPUT SCHEMA
    # -----------------------
    response_schemas = [
        ResponseSchema(
            name="events",
            description="List of events, each with summary, start, and end times."
        )
    ]
    output_parser = StructuredOutputParser.from_response_schemas(response_schemas)
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

    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

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
    response = llm(_input)

    parsed_output = output_parser.parse(response.content)

    # -----------------------
    # DISPLAY + ADD TO CALENDAR VIA MCP
    # -----------------------
    st.subheader("✨ Your AI-Generated Weekly Plan")
    for event in parsed_output["events"]:
        summary = event["summary"]
        start_time = event["start"]
        end_time = event["end"]

        st.write(f"- **{summary}** | {start_time} → {end_time}")

        try:
            r = requests.post(f"{MCP_SERVER_URL}/create_event", json={
                "summary": summary,
                "start": start_time,
                "end": end_time,
                "timeZone": "Europe/Dublin"
            })
            if r.status_code == 200:
                st.success(f"✅ Added: {summary}")
            else:
                st.error(f"❌ Failed to add {summary}: {r.text}")
        except Exception as e:
            st.error(f"Error adding {summary}: {e}")

    st.success("🎉 All events processed via MCP server!")
