# HISTORIAL CON TXT 
# Función realizada por Lizeth Sastoque


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
        print("No hay datos para exportar")
