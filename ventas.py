import datetime
from .datos import reservas_pendientes, ventas_finalizadas # Importa las listas
from .funcionesutiles import obtener_siguiente_id, pausa_sistema, mostrar_menu_generico # Importa funciones de utilidad
from .clientes import buscar_cliente_por_id_o_cuit # Importa funciones de clientes




# --- Módulo de Gestión de Ventas ---

def procesar_reserva_pendiente():# Permite al usuario consultar destinos y crear nuevas reservas de vuelo
    global id_venta    #llamo a la variable que creamos como contador por fuera 
    print("\n--- Procesar Reserva Pendiente ---")
    if not reservas_pendientes:   #si no hay reservas en la lista 
        print("No hay ninguna reserva pendiente para procesar.")
        print("Por favor, vaya a '2. Gestionar Destinos' para crear una reserva primero.")
        pausa_sistema() #Pausamos para que el usuario pueda leer
        return

    print("\nReservas Pendientes:") #Si hay reservas en la lista
    for i, reserva in enumerate(reservas_pendientes): #recorro la lista usando enumerate() es una función incorporada de Python.
                                                        #produce pares de datos: (índice, valor) i: recibe el índice,
                                                        # reserva: recibe el valor del elemento de la lista en esa posición. 
                                                        #en este caso, reserva es el diccionario completo de una de las reservas pendientes.
        cliente_info_reserva = "Sin cliente asociado"
        if reserva['id_cliente_asociado']:   #verifica si el valor de id_cliente_asociado existe 
            cliente_relacionado = buscar_cliente_por_id_o_cuit(str(reserva['id_cliente_asociado'])) #Llamo y guardo en la variable cliente relacionado
                                                                                                    #la funcion que pide ingresar un ID o cuit
                                                                                                    #y nos devuelve la info de ese cliente
            if cliente_relacionado: # si se registro algo en la variable cambio el valor de cliente_info_reserva antes definida en "sin cleinte asociado"
                cliente_info_reserva = f"Cliente: {cliente_relacionado['razonsocial_cliente']} (CUIT: {cliente_relacionado['cuit_cliente']})"
        #imprime los recorridos del ciclo for de reservas pendientes
        print(f"{i+1}. ID Reserva: {reserva['id_reserva']}, Destino: {reserva['destino_nombre']}, Fecha Ida: {reserva['fecha_ida']}, Precio: ${reserva['preciovuelo']} ARS. {cliente_info_reserva}")
        
    try: # Intenta hacer esto siguiente..
        idx_reserva_elegida = int(input("Ingrese el NÚMERO de la reserva a procesar: ")) - 1 # Pide al usuario que ingrese un número usamos int() para convertirlo a un número entero.
        # Le restamos 1, porque si el usuario ve "1." y lo elige, en la lista es el índice 0.
        # Entonces, si ingresa 1, lo convertimos a 0. Si ingresa 2, lo convertimos a 1, y así.

        if not (0 <= idx_reserva_elegida < len(reservas_pendientes)): #si NO está en el rango, entonces...
            # len(reservas_pendientes) nos da la cantidad total de reservas en la lista.
            # Por ejemplo, si hay 3 reservas, len() es 3 los índices válidos irían de 0 a 2 (len - 1).
            # Esta condición verifica si el número que ingresó el usuario está fuera de ese rango válido (o sea, si es menor a 0 o mayor o igual a la cantidad de reservas).
            print("Número de reserva inválido.") #mostramos este mensaje de error.
            pausa_sistema() # Pausamos para que el usuario pueda leer el error.
            return #salimos de la función, no podemos seguir con la reserva inválida.

    except ValueError: # Si en el bloque 'try' algo salió mal y fue un "ValueError" por ejemplo, si el usuario NO ingresa un número.
        print("Entrada inválida. Por favor, ingrese un número.") # Mostramos un mensaje para ese error.
        pausa_sistema() # Pausamos para que el usuario pueda leer el error.
        return # Y también salimos de la función, porque la entrada no fue válida.

    reserva_a_procesar = reservas_pendientes[idx_reserva_elegida]  # si la entrada estuvo en el rango correcto,
                                                        #lo busca en la lista de reservas y lo guarda en la variable reserva a procesar

    cliente_para_venta = None #defino esta variable en none para luego cambiarla cuando este lista la venta
    if reserva_a_procesar['id_cliente_asociado']: # si existe un dato guardado en mi variable anterior
        cliente_para_venta = buscar_cliente_por_id_o_cuit(str(reserva_a_procesar['id_cliente_asociado'])) #le cambio el valor de None y
        #guardo en la variable cliente para venta la funcion que devuelve el diccionario completo del cliente si lo encuentra segun el id asociado
        
        if not cliente_para_venta:
            print("No se pudo asociar un cliente a la reserva. Venta cancelada.")
            pausa_sistema()
            return
