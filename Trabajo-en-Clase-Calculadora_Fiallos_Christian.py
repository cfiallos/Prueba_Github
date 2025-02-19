print("Bienvenido a mi calculadora") 


#Definición de operaciones

def sumar(numero_1, numero_2):
    return numero_1 + numero_2

def restar(numero_1, numero_2):
    return numero_1 - numero_2

def multiplicar(numero_1, numero_2):
    return numero_1 * numero_2

def dividir(numero_1, numero_2):
    return numero_1 / numero_2

def potenciar (numero_1, numero_2):
    return numero_1 ** numero_2

def imprimir_respuesta(respuesta):
    print(f"Este es el resultado {respuesta}")
    
def menu_calculadora():
    print("Menu de Operaciones")
    print("Elegir una operación")
    print("1.- Suma")
    print("2.- Resta")
    print("3.- Multiplicación")
    print("4.- Division")
    print("5.- Potenciación")
    numero_operacion = int(input("Ingrese un número de la operación: "))
    numero_1 = int(input("Ingrse el numero 1: "))
    numero_2 = int(input("Ingrese el numero 2: "))
    respuesta = 0

    match numero_operacion:
        case(1):
            respuesta = sumar(numero_1, numero_2)
        case(2):
            respuesta = restar(numero_1, numero_2)
        case(3):
            respuesta = multiplicar(numero_1, numero_2)
        case(4):
            respuesta = dividir(numero_1, numero_2)
        case(5):
            respuesta = potenciar(numero_1, numero_2)
    imprimir_respuesta(respuesta)

menu_calculadora()