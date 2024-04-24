import streamlit as st
import requests
from datetime import date
from dotenv import load_dotenv
import os

# Load the environment variables from the .env file
load_dotenv()

def main():
    # Get the API key from environment variables
    api_key = os.getenv('API_KEY')
    
    # Set up the main structure of the Streamlit app
    st.set_page_config(page_title="Travel Planner", page_icon="✈️", layout='wide')
    
    # Title and introduction
    st.title('Travel Planner')
    st.write("Welcome to the Travel Planner! Fill out your preferences and we'll suggest a custom travel itinerary for you.")
    
    # Input form for user preferences
    with st.form("travel_preferences", clear_on_submit=False):
        destination_type = st.selectbox("What type of destination are you interested in?",
                                        ("Beach", "Mountains", "City", "Countryside"))
        budget = st.slider("What's your budget for this trip?", 100, 10000, 1000, step=100)
        travel_dates = st.date_input("Select your travel dates", value=(date.today(), date.today()))
        activity_preferences = st.multiselect("What kind of activities are you interested in?",
                                              ["Cultural", "Adventure", "Relaxation", "Sport", "Gastronomy"])
        submit_button = st.form_submit_button("Generate Itinerary")
        
    if submit_button:
        itinerary = generate_itinerary_via_gemini_api(destination_type, budget, travel_dates, activity_preferences, api_key)
        if itinerary:
            st.success("Your custom travel itinerary is ready!")
            st.write(itinerary)
        else:
            st.error("Failed to generate itinerary. Please try again later.")

def generate_itinerary_via_gemini_api(destination, budget, dates, activities, api_key):
    # API URL setup
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')

    # Formatting the prompt
    prompt = f"Generate a travel itinerary for a {destination.lower()} destination with a budget of ${budget}, " \
             f"from {dates[0]} to {dates[-1]}, including activities like {', '.join(activities)}."


    response = model.generate_content(prompt)
    
    return response.text
    
if __name__ == "__main__":
    main()
