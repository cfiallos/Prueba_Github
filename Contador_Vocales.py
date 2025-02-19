#Entrada: Nada
#Proceso: Leer los datos
#Salida: El dato leido
def leer_datos_ingreso():
    print("Contador de Palabra")
    palabra = (input("Ingrese una plabra: "))
    return palabra

#Entrada: Palabra leida
#Proceso: Contar las vocales de la palabra
#Salida: Numero de vocales
def contar_vocales(palabra_leida):
    vocales = 'aeiou'
    contador_vocales = 0 #inicializamos una variable entera con valor 0
    for letra in palabra_leida: #El for va a iterar cada una de las letras que tiene la palabra
        if letra in vocales:   #En cada ejecución se evalua si la letra se encuentra dentro del string vocales
            contador_vocales += 1  
    #Cuando termina el bucle retornamos el valor de las vocales
    return  contador_vocales
    
#Entrada: Numero de vocales
#Proceso: Impirmir datos  
def imprimir_datos(numero_vocales):  #Se define una funcion que nos ayuda a imprimir el numero de vocales
    print(f'El numero de vocales es: {numero_vocales}') # 


leer_palabra = leer_datos_ingreso()

numero_vocales = contar_vocales(leer_palabra)

imprimir_datos(numero_vocales)