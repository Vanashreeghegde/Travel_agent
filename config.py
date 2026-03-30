#configuration and setting
import os
from dotenv import load_dotenv

load_dotenv(".env")

groq_Api=os.getenv("groq_Api")
Tavily_api=os.getenv("Tavily_api")

QUESTIONS=[
    "Where do you want to go and when?",
    "How long is your trip (in days)?",
    "What's your total budget (excluding flights)?",
    "What's your passport nationality",
    "What are your travel interests? (select multiple or add your own!)"    
]


