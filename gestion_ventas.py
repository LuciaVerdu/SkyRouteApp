# ventas.py
import datetime # Importa la librería datetime para trabajar con fechas (obtener la fecha actual).
# Importa las listas de datos (reservas_pendientes, ventas_finalizadas) desde el módulo 'datos'.
from .gestiondatos import reservas_pendientes, ventas_finalizadas 
# Importa funciones de utilidad como la que genera IDs, pausa la consola y muestra menús.
from .funcionesutiles import obtener_siguiente_id, pausa_sistema, mostrar_menu_generico 
# Importa la función de búsqueda de cliente desde el módulo 'clientes' (necesaria para asociar reservas/ventas a clientes).
from .gestion_clientes import buscar_cliente_por_id_o_cuit 


# --- MODULO Gestión de Ventas ---

def procesar_reserva_pendiente(): # Permite al usuario seleccionar una reserva pendiente y registrarla como una venta finalizada.
    print("\n--- Procesar Reserva Pendiente ---") # Título del menú.
    if not reservas_pendientes: # Verifica si la lista de reservas pendientes está vacía.
        print("No hay ninguna reserva pendiente para procesar.") # Mensaje si no hay reservas.
        print("Por favor, vaya a '2. Gestionar Destinos' para crear una reserva primero.") # Instrucción al usuario.
        pausa_sistema() # Pausa para que el usuario pueda leer.
        return # Sale de la función.

    print("\nReservas Pendientes:") # Si hay reservas, muestra el listado.
    # Recorre la lista de 'reservas_pendientes' usando 'enumerate()' para obtener el índice (i) y la reserva (diccionario).
    for i, reserva in enumerate(reservas_pendientes): 
        cliente_info_reserva = "Sin cliente asociado" #defino esta variable, para luego al ingresar una reserva rellenarla
# verifica si la clave 'id_cliente_asociado' existe en el diccionario reserva y su valor no es None o vacío
        if reserva.get('id_cliente_asociado'): 
            cliente_relacionado = buscar_cliente_por_id_o_cuit(str(reserva['id_cliente_asociado'])) 
            # Si se encontró el cliente,lo busca con la fucion y lo guarda en cliente relacionado
            if cliente_relacionado: #si existe lo guarda en inforeserva y muestra sus datos
                cliente_info_reserva = f"Cliente: {cliente_relacionado['razonsocial_cliente']} (CUIT: {cliente_relacionado['cuit_cliente']})"
        
    print(f"{i+1}. ID Reserva: {reserva['id_reserva']}, Destino: {reserva['destino_nombre']}, Fecha Ida: {reserva['fecha_ida']}, Precio: ${reserva['preciovuelo']} ARS. {cliente_info_reserva}") 
        
    try: # Inicia un bloque 'try' para manejar posibles errores en la entrada del usuario.
        # Pide al usuario que ingrese el NÚMERO de la reserva a procesar y le resta 1 para obtener el índice de la lista.
        idx_reserva_elegida = int(input("Ingrese el NÚMERO de la reserva a procesar: ")) - 1 

# Valida que el índice ingresado esté dentro del rango válido de la lista de reservas pendientes.
        if not (0 <= idx_reserva_elegida < len(reservas_pendientes)): 
            print("Número de reserva inválido.") # Mensaje de error si el número está fuera de rango.
            pausa_sistema() # Pausa para que el usuario pueda leer el error.
            return # Sale de la función.

    except ValueError: # el usuario no ingresa un número 
        print("Entrada inválida. Por favor, ingrese un número.") # Mensaje de error.
        pausa_sistema() # Pausa.
        return # Sale de la función.

    # Si la entrada es válida, obtiene el diccionario completo de la reserva seleccionada.
    reserva_a_procesar = reservas_pendientes[idx_reserva_elegida] 

    cliente_para_venta = None # Inicializa la variable para el cliente de la venta.
