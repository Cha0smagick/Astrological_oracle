import streamlit as st
from kerykeion import AstrologicalSubject, KerykeionChartSVG, SynastryAspects
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

# Function to get user input for astrological charts, with unique keys
def get_user_input(key_suffix=""):
    name = st.text_input(f"Person's name {key_suffix}:", key=f"name{key_suffix}")
    year = st.number_input(f"Year of birth {key_suffix}:", min_value=1900, max_value=2099, key=f"year{key_suffix}")
    month = st.number_input(f"Month of birth {key_suffix} (1-12):", min_value=1, max_value=12, key=f"month{key_suffix}")
    day = st.number_input(f"Day of birth {key_suffix} (1-31):", min_value=1, max_value=31, key=f"day{key_suffix}")
    hour = st.number_input(f"Hour of birth {key_suffix} (0-23):", min_value=0, max_value=23, key=f"hour{key_suffix}")
    minute = st.number_input(f"Minute of birth {key_suffix} (0-59):", min_value=0, max_value=59, key=f"minute{key_suffix}")
    location = st.text_input(f"Place of birth {key_suffix}:", key=f"location{key_suffix}")
    zodiac_type = st.selectbox(f"Zodiac type {key_suffix}", ["Tropic", "Sidereal"], key=f"zodiac_type{key_suffix}").capitalize()
    return name, year, month, day, hour, minute, location, zodiac_type

class SynastryAspectsWithRelevant(SynastryAspects):
    @property
    def relevant_aspects(self):
        relevant_aspects_list = []
        
        # Add your logic to calculate relevant aspects here
        for aspect in self.all_aspects:
            # Customize this condition based on your criteria
            if aspect["orbit"] < 10:
                relevant_aspects_list.append(aspect)
        
        return relevant_aspects_list

def main():
    st.title("Astrological Chart Oracle")

    # Astrological chart generation
    st.write("Enter information for the first person:")
    name1, year1, month1, day1, hour1, minute1, location1, zodiac_type1 = get_user_input()
    person1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, location1, zodiac_type=zodiac_type1)
    
    chart_type = st.selectbox("Chart type", ["Natal", "Synastry", "Transit"]).capitalize()

    report_content = ""
    if chart_type in ["Synastry", "Transit"]:
        st.write("Enter information for the second person:")
        name2, year2, month2, day2, hour2, minute2, location2, zodiac_type2 = get_user_input(" - Person 2")
        person2 = AstrologicalSubject(name2, year2, month2, day2, hour2, minute2, location2, zodiac_type=zodiac_type2)

        if chart_type == "Synastry":
            synastry = SynastryAspectsWithRelevant(person1, person2)
            aspect_list = synastry.relevant_aspects
            report_content = "\n".join([str(aspect) for aspect in aspect_list])
        else:  # Transit
            # Display a message for the "Transit" option
            st.write("Feature in development")
    else:
        # Generate and capture the astrological report for person1
        old_stdout = sys.stdout
        sys.stdout = mystdout = StringIO()
        user_report = Report(person1)
        user_report.print_report()
        sys.stdout = old_stdout
        report_content = mystdout.getvalue()

    # Google GEMINI integration
    genai.configure(api_key='google_api_key')  # Replace with your Gemini API key
    model = genai.GenerativeModel('gemini-pro')

    # st.write("Context Information:")
    # st.write(report_content)

    st.write("Ask the Astrological Oracle using your astrological chart information as context")
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
