from python_a2a import A2AServer, AgentCard, AgentSkill, Message, TextContent, MessageRole, run_server

class HotelAgent(A2AServer):
    def __init__(self):
        super().__init__()

        self.agent_card = AgentCard(
            name="Hotel Search Agent",
            description="I help you find the best Hotel options for your journey",
            skills=[ AgentSkill(name="hotel_search", description="Search for Hotels")],
            capabilities={
                "streaming": True,
                "pushNotifications": False,
                "stateTransitionHistory": False,
                "google_a2a_compatible": True,
                "parts_array_format": True
            },
            url="http://localhost:8002", 
        )


    def handle_message(self, message: Message) -> Message:
        try:
            # Input: "Paris,2025-09-15,3" (destination, date, nights)
            city, date, nights = message.content.text.split(",")
            # Mocked hotel search
            reply = f"Hotels in {city} from {date} for {nights} nights: €90/night (HotelExample), €110/night (StayInn)"
        except:
            reply = "Invalid input. Use: destination,date,nights"
        return Message(
            content=TextContent(text=reply),
            role=MessageRole.AGENT,
            parent_message_id=message.message_id,
            conversation_id=message.conversation_id
        )

if __name__ == "__main__":
    run_server(HotelAgent(), host="0.0.0.0", port=8002)
