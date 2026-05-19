# Función realizada por Lizeth Sastoque

"""
En este módulo manejamos el historial de ecuaciones balanceadas.
Aquí guardamos las operaciones realizadas por el usuario, mostramos
el historial almacenado y también permitimos exportarlo a un archivo
de texto para conservar los resultados.
"""

from datetime import datetime

# Creamos el nombre del archivo donde se guardará el historial
ARCHIVO_HISTORIAL = "historial.txt"


# Esta función guarda cada ecuación procesada por el usuario
def guardar_en_historial(ecuacion, balanceada, tipo):

    # Abrimos el archivo en modo append para agregar información
    # sin borrar lo que ya estaba guardado anteriormente
    with open(ARCHIVO_HISTORIAL, "a") as archivo:

        # Guardamos la ecuación original ingresada
        archivo.write("Ecuación: " + ecuacion + "\n")

        # Guardamos la ecuación ya balanceada
        archivo.write("Balanceada: " + balanceada + "\n")

        # También guardamos el tipo de reacción encontrado
        archivo.write("Tipo: " + tipo + "\n")

        # Guardamos la fecha y hora en la que se realizó la operación
        archivo.write(
            "Fecha: " +
            datetime.now().strftime("%Y-%m-%d %H:%M:%S") +
            "\n"
        )

        # Agregamos una línea divisoria para organizar mejor el historial
        archivo.write("-" * 40 + "\n")


# Esta función se encarga de leer y mostrar el historial completo
def mostrar_historial():

    try:

        # Abrimos el archivo en modo lectura
        with open(ARCHIVO_HISTORIAL, "r") as archivo:

            contenido = archivo.read()

            # Si el archivo está vacío mostramos un mensaje
            if contenido.strip() == "":
                print("\nNo hay historial todavía 🫠")

            # Si sí hay contenido, mostramos todo organizado
            else:
                print("\n===== HISTORIAL =====")
                print(contenido)

    except FileNotFoundError:

        # Si el archivo todavía no existe evitamos que el programa falle
        print("\nNo hay historial todavía 🫠")


# Esta función crea una copia del historial en otro archivo de texto
def exportar_txt():

    try:

        # Leemos todo el contenido del historial original
        with open(ARCHIVO_HISTORIAL, "r") as origen:
            contenido = origen.read()

        # Creamos un nuevo archivo donde se copiará el historial
        with open("resultados.txt", "w") as destino:
            destino.write(contenido)

        # Mostramos un mensaje indicando que la exportación salió bien
        print("Historial exportado correctamente 📄")

    except FileNotFoundError:

        # Si no existe historial mostramos un mensaje al usuario
        print("No hay datos para exportar 😅")
