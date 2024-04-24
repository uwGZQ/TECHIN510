# TECHIN 510 Lab 5 (With Bonus)

## Travel Planner App

The Travel Planner is a web application built using Streamlit and the Gemini API that generates personalized travel itineraries based on user preferences. Users can specify their destination, budget, travel dates, and interests to receive a custom itinerary that includes daily activities, estimated expenses, and accommodations.

### Features:
1. Custom Travel Itineraries: Generates travel plans tailored to user-specified parameters.
2. User-Friendly Interface: Simple and intuitive interface using Streamlit.
3. Dynamic Content Generation: Leverages the Gemini API for content generation.


### Setup and Installation:
1. Set up a Python virtual environment (optional but recommended):
```bash
python -m venv env
source env/bin/activate
```

2. Install the required packages:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the root directory.
Add `API_KEY=YourGeminiApiKeyHere` to the `.env` file.

### How to Run:
Execute the following command in the project directory to start the Streamlit application:

```bash
streamlit run travel_app.py
```

Fill out the form with your travel preferences and click "Create Itinerary".

View the generated itinerary directly on the web interface.
