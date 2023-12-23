import streamlit as st
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from kerykeion.report import Report
import sys
import os
import re
import google.generativeai as genai
from io import StringIO

# Function to clean text for Google GEMINI
def clean_text(text):
    cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    return cleaned_text

# Function to generate response from Google GEMINI
def generate_response(cleaned_input, model):
    try:
        response = model.generate_content(cleaned_input, stream=True)
        full_response = ""
        for chunk in response:
            full_response += chunk.text
        return full_response
    except Exception as e:
        error_message = str(e)
        st.error(f"Error: {error_message}")
        return None

# Function to get user input for astrological charts
def get_user_input():
    name = st.text_input("Person's name:")
    year = st.number_input("Year of birth:", min_value=1900, max_value=2099)
    month = st.number_input("Month of birth (1-12):", min_value=1, max_value=12)
    day = st.number_input("Day of birth (1-31):", min_value=1, max_value=31)
    hour = st.number_input("Hour of birth (0-23):", min_value=0, max_value=23)
    minute = st.number_input("Minute of birth (0-59):", min_value=0, max_value=59)
    location = st.text_input("Place of birth:")
    zodiac_type = st.selectbox("Zodiac type", ["Tropic", "Sidereal"]).capitalize()
    return name, year, month, day, hour, minute, location, zodiac_type

def main():
    st.title("Astrological Chart and WiseOracle Integration")

    # Astrological chart generation
    st.write("Enter information for the first person:")
    name1, year1, month1, day1, hour1, minute1, location1, zodiac_type1 = get_user_input()
    
    chart_type = st.selectbox("Chart type", ["Natal", "Synastry", "Transit"]).capitalize()
    if chart_type in ["Synastry", "Transit"]:
        st.write("Enter information for the second person:")
        name2, year2, month2, day2, hour2, minute2, location2, zodiac_type2 = get_user_input()
        person1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, location1, zodiac_type=zodiac_type1)
        person2 = AstrologicalSubject(name2, year2, month2, day2, hour2, minute2, location2, zodiac_type=zodiac_type2)
        chart = KerykeionChartSVG(person1, chart_type=chart_type, second_obj=person2)
    else:
        person1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, location1, zodiac_type=zodiac_type1)
        chart = KerykeionChartSVG(person1, chart_type=chart_type)

    chart.makeSVG()

    # Generate and capture the astrological report
    old_stdout = sys.stdout
    sys.stdout = mystdout = StringIO()
    user_report = Report(person1)
    user_report.print_report()
    sys.stdout = old_stdout
    report_content = mystdout.getvalue()

    # Google GEMINI integration
    genai.configure(api_key='your_google_api_key')  # Replace with your Gemini API key
    model = genai.GenerativeModel('gemini-pro')

    st.write("Ask the WiseOracle using your astrological chart information as context")
    user_query = st.text_input("Your question:")
    if st.button("Get Astrological Insight"):
        cleaned_input = clean_text(report_content + " " + user_query)
        response = generate_response(cleaned_input, model)
        if response:
            st.success(response)

    # Display the astrological chart
    st.markdown("## Generated Astrological Chart")
    script_dir = os.path.dirname(os.path.abspath(__file__))
    svg_files = [f for f in os.listdir(script_dir) if f.endswith(".svg")]
    if svg_files:
        svg_file = svg_files[0]
        st.image(os.path.join(script_dir, svg_file), use_container_width=True)
    else:
        st.write("No SVG files found in the current directory.")

if __name__ == "__main__":
    main()
