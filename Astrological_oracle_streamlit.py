import streamlit as st
from kerykeion import AstrologicalSubject, KerykeionChartSVG
from kerykeion.report import Report
from pathlib import Path
import sys
from PIL import Image

def get_user_input():
    name = st.text_input("Nombre de la persona:")
    year = st.number_input("Año de nacimiento:", min_value=1900, max_value=2099)
    month = st.number_input("Mes de nacimiento (1-12):", min_value=1, max_value=12)
    day = st.number_input("Día de nacimiento (1-31):", min_value=1, max_value=31)
    hour = st.number_input("Hora de nacimiento (0-23):", min_value=0, max_value=23)
    minute = st.number_input("Minuto de nacimiento (0-59):", min_value=0, max_value=59)
    location = st.text_input("Lugar de nacimiento:")
    zodiac_type = st.selectbox("Tipo de zodiaco", ["Tropic", "Sidereal"]).capitalize()

    return name, year, month, day, hour, minute, location, zodiac_type

def main():
    st.title("Generador de Cartas Astrales")
    
    st.write("Ingrese la información para la primera persona:")
    name1, year1, month1, day1, hour1, minute1, location1, zodiac_type1 = get_user_input()
    
    chart_type = st.selectbox("Tipo de gráfico", ["Natal", "Synastry", "Transit"]).capitalize()

    if chart_type in ["Synastry", "Transit"]:
        st.write("Ingrese la información para la segunda persona:")
        name2, year2, month2, day2, hour2, minute2, location2, zodiac_type2 = get_user_input()
        person1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, location1, zodiac_type=zodiac_type1)
        person2 = AstrologicalSubject(name2, year2, month2, day2, hour2, minute2, location2, zodiac_type=zodiac_type2)
        name = KerykeionChartSVG(person1, chart_type=chart_type, second_obj=person2)
    else:
        person1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, location1, zodiac_type=zodiac_type1)
        name = KerykeionChartSVG(person1, chart_type=chart_type)

    name.makeSVG()

    # Create a user report
    user_report = Report(person1)
    
    st.write(f"Número de aspectos encontrados: {len(name.aspects_list)}")

    # Download the report as a text file
    st.markdown("## Descargar Informe")
    st.write("Haga clic en el botón de abajo para descargar el informe en un archivo de texto.")

    if st.button("Descargar Informe"):
        with open('informe.txt', 'w') as file:
            sys.stdout = file
            user_report.print_report()
        sys.stdout = sys.__stdout__
        st.success("Informe descargado con éxito como 'informe.txt'")

    # Display the content of 'informe.txt'
    with open('informe.txt', 'r') as file:
        report_content = file.read()
        st.markdown("## Contenido del Informe")
        st.text(report_content)

    # Display the generated SVG image
    st.markdown("## Gráfico Astral Generado")
    st.image('chart.svg')

if __name__ == "__main__":
    main()
