import streamlit as st
from transformers import pipeline
import random
import requests
from datetime import datetime
import time
from streamlit_calendar import calendar
from pymongo import MongoClient

# Your Mistral AI API Key (replace with your actual key)
API_KEY = "PdbnxUn09hjhBi6DNOMo9xLxBsGdYoyE"
API_URL = "https://api.mistral.ai/v1/chat/completions"

# Initialize sentiment analysis model from HuggingFace
sentiment_pipeline = pipeline("sentiment-analysis", model="siebert/sentiment-roberta-large-english")

# Placeholder chatbot response suggestions for local fallback
encouraging_responses = [
    "It seems like you're feeling down. Remember, tough times don't last. Stay strong!",
    "I hear you're going through something. It's okay to feel sad, but I'm here for you.",
    "Life can be tough, but you're tougher. Want to talk more about it?",
    "I know things may seem hard right now, but brighter days are ahead!"
]

happy_responses = [
    "I'm so glad you're feeling good today! Keep it up!",
    "That's wonderful! Keep spreading the positive energy!",
    "It's great to hear you're happy! Stay awesome!",
    "Your positivity is inspiring! Keep sharing the good vibes!"
]

neutral_responses = [
    "Thanks for sharing! Would you like to talk more about how you're feeling?",
    "It's always good to share. Let me know if there's anything specific you'd like to discuss.",
    "I'm here to listen whenever you want to talk.",
    "Your feelings are valid. Is there anything you'd like to share further?"
]

# MongoDB connection setup
MONGO_URI = "mongodb://localhost:27017/"
client = MongoClient(MONGO_URI)
db = client.get_database('personal_diary')
mood_log_collection = db['mood_log']

# Function to call Mistral AI API for chatbot response
def get_mistral_response(user_input):
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        "messages": [{"role": "user", "content": user_input}],
        "model": "mistral-small-latest",
        "max_tokens": 150
    }

    try:
        response = requests.post(API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()['choices'][0]['message']['content']
    except requests.RequestException as e:
        st.error(f"Error communicating with Mistral API: {e}")
        return None

# Function to analyze sentiment and generate a combined response
def analyze_sentiment_and_respond(user_input):
    sentiment = sentiment_pipeline(user_input)[0]
    sentiment_label = sentiment['label']
    confidence_score = sentiment['score']

    neutral_phrases = [
        "regular day", "nothing special", "just sitting",
        "trying to think", "uneventful", "feeling okay",
        "not too happy", "just existing"
    ]

    if any(phrase in user_input.lower() for phrase in neutral_phrases):
        mood_response = random.choice(neutral_responses)
        sentiment_label = 'NEUTRAL'
    elif sentiment_label == 'NEGATIVE':
        mood_response = random.choice(encouraging_responses)
    elif sentiment_label == 'POSITIVE' and confidence_score > 0.7:
        mood_response = random.choice(happy_responses)
    else:
        mood_response = random.choice(neutral_responses)

    return mood_response, {'label': sentiment_label, 'score': confidence_score}

# Function to log mood entry to MongoDB
def log_mood_entry(entry, sentiment, score, date, chatbot_response):
    mood_log_collection.insert_one({
        'entry': entry,
        'sentiment': sentiment,
        'score': score,
        'date': date,
        'chatbot_response': chatbot_response
    })

# Function to retrieve mood log entries from MongoDB
def get_mood_log():
    return list(mood_log_collection.find())

# Function to display the calendar with highlighted journal entry days
def display_calendar():
    events = []

    # Prepare events for the calendar based on mood log entries
    for log in get_mood_log():
        event_date = datetime.strptime(log['date'], '%Y-%m-%d %H:%M:%S')
        events.append({
            'title': log['entry'],  # Use entry as event title
            'start': event_date.strftime('%Y-%m-%d'),  # Format date for calendar
            'allDay': True,
            'backgroundColor': '#FF6C6C',  # Color for highlighted days (can customize)
            'borderColor': '#FF6C6C'  # Border color for events
        })

    calendar_options = {
        'editable': False,
        'selectable': True,
        'headerToolbar': {
            'left': 'today prev,next',
            'center': 'title',
            'right': 'dayGridMonth,timeGridWeek,timeGridDay'
        }
    }

    # Display the calendar with highlighted entries
    try:
        calendar(events=events, options=calendar_options)  # Display the calendar
    except Exception as e:
        st.error(f"Error displaying calendar: {e}")

# Inject custom CSS
with open("styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Password page
if 'authenticated' not in st.session_state:
    st.title("Welcome to My Virtual Personal Diary")  # Name of the diary

    password = st.text_input("Enter Password:", type="password")

    if st.button("Submit"):
        if password == "1234":
            st.session_state.authenticated = True
            st.success("Access Granted! Navigating to the chatbot...")
        else:
            st.error("Incorrect Password. Please try again.")
else:
    # Streamlit UI setup for chatbot after successful authentication
    st.title("Personal Diary Chatbot with Sentiment Analysis")

    st.write("Welcome! This is your virtual personal diary. Feel free to share how you're feeling today, and the chatbot will respond based on your emotions.")

    user_input = st.text_input("How are you feeling today?")

    if st.button("Submit Entry"):  # Use a button for submission
        if user_input:  # Only process if there's input

            # Analyze sentiment and get responses
            mood_response, sentiment_result = analyze_sentiment_and_respond(user_input)
            chatbot_response = get_mistral_response(user_input)

            # Use mood response if chatbot response is None (due to an error)
            if chatbot_response is None:
                chatbot_response = mood_response

            # Display responses temporarily before logging them
            response_placeholder = st.empty()  # Create a placeholder

            response_placeholder.write(f"Sentiment Analysis: {sentiment_result['label']} (Confidence: {sentiment_result['score']:.2f})")
            time.sleep(2)  # Delay before showing the chatbot suggestion

            response_placeholder.write(f"Chatbot: {chatbot_response}")

            time.sleep(5)  # Delay before logging the entry

            # Log the user's sentiment and chatbot's suggestion if they enter something
            current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # Get current date and time

            # Check if this entry already exists before adding it again
            existing_entries = [log['entry'] for log in get_mood_log()]

            if user_input not in existing_entries:
                log_mood_entry(user_input, sentiment_result['label'], sentiment_result['score'], current_time, chatbot_response)

                response_placeholder.success("Entry logged successfully!")  # Indicate success

                # Clear input after submission (optional)
                user_input = ""

            else:
                st.warning("This entry has already been logged.")

            time.sleep(1)  # Optional delay before clearing the placeholder

            response_placeholder.empty()  # Clear the placeholder after logging

    # Display the user's mood log history
    st.write("### Your Mood Log:")

    for log in get_mood_log():
        st.write(f"Date: {log['date']}")
        st.write(f"Entry: {log['entry']}")
        st.write(f"Sentiment: {log['sentiment']} (Confidence: {log['score']:.2f})")
        st.write(f"Chatbot Suggestion: {log['chatbot_response']}")  # Display chatbot suggestion
        st.write("---")

    # Initialize calendar visibility in session state if not already done
    if 'calendar_visible' not in st.session_state:
        st.session_state.calendar_visible = False

    # Toggle button to show/hide the calendar
    if st.button("Show Calendar"):
        st.session_state.calendar_visible = not st.session_state.calendar_visible

    # Show the calendar if it's set to visible
    if st.session_state.calendar_visible:
        display_calendar()  # Call the function to display the calendar