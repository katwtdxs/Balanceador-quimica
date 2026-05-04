# Función realizada por Lzeth Sastoque
# Aquí guardamos todo en un archivo de texto sencillo
# Es más fácil de manejar y no depende de formatos complejos

from datetime import datetime

ARCHIVO_HISTORIAL = "historial.txt"


def guardar_en_historial(ecuacion, balanceada, tipo):
    # Esta función guarda cada operación que realiza el usuario
    # Se abre el archivo en modo "append" para no borrar lo que ya hay, y se escribe la información con un formato legible


    with open(ARCHIVO_HISTORIAL, "a") as archivo:
        archivo.write("Ecuación: " + ecuacion + "\n")  # Se guarda la ecuación original
        archivo.write("Balanceada: " + balanceada + "\n") # Se guarda la ecuación ya balanceada
        archivo.write("Tipo: " + tipo + "\n") # Se guarda el tipo de reacción (síntesis, descomposición, etc.)
        archivo.write("Fecha: " + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + "\n")  # Se guarda la fecha y hora en la que se hizo la operación
        archivo.write("-" * 40 + "\n")  # separador para que no se mezcle todo


def mostrar_historial():
    # Esta función lee el archivo y muestra todo el historial guardado
    
    try:
        with open(ARCHIVO_HISTORIAL, "r") as archivo:
            contenido = archivo.read()
            


            # Si el archivo está vació, se muestra un mensaje 
            if contenido.strip() == "":
                print("\nNo hay historial todavía 🫠")
           
           # Si sí hay datos, se muestran organizados
            else:
                print("\n===== HISTORIAL =====")
                print(contenido)
                
    except FileNotFoundError:
        # Si el archivo no existe aún, se evita que el programa falle
        print("\nNo hay historial todavía 🫠")


def exportar_txt():
    # Esta función crea una copia del historial con otro nombre

    # Es decir "Exporta# el contenido a un nuevo archivo"
    
    try:
        # Se lee el archivo original y se guarda su contenido
        with open(ARCHIVO_HISTORIAL, "r") as origen:
            contenido = origen.read()
        # Se crea un nuevo archivo y se escribe el contenido del historial en él
        with open("resultados.txt", "w") as destino:
            destino.write(contenido)

        print("Historial exportado correctamente 📄")

    except FileNotFoundError:
        # Su no hay historial, se muestra un mensaje indicando que no hay datos para exportar
        print("No hay datos para exportar 😅")