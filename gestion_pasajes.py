# reservas.py
import datetime # Importa la librería datetime para trabajar con fechas.
# Importa las listas de datos (reservas_pendientes, destinos_disponibles, clientes_registrados) desde el módulo de datos.
from .gestiondatos import reservas_pendientes, destinos_disponibles, clientes_registrados 
# Importa funciones de utilidad como la que genera IDs, pausa la consola y muestra menús.
from .funcionesutiles import obtener_siguiente_id, pausa_sistema, mostrar_menu_generico 
# Importa funciones de clientes (buscar_cliente_por_id_o_cuit, ver_clientes_registrados) que se necesitan aquí.
from .gestion_clientes import buscar_cliente_por_id_o_cuit, ver_clientes_registrados 

# -------------MODULO Gestión de Destinos

def listar_destinos_disponibles(): #Muestra el diccionario de destinos disponibles
    print("\n--- Listado de Destinos Disponibles ---") 
    if not destinos_disponibles: # Si el diccionario de destinos está vacio
        print("No hay destinos registrados en el sistema.") # Informamos que no hay destinos.
    else: # Si hay destinos...
        print("Sigla (Nombre del Destino) - Precio")
        # Recorre cada par clave-valor en el diccionario de destinos.
        for sigla, info_destino in destinos_disponibles.items(): #El método .items() devuelve una vista de los pares (clave, valor)
                                                            #del diccionario destinos disponibles. Cada "ítem" en el bucle for es una tupla que contiene la clave y su valor.
            
            # Imprime la sigla, el nombre y el precio del destino.
            print(f"°{sigla} ({info_destino['nombre']}) - ${info_destino['precio']:,.2f} ARS") # Formateamos el precio para miles.
    pausa_sistema() # Pausa el sistema para que el usuario pueda leer la información.


def registrar_nuevo_destino(): #Permite al usuario agregar un nuevo destino al diccionario
                                #destinos_disponibles. Requiere una sigla única, nombre y costo base.
    print("\n--- Registrar Nuevo Destino ---")
    sigla = input("Ingrese la SIGLA del nuevo destino (ej. ROS): ").upper() # Pedimos la sigla del nuevo destino.
    
    if sigla in destinos_disponibles: # Verificamos si la sigla ya existe.
        print(f"Error: La sigla '{sigla}' ya existe para el destino '{destinos_disponibles[sigla]['nombre']}'.")
        pausa_sistema()
        return

    nombre = input("Ingrese el NOMBRE del destino (ej. Rosario): ") # Pedimos el nombre del destino.
    
    try: # Usamos un try-except para manejar errores si el precio no es un número.
        precio = float(input("Ingrese el COSTO BASE del destino en ARS (ej. 50000): ")) # Pedimos el precio.
        if precio <= 0: # Validamos que el precio sea positivo.
            print("Error: El costo base debe ser un número positivo.")
            pausa_sistema()
            return
    except ValueError: # Si el usuario no ingresa valor numerico.
        print("Error: El costo base debe ser un número.")
        pausa_sistema()
        return

    # Si todo es válido, agregamos el nuevo destino al diccionario.
    destinos_disponibles[sigla] = {'nombre': nombre, 'precio': precio}
    print(f"Destino '{nombre}' ({sigla}) con costo ${precio:,.2f} ARS, registrado exitosamente.")
    pausa_sistema()


#Permite al usuario modificar el nombre o el precio de un destino existente.
 
