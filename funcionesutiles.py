#funciones utiles.py


def obtener_siguiente_id(lista_registros, clave_id): #Esta funcion es llamada en la funcion de agregar clientes nuevos y sirve para incrementar el ID
#Toma como argumento la lista clientes_registrados 
#verifica primero en la lista de registros si ya hay algun cliente ingresado y si no lo hay cambia el valor a 1
    if not lista_registros:
        return 1
    
    #Creamos una variable para guardar el ID más alto que encuentre.
    # La inicializamos en 0, asumiendo que los IDs siempre serán 1 o más.
    id_mas_alto_encontrado = 0
    
    # Paso 3: Recorremos cada 'registro' (que es un diccionario) en la lista de registros ( que trae la info de clientes_registrados).
    for registro_actual in lista_registros:
#El ciclo for va a tomar un elemento a la vez de la lista.
#En cada "vuelta" del ciclo, el elemento que se toma de la lista se guarda temporalmente en la variable registro_actual
        id_actual = registro_actual.get(clave_id, 0)  #Guardo en la variable id actual el ID del registro 
                                                    #y si clave_id no existe asume que su ID es 0. Utilizamos el GET por error en el codigo

#comparo el id actual y el id que deifinimos en 0 
        if id_actual > id_mas_alto_encontrado:
            # Si es así, actualizamos 'id_mas_alto_encontrado' con este nuevo valor.
            id_mas_alto_encontrado = id_actual
            
    # Cambio el contador al siguiente ID disponible es el 'id_mas_alto_encontrado' más 1.
    return id_mas_alto_encontrado + 1

def pausa_sistema(): #Pausamos para que el usuario pueda leer
    input("\nPresione Enter para continuar...")

def mostrar_menu_generico(titulo_menu, opciones_menu):
    print(f"\n--- {titulo_menu} ---")
    
    contador = 1  # Inicializamos un contador manual en 1
    for opcion_texto in opciones_menu: # Recorremos la lista de opciones del submenu
        print(f"{contador}. {opcion_texto}") # Usamos el contador para numerar e ir mostrando las opciones de la lista del submenu
        contador += 1  # Incrementamos el contador en cada vuelta del bucle
        
    print("----------------------------------------------------------")
    return input("Ingrese una opción: ")   #En esta misma funcion cuando se ejecuta el cliente ingresa la opcion del submenu
