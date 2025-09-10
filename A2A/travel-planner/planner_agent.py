from python_a2a import A2AClient, Message, MessageRole, TextContent
import streamlit as st

FLIGHT_AGENT_URL = "http://localhost:8001/a2a"
HOTEL_AGENT_URL = "http://localhost:8002/a2a"

def send_to_agent(base_url, message_text):
    # Create a [Python A2A](python-a2a.html) client to talk to our agent
    agent_client = A2AClient(base_url)
            
    # Send a message using [Python A2A](python-a2a.html)
    message = Message(
            content=TextContent(text=message_text),
            role=MessageRole.USER
        )
    response = agent_client.send_message(message)
    return response.content.text

st.title("🛫 AI-Powered Travel Planner (A2A Protocol)")

origin = st.text_input("Origin City", "Dublin")
destination = st.text_input("Destination City", "Paris")
date = st.date_input("Departure Date")
nights = st.number_input("Number of Nights", min_value=1, value=3)

if st.button("Plan My Trip"):
    with st.spinner("Talking to AI agents..."):
        print(f"Sending to flight agent: {origin}, {destination}, {date}")
        print(f"Sending to hotel agent: {destination}, {date}, {nights}")

        flights = send_to_agent(FLIGHT_AGENT_URL, f"{origin},{destination},{date}")
        hotels = send_to_agent(HOTEL_AGENT_URL, f"{destination},{date},{nights}")
        
        st.subheader("Your AI-Generated Travel Plan:")
        st.write(f"✈️ **Flights**: {flights}")
        st.write(f"🏨 **Hotels**: {hotels}")