#muestro todos los datos del cliente de la reserva a procesar
    print(f"\n--- Detalles de la Reserva a Procesar (ID: {reserva_a_procesar['id_reserva']}) ---")
    print(f"Cliente: {cliente_para_venta['razonsocial_cliente']} (CUIT: {cliente_para_venta['cuit_cliente']})")
    print(f"Destino: {reserva_a_procesar['destino_nombre']}")
    print(f"Fecha de Ida: {reserva_a_procesar['fecha_ida']}")
    print(f"Precio: ${reserva_a_procesar['preciovuelo']} ARS")
#Guardo en este variable el ingreso por teclado de la confirmacion
    confirmacion_venta = input("\n¿Confirmar la venta de esta reserva? (S/N): ").upper() 
#si es S guardo la info del cliente 
    if confirmacion_venta == 'S':
#Llamo a la funcion que aumenta el ID para que le asigne uno al nuevo registro id_pasaje del diccionario dentro de la lista ventas finalizadas
#y guardo el valor en id_venta
        id_venta = obtener_siguiente_id(ventas_finalizadas, 'id_pasaje')
#creacion del diccionario que contiene la informacion de cada venta      
        venta_registrada_data = {
            'id_pasaje': id_venta,
            'id_cliente_asociado': cliente_para_venta['id_cliente'],
            'razonsocial_cliente': cliente_para_venta['razonsocial_cliente'],
            'cuit_cliente': cliente_para_venta['cuit_cliente'],
            'correo_cliente': cliente_para_venta['correo_cliente'],
            'destino': reserva_a_procesar['destino_nombre'],
            'precio': reserva_a_procesar['preciovuelo'],
#utilizo la libreria importada DATETIME para convertir con la funcion datetime.date.today los datos ingresados tipo texto a tipo fecha
            'fecha_venta': datetime.date.today().strftime("%d-%m-%Y"),   
            'fecha_vuelo': reserva_a_procesar['fecha_ida']
        }
#Agrego los datos del diccionario a la lista ventas_finalizadas
        ventas_finalizadas.append(venta_registrada_data)

        reservas_pendientes.pop(idx_reserva_elegida) #POP metodo de las listas de Python.Para eliminar un elemento de la lista reservas pendientes.
                                                    #borra el id pendiente de reserva ya que se confirmo la venta
#imprimo los datos del diccionario con los datos de la venta
        print("\n--- ¡Venta de Reserva Procesada con Éxito! ---")
        print(f"ID de Venta: {venta_registrada_data['id_pasaje']}")
        print(f"Cliente: {venta_registrada_data['razonsocial_cliente']}")
        print(f"Destino: {venta_registrada_data['destino']}")
        print(f"Precio: ${venta_registrada_data['precio']:,.2f} ARS")
        print(f"Fecha de Venta: {venta_registrada_data['fecha_venta']}")
        print(f"Fecha de Vuelo: {venta_registrada_data['fecha_vuelo']}")
        print(f"Se enviará a su correo: {venta_registrada_data['correo_cliente']} el cupón de pago e indicaciones para finalizar la venta.")
    else:
#si no ingresa S para confirmar la venta
        print("Procesamiento de reserva cancelado.")
    pausa_sistema() # Pausamos para que el usuario pueda leer el error.

def cancelar_reserva_pendiente():  #Funcion para cancelar una reserva que todavia no ha sido vendida 
    print("\n--- Cancelar Reserva Pendiente ---")
    if not reservas_pendientes: #Si la lista esta vacia
        print("No hay ninguna reserva pendiente para cancelar.")
        pausa_sistema() #pausa para leer error y salir 
        return
#utilizo un ciclo
    print("\nReservas Pendientes:")
    for i, reserva in enumerate(reservas_pendientes):     #recorro la lista usando enumerate() es una función incorporada de Python.
                                                        #produce pares de datos: (índice, valor) i: recibe el índice,
                                                        # reserva: recibe el valor del elemento de la lista en esa posición. 
                                                        #en este caso, reserva es el diccionario completo de una de las reservas pendientes.
