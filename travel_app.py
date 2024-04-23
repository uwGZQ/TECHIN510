# import os

# import requests
# from dotenv import load_dotenv

# load_dotenv()

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
    # api_url = 'https://api.gemini.com/v1/generate/text'
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-pro')


    # headers = {'Authorization': f'Bearer {api_key}'}
    
    # Formatting the prompt
    prompt = f"Generate a travel itinerary for a {destination.lower()} destination with a budget of ${budget}, " \
             f"from {dates[0]} to {dates[-1]}, including activities like {', '.join(activities)}."
    
    # # API payload
    # payload = {
    #     'prompt': prompt,
    #     'max_tokens': 150
    # }

    # Making the API call
    response = model.generate_content(prompt)
    # response = requests.post(api_url, headers=headers, json=payload)
    # if response.status_code == 200:
    #     # Assuming the API returns text directly
    #     return response.json()['choices'][0]['text']
    # else:
    #     # Error handling if the API call fails
    #     st.error(f"API call failed with status code {response.status_code}: {response.text}")
    #     return None
    return response
    
if __name__ == "__main__":
    main()
