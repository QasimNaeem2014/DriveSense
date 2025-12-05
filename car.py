import streamlit as st
import os
from google import genai
from google.genai import types
import time
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="🚗 Drive Sense",
    page_icon="🚗",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Enhanced Custom CSS with black-purple theme
st.markdown("""
<style>
    /* Main background */
    .main {
        background: linear-gradient(135deg, #0a0015 0%, #1a0033 50%, #2d1b4e 100%);
    }
    .stApp {
        background: linear-gradient(135deg, #0a0015 0%, #1a0033 50%, #2d1b4e 100%);
    }

    /* Animated Car Header */
    .car-header {
        position: relative;
        width: 100%;
        height: 150px;
        background: linear-gradient(180deg, #1a0033 0%, transparent 100%);
        overflow: hidden;
        margin-bottom: 2rem;
        border-bottom: 2px solid rgba(139, 92, 246, 0.3);
    }

    .car-animation {
        position: absolute;
        top: 50%;
        transform: translateY(-50%);
        animation: drive 8s linear infinite;
        font-size: 5rem;
        filter: drop-shadow(0 0 20px rgba(124, 58, 237, 0.8));
    }

    @keyframes drive {
        0% { left: -10%; }
        100% { left: 110%; }
    }

    .app-title {
        position: absolute;
        top: 50%;
        left: 50%;
        transform: translate(-50%, -50%);
        font-size: 3rem;
        font-weight: bold;
        color: #c4b5fd;
        text-shadow: 0 0 30px rgba(167, 139, 250, 0.8);
        z-index: 10;
        font-family: 'Arial Black', sans-serif;
        letter-spacing: 3px;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        display: none;
    }

    /* Navigation styling */
    .nav-container {
        display: flex;
        justify-content: center;
        gap: 1rem;
        margin: 1rem 0 2rem 0;
        flex-wrap: wrap;
    }

    .nav-button {
        background: linear-gradient(135deg, #6b21a8 0%, #7c3aed 100%);
        color: white;
        padding: 0.75rem 2rem;
        border-radius: 2rem;
        font-weight: bold;
        text-decoration: none;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(107, 70, 193, 0.4);
        border: 2px solid transparent;
    }

    .nav-button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6);
        border-color: #a78bfa;
    }

    .nav-button.active {
        background: linear-gradient(135deg, #8b5cf6 0%, #a78bfa 100%);
        border-color: #c4b5fd;
    }

    /* Chat messages */
    .chat-message {
        padding: 1.5rem;
        border-radius: 1rem;
        margin-bottom: 1rem;
        display: flex;
        flex-direction: column;
        animation: fadeIn 0.5s;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }
    .user-message {
        background: linear-gradient(135deg, #4c1d95 0%, #6b21a8 100%);
        color: white;
        margin-left: 20%;
        box-shadow: 0 4px 15px rgba(107, 70, 193, 0.4);
    }
    .bot-message {
        background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%);
        color: white;
        margin-right: 20%;
        box-shadow: 0 4px 15px rgba(49, 46, 129, 0.4);
    }

    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
    }

    /* Card styling */
    .car-card {
        background: linear-gradient(135deg, #1e1b4b 0%, #2d1b69 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        box-shadow: 0 8px 20px rgba(0, 0, 0, 0.5);
        margin: 1rem 0;
        transition: transform 0.3s;
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #e9d5ff;
    }
    .car-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 25px rgba(107, 70, 193, 0.4);
        border-color: rgba(167, 139, 250, 0.6);
    }

    /* Button styling */
    .stButton>button {
        background: linear-gradient(135deg, #6b21a8 0%, #7c3aed 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 2rem;
        font-weight: bold;
        transition: all 0.3s;
        box-shadow: 0 4px 15px rgba(107, 70, 193, 0.4);
    }
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(124, 58, 237, 0.6);
        background: linear-gradient(135deg, #7c3aed 0%, #8b5cf6 100%);
    }

    /* Input fields */
    .stTextInput>div>div>input, .stSelectbox>div>div>select, .stTextArea>div>div>textarea {
        background: rgba(30, 27, 75, 0.6);
        color: #e9d5ff;
        border: 1px solid rgba(139, 92, 246, 0.4);
        border-radius: 0.5rem;
    }

    /* Headers */
    h1, h2, h3 {
        color: #c4b5fd !important;
        text-shadow: 0 2px 10px rgba(167, 139, 250, 0.3);
    }

    /* Metric cards */
    .metric-card {
        background: linear-gradient(135deg, #2d1b69 0%, #3730a3 100%);
        padding: 1rem;
        border-radius: 0.5rem;
        text-align: center;
        color: white;
        border: 1px solid rgba(139, 92, 246, 0.3);
    }

    /* Info/Warning boxes */
    .stAlert {
        background: rgba(30, 27, 75, 0.6);
        border-left: 4px solid #7c3aed;
        color: #e9d5ff;
    }

    /* Success messages */
    .stSuccess {
        background: rgba(45, 27, 105, 0.6);
        border-left: 4px solid #10b981;
        color: #d1fae5;
    }

    /* Make text more visible */
    p, label, span, div {
        color: #ddd6fe !important;
    }

    /* Radio buttons */
    .stRadio > label {
        color: #c4b5fd !important;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'gemini_client' not in st.session_state:
    st.session_state.gemini_client = None
if 'user_preferences' not in st.session_state:
    st.session_state.user_preferences = {}
if 'recommended_cars' not in st.session_state:
    st.session_state.recommended_cars = []
if 'page' not in st.session_state:
    st.session_state.page = "Find My Car"
if 'api_key_input' not in st.session_state:
    st.session_state.api_key_input = ""


# Functions
# Image fetching removed as per user request


def initialize_gemini(api_key):
    """Initialize Gemini client"""
    try:
        client = genai.Client(api_key=api_key)
        # Test the connection
        test_response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents="Hello"
        )
        return client
    except Exception as e:
        st.error(f"Error initializing Gemini: {str(e)}")
        return None


def get_gemini_response(client, prompt, image_bytes=None):
    """Get response from Gemini API"""
    try:
        # Clean the prompt - remove problematic characters
        prompt = str(prompt).encode('utf-8', 'ignore').decode('utf-8')

        if image_bytes:
            contents = [
                types.Part(inline_data=types.Blob(mime_type="image/jpeg", data=image_bytes)),
                types.Part.from_text(text=prompt),
            ]
        else:
            contents = prompt

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=contents,
        )

        # Extract text from response
        if hasattr(response, 'text'):
            return response.text
        elif hasattr(response, 'candidates') and len(response.candidates) > 0:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                text_parts = [part.text for part in candidate.content.parts if hasattr(part, 'text')]
                return ''.join(text_parts)

        return "No response received from API"

    except Exception as e:
        error_msg = str(e)
        st.error(f"API Error: {error_msg}")
        return f"Error: {error_msg}"


# Initialize Gemini client
env_api_key = os.getenv("GEMINI_API_KEY")

if env_api_key and not st.session_state.gemini_client:
    st.session_state.gemini_client = initialize_gemini(env_api_key)

# Main content
# Animated Car Header
st.markdown("""
<div class="car-header">
    <div class="app-title">DRIVE SENSE</div>
    <div class="car-animation">🚘</div>
</div>
""", unsafe_allow_html=True)

# API Key input if not already set
if not st.session_state.gemini_client:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.markdown("### 🔑 Enter Your Gemini API Key")
        api_key = st.text_input("", type="password",
                                placeholder="Paste your Gemini API key here",
                                help="Get your API key from Google AI Studio",
                                key="api_input")

        if st.button("Connect", use_container_width=True):
            if api_key:
                with st.spinner("Connecting to Gemini AI..."):
                    st.session_state.gemini_client = initialize_gemini(api_key)
                    if st.session_state.gemini_client:
                        st.success("Connected to Gemini AI! 🎉")
                        time.sleep(1)
                        st.rerun()
            else:
                st.warning("Please enter your API key")
        st.markdown("---")

# Navigation
col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    nav_col1, nav_col2 = st.columns(2)

    with nav_col1:
        if st.button("🔍 Find My Car", use_container_width=True):
            st.session_state.page = "Find My Car"
            st.rerun()

    with nav_col2:
        if st.button("⚖️ Compare Cars", use_container_width=True):
            st.session_state.page = "Compare Cars"
            st.rerun()

st.markdown("---")

page = st.session_state.page

if page == "Find My Car":
    st.title("Find Your Perfect Car")
    st.markdown("Tell us your preferences and we'll recommend the best cars for you!")
    st.info("💡 Please provide specific car model names (e.g., Toyota Corolla, Honda Civic, Suzuki Alto) for accurate recommendations.")

    if not st.session_state.gemini_client:
        st.warning("Please enter your Gemini API key in the sidebar to get started!")
    else:
        # Preference Form
        st.markdown("### Your Preferences")

        col1, col2 = st.columns(2)

        with col1:
            budget = st.selectbox("Budget Range",
                                  ["Under Rs. 20 Lakh", "Rs. 20-30 Lakh", "Rs. 30-50 Lakh",
                                   "Rs. 50-75 Lakh", "Rs. 75 Lakh - 1 Crore", "Over Rs. 1 Crore"])

            car_type = st.selectbox("Car Type",
                                    ["Sedan", "SUV", "Truck", "Coupe",
                                     "Hatchback", "Minivan", "Electric", "Hybrid"])

            usage = st.selectbox("Primary Use",
                                 ["Daily Commute", "Family Transport",
                                  "Weekend Fun", "Off-Road", "Luxury", "Business"])

        with col2:
            seating = st.selectbox("Seating Capacity",
                                   ["2 seats", "4-5 seats", "6-7 seats", "8+ seats"])

            fuel_type = st.selectbox("Fuel Preference",
                                     ["Gasoline", "Diesel", "Electric", "Hybrid", "No Preference"])

            brand_pref = st.text_input("Preferred Brands (optional)",
                                       placeholder="e.g., Toyota, Honda, Suzuki")

        additional_notes = st.text_area("Additional Requirements (optional)",
                                        placeholder="e.g., good cargo space, high safety rating, fuel efficient")

        if st.button("Find My Perfect Car", use_container_width=True):
            with st.spinner("Analyzing your preferences and finding the best cars..."):
                # Store preferences
                st.session_state.user_preferences = {
                    "budget": budget,
                    "car_type": car_type,
                    "usage": usage,
                    "seating": seating,
                    "fuel_type": fuel_type,
                    "brand_pref": brand_pref,
                    "additional": additional_notes
                }

                # Create CONCISE prompt for Gemini
                prompt = f"""Recommend 3 cars based on: Budget: {budget}, Type: {car_type}, Use: {usage}, Seating: {seating}, Fuel: {fuel_type}, Brands: {brand_pref if brand_pref else 'Any'}, Notes: {additional_notes if additional_notes else 'None'}

IMPORTANT: 
1. Only recommend REAL car models that exist in Pakistan
2. Show prices in PKR (Pakistani Rupees)
3. If the user input seems invalid or unrelated to cars, respond with "I don't know - please provide valid car preferences"

Format EXACTLY like this for each car:
**[Car Name]** - Rs. [Price in PKR]
• Key feature 1
• Key feature 2
• Why it fits (1 sentence)

Keep it SHORT and CLEAR. No long paragraphs."""

                st.info("Sending request to Gemini AI...")
                response = get_gemini_response(st.session_state.gemini_client, prompt)

                if response and not response.startswith("Error"):
                    st.markdown("---")
                    st.markdown("### Recommended Cars for You")
                    st.markdown(f'<div class="car-card">{response}</div>', unsafe_allow_html=True)
                else:
                    st.error("Failed to get recommendations. Please check your API key and try again.")

elif page == "Compare Cars":
    st.title("⚖️ Compare Cars Side-by-Side")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🚗 Car 1")
        car1 = st.text_input("Enter first car:", key="car1",
                             placeholder="E.g., Toyota Corolla 2024")

    with col2:
        st.markdown("### 🚗 Car 2")
        car2 = st.text_input("Enter second car:", key="car2",
                             placeholder="E.g., Honda Civic 2024")

    if st.button("⚖️ Compare Now", use_container_width=True):
        if not st.session_state.gemini_client:
            st.error("⚠️ Please enter your Gemini API key first!")
        elif car1 and car2:
            st.markdown("---")
            st.markdown("### 📊 Detailed Comparison")

            with st.spinner("Analyzing..."):
                # Input validation
                invalid_patterns = ['1000009898', 'asdfgh', '!!!', '---']
                if any(char.isdigit() for char in car1) and len([c for c in car1 if c.isdigit()]) > 6:
                    st.error("I don't know - please provide valid car model names, not random numbers.")
                elif any(char.isdigit() for char in car2) and len([c for c in car2 if c.isdigit()]) > 6:
                    st.error("I don't know - please provide valid car model names, not random numbers.")
                else:
                    # CONCISE comparison prompt
                    prompt = f"""Compare {car1} vs {car2}. 

IMPORTANT:
1. Only compare if these are REAL car models
2. Show prices in PKR (Pakistani Rupees)
3. If the input seems invalid or unrelated to real cars, respond ONLY with "I don't know - please provide valid car model names"

If valid cars, be BRIEF and CLEAR:

**Performance:** [1-2 sentences]
**Price:** [Show in PKR format: Rs. X,XXX,XXX]
**Features:** [3-4 key differences as bullet points]
**Efficiency:** [1 sentence]
**Best For:** 
• {car1}: [who should buy]
• {car2}: [who should buy]

Keep it SHORT."""

                    comparison = get_gemini_response(st.session_state.gemini_client, prompt)
                    st.markdown(f'<div class="car-card">{comparison}</div>', unsafe_allow_html=True)
        else:
            st.warning("Please enter both car names!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #c4b5fd; padding: 1rem;'>
    <p>Developer: Muhammad Qasim Naeem ❤

Made with Love & AI</p>
    <p style='font-size: 0.8rem;'>14qasimnaeem.5239@gmail.com</p>
</div>
""", unsafe_allow_html=True)