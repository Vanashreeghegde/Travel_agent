#core ai agent logic
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from typing import TypedDict, Optional
import config

#hit any api
try:
    from tavily import TavilyClient
    tavily_client = TavilyClient(api_key=config.Tavily_api) if config.Tavily_api else None
except ImportError:
    print("Tavily not installed please install tavily!")
    tavily_client = None
except Exception as e:
    print(f"Error importing Tavily: {e}")
    tavily_client = None
    
class TravelState(TypedDict):
    destination : Optional[str]
    dates : Optional[str]
    duration : Optional[int]
    budget : Optional[float]
    nationality : Optional[str]
    interests : Optional[str]
    current_question: int
    search_results : dict
    itinerary : Optional[str]
    
class TravelAgent:
    def __init__(self):
        self.llm = ChatGroq(model="llama-3.1-8b-instant",
                            groq_api_key=config.groq_Api,
                            max_tokens=6000,
                            temperature=0.8)
    
    def search_info(self, state:TravelState):
        results = {}
        destination = state['destination']
        dates = state['dates']
        nationality = state['nationality']
        
        if tavily_client:
            try:
                #visa info
                visa_query = f"Visa requirements for {nationality} to {destination} in detail"
                results['visa'] = tavily_client.search(query=visa_query, 
                                                       search_depth="advanced", 
                                                       max_results=3)
                
                #weather info
                month = dates.split()[0] if dates else "March"
                weather_query = f"Weather and climate in {destination} during {month}"
                results['weather'] = tavily_client.search(query=weather_query,
                                                          search_depth="advanced",
                                                          max_results=3)
                #Restaurants
                restaurants_query = f"Best restaurants in {destination}"
                results['restaurants'] = tavily_client.search(query=restaurants_query,
                                                              search_depth="advanced",
                                                              max_results=3)
            except Exception as e:
                print(f"Error during search: {e}")
        state['search_results'] = results
        return state
    
    def generate_itinerary(self, state:TravelState):
        search_context = ""
        for category, data in state['search_results'].items():
            if data and 'results' in data:
                search_context += f"\n{category.capitalize()}:\n"
                for result in data['results'][:2]:
                    search_context += f"- {result.get('content', 'No content')}\n"
        prompt = f"""Create a travel itinerary for :
Destination : {state['destination']}
Dates : {state['dates']}
Duration : {state['duration']} days
Budget : {state['budget']}
Nationality : {state['nationality']}
Interests : {state['interests']}

Search Results Context:
{search_context}

Please create a detailed day-by-day itinerary including:
- Visa Requirements in detail and depth
- Budget Breakdown
- Day-by-day plan (morning/afternoon/evening)
- Restaurant recommendations and local cuisine (Vegetarian only strictly!)
- Useful links (travel apps names etc)

Format the response as a structured itinerary with clear headings and bullet points.
Make it practical and budget-conscious"""
        response = self.llm.invoke([HumanMessage(content=prompt)])
        state['itinerary'] = response.content
        return state
    
    def plan_trip(self, answers:list):
        state = TravelState(
            destination=None,
            dates=None,
            duration=None,
            budget=None,
            nationality=None,
            interests=None,
            current_question=0,
            search_results={},
            itinerary=None
        )
        if len(answers) >=5:
            dest_date = answers[0].split(" in ")
            state['destination'] = dest_date[0].strip() if len(dest_date) > 0 else answers[0]
            state['dates'] = dest_date[1].strip() if len(dest_date) > 1 else "March 2026"
            
            try:
                state['duration'] = int(answers[1].split()[0])
            except (ValueError, IndexError):
                state['duration'] = 3

            try:
                state['budget'] = float(answers[2])
            except (ValueError, IndexError):
                state['budget'] = 1000.0
            state['nationality'] = answers[3]
            state['interests'] = answers[4]
        state = self.search_info(state)
        state = self.generate_itinerary(state)
        return state['itinerary']



                
        