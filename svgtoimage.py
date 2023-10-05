import os
import cairosvg

def convertir_svg_a_imagen(svg_file, formato_destino):
    formato_ext = formato_destino
    if formato_destino == 'jpg':
        formato_ext = 'jpeg'

    output_file = os.path.splitext(svg_file)[0] + '.' + formato_ext

    try:
        if formato_destino == 'png':
            cairosvg.svg2png(url=svg_file, write_to=output_file)
        elif formato_destino == 'jpg':
            cairosvg.svg2jpeg(url=svg_file, write_to=output_file)
        elif formato_destino == 'pdf':
            cairosvg.svg2pdf(url=svg_file, write_to=output_file)
        else:
            print("Formato de destino no válido. No se realizó la conversión.")
            return

        print(f"El archivo se ha convertido exitosamente a {formato_destino}.")
    except Exception as e:
        print(f"Error al convertir el archivo: {str(e)}")

if __name__ == "__main__":
    ruta_archivo_svg = input("Ingrese la ruta del archivo SVG: ")

    if not os.path.exists(ruta_archivo_svg):
        print("El archivo SVG no existe en la ruta proporcionada.")
    else:
        opciones_formato = ['png', 'jpg', 'pdf']
        print("Formatos de destino disponibles: png, jpg, pdf")
        formato_destino = input("Elija un formato de destino: ").lower()

        if formato_destino not in opciones_formato:
            print("Formato de destino no válido.")
        else:
            convertir_svg_a_imagen(ruta_archivo_svg, formato_destino)
