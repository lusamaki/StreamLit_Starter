import streamlit as st
import phonenumbers
from phonenumbers import geocoder

# Sidebar
st.sidebar.title("Navigation")
st.sidebar.write("Phone Number Country Detector")

# Title
st.title("📱 Phone Number Country Detector")

# Input
number = st.text_input("Enter phone number with country code (e.g., +254...)")

# Button
if st.button("Detect Country"):
    try:
        parsed_number = phonenumbers.parse(number)
        country = geocoder.description_for_number(parsed_number, "en")
        
        if country:
            st.success(f"🌍 This number is from: {country}")
            st.balloons()
        else:
            st.warning("Country not found. Check the number format.")
    
    except:
        st.error("❌ Invalid phone number. Make sure it includes country code (e.g., +254...)")