#se repite el mismo codigo que al buscar una reserva para luego venderla       
        cliente_info_reserva = "Sin cliente asociado"  
 
        if reserva['id_cliente_asociado']:  #verifica si el valor, que estamos recorriendo en la lista, de id_cliente_asociado existe 
            cliente_relacionado = buscar_cliente_por_id_o_cuit(str(reserva['id_cliente_asociado'])) #Llamo y guardo en la variable cliente relacionado
                                                                                                    #la funcion que pide ingresar un ID o cuit
                                                                                                    #y nos devuelve la info de ese cliente
#si se registro algo en la variable cambio el valor de cliente_info_reserva antes definida como "sin cliente asociado"
            if cliente_relacionado:
                cliente_info_reserva = f"Cliente: {cliente_relacionado['razonsocial_cliente']}"
#imprime los recorridos del ciclo for de reservas pendientes
        print(f"{i+1}. ID Reserva: {reserva['id_reserva']}, Destino: {reserva['destino_nombre']}, Fecha Ida: {reserva['fecha_ida']}, Precio: ${reserva['preciovuelo']:,.2f} ARS. {cliente_info_reserva}")

    try: 
        idx_reserva_cancelar = int(input("Ingrese el NÚMERO de la reserva a cancelar: ")) - 1 #Pide al usuario que ingrese un número usamos int() para convertirlo a un número entero.
        # Le restamos 1, porque si el usuario ve "1." y lo elige, en la lista es el índice 0.
        # Entonces, si ingresa 1, lo convertimos a 0. Si ingresa 2, lo convertimos a 1, y así.
        if not (0 <= idx_reserva_cancelar < len(reservas_pendientes)): #verifico que este en el numero este en el rango de valores que existen en la lista 
            print("Número de reserva inválido.")  #si no esta imprime este mensaje
            pausa_sistema() #pausa para leer el error
            return  #sale para que ingrese otro
    except ValueError:  #si no ingresa un valor numerico
        print("Entrada inválida. Por favor, ingrese un número.")
        pausa_sistema() #pausa para leer el error
        return  #sale para que ingrese otro

    reserva_a_cancelar = reservas_pendientes[idx_reserva_cancelar] #si el ingreso fue correcto no ingresa al if ni al except y guarda
                                                                    #en la variable reserva cancelar la info de la lista en ese id ingresado
    #consulta por teclado si quiere confirmar la cancelacion
    confirmacion_cancelacion = input(f"¿Está seguro de cancelar la reserva ID {reserva_a_cancelar['id_reserva']} para {reserva_a_cancelar['destino_nombre']} ({reserva_a_cancelar['fecha_ida']})? (S/N): ").upper()
    #si ingreso S elimina de la lista con la funcion POP la info de la lista del id ingresado
    if confirmacion_cancelacion == 'S':
        reservas_pendientes.pop(idx_reserva_cancelar)
        print("Reserva cancelada exitosamente. Derecho de cancelación de compra (Ley 24.240 de Defensa al Consumidor y en el Código Civil y Comercial de la Nación (Ley 26.994)).")
    else: #si no ingresa S 
        print("Cancelación de reserva abortada.")
    pausa_sistema() #pausa para que pueda leer el error
def submenu_gestionar_ventas(): #funcion para el sub menu de ventas

    while True:
        #imprimimos el sub menu
        print("\n--- Submenú Gestionar Ventas ---")
        print("1. Procesar reserva pendiente")
        print("2. Cancelar reserva pendiente")
        print("3. Volver al Menú Principal")
        print("----------------------------------------------------------")
        opcion_ventas_elegida = input("Ingrese una opción: ") #Ingreso de la opcion por teclado
#condicionales que llaman la funcion que corresponda segun la opcion que se ingrese
        if opcion_ventas_elegida == '1':
            procesar_reserva_pendiente()
        elif opcion_ventas_elegida == '2':
            cancelar_reserva_pendiente()
        elif opcion_ventas_elegida == '3':
            print("Volviendo al Menú Principal...")
            break #sale del sub menu
        else:#si no ingresa una de las opciones existentes
            print("Opción no válida. Intente de nuevo.")
            pausa_sistema() #pausa para leer el error