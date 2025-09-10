from python_a2a import A2AServer, Message, TextContent, MessageRole, run_server, AgentCard, AgentSkill, Task


class FlightAgent(A2AServer):
    def __init__(self):
        print("Initializing FlightAgent")
        super().__init__()
        
        self.agent_card = AgentCard(
            name="Flight Search Agent",
            description="I help you find the best flight options for your journey",
            skills=[ AgentSkill(name="flight_search", description="Search for flights")],
            capabilities={
                "streaming": True,
                "pushNotifications": False,
                "stateTransitionHistory": False,
                "google_a2a_compatible": True,
                "parts_array_format": True
            },
            url="http://localhost:8001",  # Optional: URL to the agent's web interface
        )

        self.tasks = [Task(id="task-001", message="flight_search_test")]


    
    def handle_task(self, task) -> Task:
        print(f"Handling task: {task} with parameters:")
        if task.message == "flight_search":
            # origin = parameters.get("origin")
            # destination = parameters.get("destination")
            # date = parameters.get("date")
            origin, destination, date = "Dublin", "Paris", "2025-09-15"
            return Task(
                id="task-001",
                message={
                    "origin": origin,
                    "destination": destination,
                    "date": date
                }
            )
            # return f"Searching for flights from {origin} to {destination} on {date}..."
        
        return Task(id="task-unknown", message="Unknown task")

    def handle_message(self, message: Message) -> Message:
        print(f"Received message: {message.content.text}")
        try:
            origin, dest, date = message.content.text.split(",")
            reply = f"Flights from {origin} to {dest} on {date}: €120 (AirExample), €135 (FlyNow)"
        except:
            reply = "Invalid input. Use: origin,destination,date"
        return Message(
            content=TextContent(text=reply),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )


if __name__ == "__main__":
    agent = FlightAgent()
    print(f"Starting agent with card: {agent.agent_card}")
    run_server(agent, host="0.0.0.0", port=8001)