#Si la reserva tiene un id_cliente_asociado válido, entonces se intenta buscar la información completa de ese cliente
    if reserva_a_procesar.get('id_cliente_asociado'): 
        # Busca los detalles completos de ese cliente. Y los guarda en cliente para
        cliente_para_venta = buscar_cliente_por_id_o_cuit(str(reserva_a_procesar['id_cliente_asociado'])) 
        
        # Si el cliente asociado no se encontró (ej. fue eliminado del sistema)
        if not cliente_para_venta:
            print("No se pudo asociar un cliente válido a la reserva. Venta cancelada.")
            pausa_sistema()
            return

#Si la reserva no tiene un id_cliente_asociado.
    if not cliente_para_venta: 
        
        cliente_para_venta = {
            'id_cliente': None, 
            'razonsocial_cliente': "Cliente No Asociado", 
            'cuit_cliente': "N/A", 
            'correo_cliente': "N/A"
        }
        print("Advertencia: Esta reserva se procesará sin un cliente registrado formalmente.")

    # Muestra un resumen de los detalles de la reserva y el cliente antes de la confirmación final.
    print(f"\n--- Detalles de la Reserva a Procesar (ID: {reserva_a_procesar['id_reserva']}) ---")
    print(f"Cliente: {cliente_para_venta['razonsocial_cliente']} (CUIT: {cliente_para_venta['cuit_cliente']})")
    print(f"Destino: {reserva_a_procesar['destino_nombre']}")
    print(f"Fecha de Ida: {reserva_a_procesar['fecha_ida']}")
    print(f"Precio: ${reserva_a_procesar['preciovuelo']:,.2f} ARS") # Formateamos el precio.

    # Pide confirmación final al usuario para registrar la venta.
    confirmacion_venta = input("\n¿Confirmar la venta de esta reserva? (S/N): ").upper() 
    
    if confirmacion_venta == 'S': # Si el usuario confirma la venta
        # Obtiene el siguiente ID único para la nueva venta (pasaje)
        nuevo_id_venta = obtener_siguiente_id(ventas_finalizadas, 'id_pasaje')
        
# Crea el diccionario que contendrá toda la información de la venta finalizada
        venta_registrada_data = {
            'id_pasaje': nuevo_id_venta,
            'id_cliente_asociado': cliente_para_venta['id_cliente'],
            'razonsocial_cliente': cliente_para_venta['razonsocial_cliente'],
            'cuit_cliente': cliente_para_venta['cuit_cliente'],
            'correo_cliente': cliente_para_venta['correo_cliente'],
            'destino': reserva_a_procesar['destino_nombre'],
            'precio': reserva_a_procesar['preciovuelo'],
            'fecha_venta': datetime.datetime.now(), # para incluir la hora exacta
            'fecha_vuelo': reserva_a_procesar['fecha_ida'],
            'estado': 'Activa' ##La venta se registra como 'Activa'.
        }
        ventas_finalizadas.append(venta_registrada_data) # Agrega el diccionario de la venta a la lista de ventas finalizadas.

        reservas_pendientes.pop(idx_reserva_elegida) # Elimina la reserva de la lista de pendientes (ya no está pendiente, ahora es una venta).
        
        print("\n--- ¡Venta de Reserva Procesada con Éxito! ---")

# Imprime un resumen  de la venta realizada.
        print(f"ID de Venta: {venta_registrada_data['id_pasaje']}")
        print(f"Cliente: {venta_registrada_data['razonsocial_cliente']}")
        print(f"Destino: {venta_registrada_data['destino']}")
        print(f"Precio: ${venta_registrada_data['precio']:,.2f} ARS")
        print(f"Fecha y Hora de Venta: {venta_registrada_data['fecha_venta'].strftime('%d-%m-%Y %H:%M:%S')}")  #uso funcion datetime para ver fecha y hora
        print(f"Fecha de Vuelo: {venta_registrada_data['fecha_vuelo']}")
        print(f"Estado: {venta_registrada_data['estado']}") # Muestra el estado de la venta.
        print(f"Se enviará a su correo: {venta_registrada_data['correo_cliente']} el cupón de pago e indicaciones para finalizar la venta.")
    else: # Si el usuario no confirma la venta.
        print("Procesamiento de reserva cancelado.")
    pausa_sistema() # Pausa al final de la operación.

