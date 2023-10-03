from kerykeion import AstrologicalSubject, KerykeionChartSVG
from pathlib import Path
from kerykeion.report import Report  # Importa la clase Report desde kerykeion.report
import sys  # Importa el módulo sys para redirigir la salida estándar

CURRENT_DIR = Path(__file__).parent


def get_user_input():
    name = input("Nombre de la persona: ")
    year = int(input("Año de nacimiento: "))
    month = int(input("Mes de nacimiento (1-12): "))
    day = int(input("Día de nacimiento (1-31): "))
    hour = int(input("Hora de nacimiento (0-23): "))
    minute = int(input("Minuto de nacimiento (0-59): "))
    location = input("Lugar de nacimiento: ")
    zodiac_type = input("Tipo de zodiaco (Tropic o Sidereal): ").capitalize()

    return name, year, month, day, hour, minute, location, zodiac_type


def main():
    print("Ingrese la información para la primera persona:")
    name1, year1, month1, day1, hour1, minute1, location1, zodiac_type1 = get_user_input()
    
    chart_type = input("Tipo de gráfico (Natal, Synastry o Transit): ").capitalize()

    if chart_type in ["Synastry", "Transit"]:
        print("Ingrese la información para la segunda persona:")
        name2, year2, month2, day2, hour2, minute2, location2, zodiac_type2 = get_user_input()
        person1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, location1, zodiac_type=zodiac_type1)
        person2 = AstrologicalSubject(name2, year2, month2, day2, hour2, minute2, location2, zodiac_type=zodiac_type2)
        name = KerykeionChartSVG(person1, chart_type=chart_type, second_obj=person2)
    else:
        person1 = AstrologicalSubject(name1, year1, month1, day1, hour1, minute1, location1, zodiac_type=zodiac_type1)
        name = KerykeionChartSVG(person1, chart_type=chart_type)

    name.makeSVG()
    print(len(name.aspects_list))

    # Crear una instancia de Report utilizando los datos del usuario
    user_report = Report(person1)

    # Redirigir la salida estándar a un archivo
    with open('informe.txt', 'w') as file:
        sys.stdout = file  # Redirige la salida estándar al archivo
        user_report.print_report()  # Llama al método print_report para que escriba en el archivo

    # Restaura la salida estándar
    sys.stdout = sys.__stdout__

if __name__ == "__main__":
    from kerykeion.utilities import setup_logging
    setup_logging(level="debug")

    main()
