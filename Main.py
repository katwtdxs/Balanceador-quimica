
"""Aquí va a ir la union de todo el codigo"""
print("-Probando")

try:
    num1 = input("Ingresa el primer número: ")
    num2 = input("Ingresa el segundo número: ")

    resultado = int(num1) + int(num2)

    print(f"\nLa suma de {num1} + {num2} es: {resultado}")

except ValueError:
    print("\nError: Por favor ingresa solo números.")