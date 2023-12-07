import streamlit as st
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from kerykeion.report import Report
import sys
import os

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
    st.title("Astrological Chart Generator")
    st.markdown(
    """
    
    **Author:** cha0smagick the Techno Wizard  
    **Created for the blog:** [El Rincon Paranormal](https://elrinconparanormal.blogspot.com)  
    **Project's main page:** [Technowizard Cha0smagick's Astrological charts](hhttps://elrinconparanormal.blogspot.com/2023/12/Free%20Astrological%20Chart%20Generator%20Tool%20Online.html)  
    
    **Donate crypto to support the project:**
    
    - Bitcoin: 3KcF1yrY44smTJpVW68m8dw8q64kPtzvtX
    - Litecoin: LME9oq8BRQ6dDdqEKg3HJB9UL6byhJka1X
    - Gridcoin: RyAcDpYRMWfDHLTizCTLzy58qBgzcfo5eZ
    - Dodgecoin: DDSxowLFPyBHVdV16hGhWdhyfa8ors3VPd
    - Blackcoin: B62pVSG1hjvBDbCeKbEnYmKxUg5rsnZKwt
    - Dash: Xj1MjAgxZPRqysMHox4sUV9XYZixrsk4e6
    - Peercoin: PA43iLNooKU76u4yPTtL5j97W6zwWkwxV2
    - Syscoin: sys1qg6npncq4xe7ruz4e4xlnvuyrzj90qvv3gg0yag
    
    """
)
    
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

    # Create a user report
    user_report = Report(person1)
    
    st.write(f"Number of aspects found: {len(chart.aspects_list)}")

    # Download the report as a text file
    st.markdown("## Download Report")
    st.write("Click the button below to download the report as a text file.")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    report_file_path = os.path.join(script_dir, "report.txt")

    if st.button("Download Report"):
        # Create a user report
        user_report = Report(person1)
        
        with open(report_file_path, 'w') as file:
            sys.stdout = file
            user_report.print_report()
        sys.stdout = sys.__stdout__
        st.success(f"Report successfully downloaded as 'report.txt'")

    # Display the content of 'report.txt'
    if os.path.exists(report_file_path):
        with open(report_file_path, 'r') as file:
            report_content = file.read()
            st.markdown("## Report Content")
            st.text(report_content)
    else:
        st.warning("Report file not found. Please generate the report first.")

    # Search and display an SVG image in the current directory
    st.markdown("## Generated Astrological Chart")
    svg_files = [f for f in os.listdir(script_dir) if f.endswith(".svg")]

    if svg_files:
        svg_file = svg_files[0]  # Display the first SVG file found
        st.image(os.path.join(script_dir, svg_file), use_container_width=True)
    else:
        st.write("No SVG files found in the current directory.")

if __name__ == "__main__":
    main()