def cancelar_reserva_pendiente(): # Función para cancelar una reserva que aún no ha sido vendida (está pendiente).
    print("\n--- Cancelar Reserva Pendiente ---")
    if not reservas_pendientes: # Verifica si la lista de reservas pendientes está vacía.
        print("No hay ninguna reserva pendiente para cancelar.") # Mensaje si no hay reservas.
        pausa_sistema() # Pausa.
        return # Sale de la función.

    print("\nReservas Pendientes:") # Muestra el listado de reservas pendientes.
    # Recorre la lista de 'reservas_pendientes' para mostrarlas al usuario.
    for i, reserva in enumerate(reservas_pendientes): 
        cliente_info_reserva = "Sin cliente asociado" 
        if reserva.get('id_cliente_asociado'): 
            
            cliente_relacionado = buscar_cliente_por_id_o_cuit(str(reserva['id_cliente_asociado'])) 
            if cliente_relacionado: # Si el cliente fue encontrado.
                cliente_info_reserva = f"Cliente: {cliente_relacionado['razonsocial_cliente']} (CUIT: {cliente_relacionado['cuit_cliente']})" # Incluye CUIT para mayor detalle.
        # Imprime los detalles de la reserva.
        print(f"{i+1}. ID Reserva: {reserva['id_reserva']}, Destino: {reserva['destino_nombre']}, Fecha Ida: {reserva['fecha_ida']}, Precio: ${reserva['preciovuelo']:,.2f} ARS. {cliente_info_reserva}")

    try: # Bloque 'try' para la entrada del usuario.
        # Pide al usuario el numero de la reserva a cancelar y lo convierte a índice.
        idx_reserva_cancelar = int(input("Ingrese el NÚMERO de la reserva a cancelar: ")) - 1 
        # Valida que el índice esté dentro del rango.
        if not (0 <= idx_reserva_cancelar < len(reservas_pendientes)): 
            print("Número de reserva inválido.") 
            pausa_sistema() 
            return 
    except ValueError: # Captura si la entrada no es un número.
        print("Entrada inválida. Por favor, ingrese un número.")
        pausa_sistema()
        return 

    # Si la entrada es válida, obtiene la reserva a cancelar.
    reserva_a_cancelar = reservas_pendientes[idx_reserva_cancelar] 
    # Pide confirmación al usuario para la cancelación.
    confirmacion_cancelacion = input(f"¿Está seguro de cancelar la reserva ID {reserva_a_cancelar['id_reserva']} para {reserva_a_cancelar['destino_nombre']} ({reserva_a_cancelar['fecha_ida']})? (S/N): ").upper()
    
    if confirmacion_cancelacion == 'S': # Si el usuario confirma.
        reservas_pendientes.pop(idx_reserva_cancelar) # Elimina la reserva de la lista de pendientes.
        print("Reserva cancelada exitosamente. Derecho de cancelación de compra (Ley 24.240 de Defensa al Consumidor y en el Código Civil y Comercial de la Nación (Ley 26.994)).")
    else: # Si el usuario no confirma.
        print("Cancelación de reserva abortada.")
    pausa_sistema() # Pausa al final de la operación.

def submenu_gestionar_ventas(): # Función que maneja las opciones dentro del submenú de Gestión de Ventas.
    while True: # Bucle infinito para mostrar el submenú hasta que el usuario decida volver.
        opciones_ventas = [ # Lista de opciones para este submenú.
            "Procesar reserva pendiente",
            "Cancelar reserva pendiente",
            "Volver al Menú Principal"
        ]
# Muestra el submenú usando la funciónes utiles
        opcion_ventas_elegida = mostrar_menu_generico("Submenú Gestionar Ventas", opciones_ventas) 
# Llama a la función correspondiente según la opción elegida.
        if opcion_ventas_elegida == '1':
            procesar_reserva_pendiente()
        elif opcion_ventas_elegida == '2':
            cancelar_reserva_pendiente()
        elif opcion_ventas_elegida == '3':
            print("Volviendo al Menú Principal...") # Mensaje al salir del submenú.
            break # Sale del bucle 'while True'.
        else: # Si la opción ingresada no es válida.
            print("Opción no válida. Intente de nuevo.")
            pausa_sistema()