def modificar_destino_existente():

    print("\n--- Modificar Destino ---")
    if not destinos_disponibles: # Verificamos si hay destinos para modificar.
        print("No hay destinos registrados para modificar.")
        pausa_sistema()
        return

    listar_destinos_disponibles() # Mostramos la lista de destinos para que el usuario elija.

    sigla_a_modificar = input("Ingrese la SIGLA del destino a modificar: ").upper()
    
    if sigla_a_modificar not in destinos_disponibles: # Verificamos si el destino existe.
        print("Error: Destino no encontrado.")
        pausa_sistema()
        return

    destino_a_modificar = destinos_disponibles[sigla_a_modificar] # Obtenemos el diccionario del destino.
    
    print(f"\nDatos actuales de {sigla_a_modificar} ({destino_a_modificar['nombre']}):")
    print(f"Nombre: {destino_a_modificar['nombre']}")
    print(f"Precio: ${destino_a_modificar['precio']:,.2f} ARS")

    print("\nIngrese los nuevos datos (deje en blanco para mantener el actual):")
    nuevo_nombre = input(f"Nuevo nombre ({destino_a_modificar['nombre']}): ")
    nuevo_precio_str = input(f"Nuevo precio ({destino_a_modificar['precio']:,.2f} ARS): ")

    if nuevo_nombre: # Si el usuario ingresó un nuevo nombre.
        destino_a_modificar['nombre'] = nuevo_nombre

    if nuevo_precio_str: # Si el usuario ingresó un nuevo precio.
        try:
            nuevo_precio = float(nuevo_precio_str)
            if nuevo_precio <= 0: # Validamos que el precio sea positivo.
                print("Error: El nuevo precio debe ser un número positivo. Precio no modificado.")
            else:
                destino_a_modificar['precio'] = nuevo_precio
        except ValueError:
            print("Error: El nuevo precio debe ser un número. Precio no modificado.")

    print(f"Destino '{sigla_a_modificar}' modificado exitosamente.")
    pausa_sistema()

# Permite al usuario eliminar un destino del diccionario destinos_disponibles.

def eliminar_destino_existente():

    print("\n--- Eliminar Destino ---")
    if not destinos_disponibles: # Verificamos si hay destinos para eliminar.
        print("No hay destinos registrados para eliminar.")
        pausa_sistema()
        return

    listar_destinos_disponibles() # Mostramos la lista de destinos para que el usuario elija.

    sigla_a_eliminar = input("Ingrese la SIGLA del destino a eliminar: ").upper()
    
    if sigla_a_eliminar not in destinos_disponibles: # Verificamos si el destino existe.
        print("Error: Destino no encontrado.")
        pausa_sistema()
        return
    
    # Preguntamos confirmación antes de eliminar.
    confirmacion = input(f"¿Está seguro de eliminar el destino '{destinos_disponibles[sigla_a_eliminar]['nombre']}' ({sigla_a_eliminar})? (S/N): ").upper()
    
    if confirmacion == 'S': # Si el usuario confirma.
        del destinos_disponibles[sigla_a_eliminar] # Eliminamos el destino del diccionario.
        print(f"Destino '{sigla_a_eliminar}' eliminado exitosamente.")
    else: # Si el usuario no confirma.
        print("Operación de eliminación cancelada.")
    pausa_sistema()


def gestionar_destinos_y_reservas(): # Función para que el usuario consulte destinos y cree nuevas reservas.
    print("\n--- Crear Nueva Reserva ---") 
    listar_destinos_disponibles() #mostramos los destinos disponibles. Llamando la funcion que muestra el diccionario

    # Pide al usuario que ingrese las siglas del destino que quiere reservar.
    destino_seleccionado_sigla = input("Ingrese siglas del destino para crear la reserva (o 'SALIR' para volver): ").upper()

    if destino_seleccionado_sigla == 'SALIR': # Si el usuario ingresa SALIR
        return # Sale de la función y regresa al menú principal 

