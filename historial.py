"""
Módulo: Historial con txt
Autor: Lizeth Sastoque
Descripción:
    Gestiona el registro persistente de las ecuaciones procesadas por
    el programa. Guarda cada resultado en un archivo de texto plano
    (historial.txt) con fecha y hora, y permite visualizar o exportar
    el historial.
Funciones:
    - guardar_en_historial(ecuacion, balanceada, tipo): Añade una entrada al historial.
    - mostrar_historial(): Imprime el historial completo en consola.
    - exportar_txt(): Copia el historial a un archivo 'resultados.txt'.
Dependencias:
    - datetime (librería estándar de Python)
"""


from datetime import datetime

ARCHIVO_HISTORIAL = "historial.txt"


def guardar_en_historial(ecuacion, balanceada, tipo):
    # Cada vez que el usuario haga una operación, se guarda aquí
    
    with open(ARCHIVO_HISTORIAL, "a") as archivo:
        archivo.write("Ecuación: " + ecuacion + "\n")
        archivo.write("Balanceada: " + balanceada + "\n")
        archivo.write("Tipo: " + tipo + "\n")
        archivo.write("Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")
        archivo.write("-" * 40 + "\n")  # separador para que no se mezcle todo


def mostrar_historial():
    # Muestra todo lo que está guardado
    
    try:
        with open(ARCHIVO_HISTORIAL, "r") as archivo:
            contenido = archivo.read()
            
            if contenido.strip() == "":
                print("\nNo hay historial todavía ")

            else:
                print("\n===== HISTORIAL =====")
                print(contenido)
                
    except FileNotFoundError:

        # Si el archivo no existe aún, se evita que el programa falle

        print("\nNo hay historial todavía ")


def exportar_txt():
    # En este caso ya estamos trabajando en TXT 
    # Así que solo hacemos una copia con otro nombre
    
    try:
        with open(ARCHIVO_HISTORIAL, "r") as origen:
            contenido = origen.read()

        with open("resultados.txt", "w") as destino:
            destino.write(contenido)

        print("Historial exportado correctamente ")

    except FileNotFoundError:
         print("No hay datos para exportar ")
        # Su no hay historial, se muestra un mensaje indicando que no hay datos para exportar
         print("No hay datos para exportar ")