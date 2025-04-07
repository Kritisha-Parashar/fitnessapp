import streamlit as st
import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the API key from environment
api_key = os.getenv("OPENAI_API_KEY")

# Check and raise error if not found
if not api_key:
    st.error("❌ OpenAI API key not found. Please check your .env file.")
    st.stop()

# Create the OpenAI client
client = OpenAI(api_key=api_key)


st.set_page_config(page_title="AI Fitness Coach", layout="centered")
st.title("🏋️ AI Fitness Coach")

st.markdown("Fill in your details and get a personalized workout & diet plan powered by GPT-4!")

with st.form("user_profile"):
    name = st.text_input("Your Name")
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    height = st.number_input("Height (in cm)", min_value=100, max_value=250)
    weight = st.number_input("Weight (in kg)", min_value=30, max_value=250)
    goal = st.selectbox("Fitness Goal", ["Weight Loss", "Muscle Gain", "Maintenance"])
    submitted = st.form_submit_button("Generate My Plan")

from openai import OpenAI

client = OpenAI()  # automatically uses your OPENAI_API_KEY from env

def generate_fitness_plan(name, gender, height, weight, goal):
    prompt = f"""
    You are a professional fitness and nutrition expert.

    Create a detailed fitness and diet plan for the following user:
    Name: {name}
    Gender: {gender}
    Height: {height} cm
    Weight: {weight} kg
    Goal: {goal}

    Include:
    - A summary of fitness level based on BMI
    - Daily meal plan (with meals and times)
    - Weekly workout routine (with rest days)
    - Tips to stay consistent

    Make it personalized and friendly.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # Or "gpt-3.5-turbo"
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=1000
    )

    return response.choices[0].message.content


if submitted:
    if name:
        with st.spinner("Generating your custom plan..."):
            plan = generate_fitness_plan(name, gender, height, weight, goal)
        st.success(f"Here's your personalized plan, {name}!")
        st.markdown(plan)
    else:
        st.error("Please enter your name.")