# Verifica si la sigla ingresada  exist en el diccionario destinos_disponibles
    if destino_seleccionado_sigla in destinos_disponibles: 
        info_destino_elegido = destinos_disponibles[destino_seleccionado_sigla] #lo guarda en la variable info
        preciovuelo_elegido = info_destino_elegido['precio'] #y guarda aqui el precio indicando la posicion de precio del diccionario
        print(f"El costo de su viaje a {info_destino_elegido['nombre']} es de ${preciovuelo_elegido:,.2f} ARS") 

        # Pide confirmación al usuario para crear la reserva.
        confirmacion_reserva = input("Ingrese S para confirmar el boleto, ingrese N para cancelar la operación: ").upper() 
        
        if confirmacion_reserva == 'S': 
            fecha_ida_reserva = input("Ingrese la fecha de ida para su reserva (DD-MM-AAAA): ") 
            id_cliente_asociado_reserva = None # Inicializa la variable para el ID del cliente asociado como None.
            
            if clientes_registrados: # Verifica si hay clientes registrados para poder asociar uno.
                print("\nPara esta reserva, asocie un cliente existente:") # Pide asociar un cliente.
                ver_clientes_registrados() # Llama a la función de 'gestionclientes.py' para mostrar los clientes registrados.
                
                # Pide al usuario el ID o CUIT del cliente para asociar a la reserva.
                cliente_id_o_cuit_input = input("Ingrese el ID o CUIT del cliente para esta reserva (o deje en blanco para no asociar ahora): ")
                # Llama a la función de 'funcionesutiles.py' para buscar al cliente.
                cliente_asociado_encontrado = buscar_cliente_por_id_o_cuit(cliente_id_o_cuit_input) 
                
                if cliente_asociado_encontrado: # Si encuentra el cliente 
                    # Guarda el ID del cliente encontrado en nuestra variable antes definida como NONE
                    id_cliente_asociado_reserva = cliente_asociado_encontrado['id_cliente'] 
                    print(f"Reserva asociada al cliente: {cliente_asociado_encontrado['razonsocial_cliente']}.") 
                else: # Si el cliente no fue encontrado o el usuario no quiso asociar uno.
                    print("Cliente no encontrado o no se asoció cliente a la reserva en este momento.") 
            else: # Si no hay clientes registrados en el sistema.
                print("No hay clientes registrados. Cree uno antes de asociar a la reserva.")

            # Llama a la función de utilidad para obtener el siguiente ID único para la reserva.
            nuevo_id_reserva = obtener_siguiente_id(reservas_pendientes, 'id_reserva') 
            
            # Crea un diccionario para la nueva reserva con todos los datos recolectados.
            nueva_reserva = {
                'id_reserva': nuevo_id_reserva, 
                'destino_sigla': destino_seleccionado_sigla,
                'destino_nombre': info_destino_elegido['nombre'],
                'preciovuelo': preciovuelo_elegido,
                'fecha_ida': fecha_ida_reserva,
                'id_cliente_asociado': id_cliente_asociado_reserva 
            }
            reservas_pendientes.append(nueva_reserva) 
            
            print("\n--- ¡Boleto reservado! ---") 
            print("Por favor, diríjase a '3. Gestionar Ventas' para completar la compra.") 
            print(f"Reserva ID: {nueva_reserva['id_reserva']} para: {nueva_reserva['destino_nombre']} el {nueva_reserva['fecha_ida']} por ${nueva_reserva['preciovuelo']:,.2f} ARS")

        elif confirmacion_reserva == 'N': # Si el usuario cancela la reserva.
            print("Operación de reserva cancelada.")
        else: # Si la respuesta de confirmación no es 'Y' ni 'N'.
            print("Respuesta no válida.")
    else: # Si la sigla del destino ingresada no es reconocida.
        print("Destino no reconocido o no disponible.")
    pausa_sistema() 

def submenu_gestionar_destinos(): # Maneja las opciones dentro del submenú de Gestión de Destinos y Reservas.
 
    while True: # Bucle infinito para que el submenú se muestre hasta que el usuario decida salir.
        opciones_destinos = [ # Lista de las opciones disponibles en este submenú.
            "Listar Destinos",
            "Registrar Nuevo Destino",
            "Modificar Destino Existente",
            "Eliminar Destino Existente",
            "Crear Nueva Reserva",
            "Volver al Menú Principal"
        ]
        # Muestra el submenú usando la función y obtiene la opción que ingreso el usuario.
        opcion_elegida = mostrar_menu_generico("Submenú Gestión de Destinos y Reservas", opciones_destinos) 
        
        # Realiza la acción correspondiente según la opción elegida por el usuario.
        if opcion_elegida == '1':
            listar_destinos_disponibles() 
        elif opcion_elegida == '2':
            registrar_nuevo_destino() 
        elif opcion_elegida == '3':
            modificar_destino_existente() 
        elif opcion_elegida == '4':
            eliminar_destino_existente() 
        elif opcion_elegida == '5':
            gestionar_destinos_y_reservas() 
        elif opcion_elegida == '6':
            print("Volviendo al Menú Principal...") # Mensaje al salir del submenú.
            break # Sale del bucle 'while True', regresando al menú principal.
        else: # Si el usuario ingresa una opción no válida.
            print("Opción no válida. Intente de nuevo.") # Mensaje de error.
            pausa_sistema() # Pausa para que el usuario lea el error.