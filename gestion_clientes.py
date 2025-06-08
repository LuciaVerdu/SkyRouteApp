#gestion_clientes.py
from .gestiondatos import clientes_registrados # Importa la lista de clientes desde data.py
from .funcionesutiles import obtener_siguiente_id, pausa_sistema, mostrar_menu_generico # Importa funciones de utilidad

# --- Módulo de Gestión de Clientes ---

def ver_clientes_registrados(): #Listado de los cliente registrados
    print("\n--- Ver Clientes ---")
    if not clientes_registrados: #corroboro que no este vacia mi lista para hacer la muestra
        print("No hay clientes registrados en el sistema.")
    else:
        print("Listado de Clientes:")
        for cliente in clientes_registrados:   #recorro la lista elemento por elemento y lo imprimo
            print(f"ID: {cliente['id_cliente']}, Razón Social: {cliente['razonsocial_cliente']}, CUIT: {cliente['cuit_cliente']}, Correo: {cliente['correo_cliente']}")
    pausa_sistema() #Pausamos para que el usuario pueda leer

def agregar_nuevo_cliente():  #Agrego un cliente a la lista clientes_registrados.
    
    print("\n--- Agregar Cliente ---") #ingreso variables por teclado 
    razonsocial_cliente = input("Ingrese nombre/razón social del nuevo cliente: ")
    cuit_cliente= input("Ingrese CUIT del nuevo cliente: ")
    correo_cliente = input("Ingrese Correo de Contacto del nuevo cliente: ")
#verifica que no esten en blanco
    if not razonsocial_cliente or not cuit_cliente or not correo_cliente:
        print("Error: DEBE COMPLETAR TODOS LOS CAMPOS.")
    else: #si no estan en blanco, busca con un ciclo for cada posicion en la lista clientesregistrados y cuando encuentra el mismo cuit 
            #verifica que el cuit ya esta ingresado
        if any(cuit['cuit_cliente'] == cuit_cliente for cuit in clientes_registrados):
            print("Error: Ya existe un cliente con el CUIT ingresado.")
            pausa_sistema() #Pausamos para que el usuario pueda leer
            return
#variable definida globalmente en el main
        id_cliente = obtener_siguiente_id(clientes_registrados, 'id_cliente') #llamo la funcion para incrementar el id del cliente
#guardo en el diccionario nuevo_cliente los datos ingresados por teclado anteriormente
        nuevo_cliente = {
            'id_cliente': id_cliente,
            'razonsocial_cliente': razonsocial_cliente,
            'cuit_cliente': cuit_cliente,
            'correo_cliente': correo_cliente,
        }
#agrego los datos del diccionario a mi lista clientes registrados y los muestro
        clientes_registrados.append(nuevo_cliente)
        print(f"Cliente '{razonsocial_cliente}' (ID: {id_cliente}) agregado exitosamente.")
    pausa_sistema() #Pausamos para que el usuario pueda leer
def buscar_cliente_por_id_o_cuit(identificador_busqueda): # Encuentra un cliente por su ID o CUIT en la lista de clientes_registrados.

    #Primero, verificamos si el identificador de búsqueda ingresado es completamente numérico.
    # Si es numérico, asumimos que el usuario ingresó un ID de cliente.
    if identificador_busqueda.isdigit(): 
        id_int = int(identificador_busqueda) # Convertimos el string numérico a un entero para poder compararlo.
        # Recorremos la lista de todos los clientes registrados.
        for cliente in clientes_registrados:
            # Si el 'id_cliente' del cliente actual coincide con el ID que buscamos...
            if cliente['id_cliente'] == id_int:
                return cliente # Devolvemos el diccionario completo de ese cliente y salimos de la función.
    
    # Si el identificador no era numérico (o si no se encontró por ID),
    # intentamos buscarlo como un CUIT.
    # Recorremos la lista de todos los clientes registrados nuevamente.
    for cliente in clientes_registrados:
        # Si el 'cuit_cliente' del cliente actual coincide con el identificador de búsqueda...
        if cliente['cuit_cliente'] == identificador_busqueda:
            return cliente # Devolvemos el diccionario completo de ese cliente y salimos de la función.
            
    return None # Si después de ambas búsquedas (por ID y por CUIT) no se encontró ningún cliente, devolvemos None.

def modificar_cliente_existente(): #  Permite actualizar los datos de un cliente existente.
    print("\n--- Modificar Cliente ---")
    if not clientes_registrados: #verifico que la lista
        print("No hay clientes para modificar. Agregue uno primero.")
        pausa_sistema() #Pausamos para que el usuario pueda leer
        return

    identificador_cliente = input("Ingrese el ID o CUIT del cliente a modificar: ")
    cliente_encontrado = buscar_cliente_por_id_o_cuit(identificador_cliente)

    if cliente_encontrado:
        print(f"\nDatos actuales del cliente (ID: {cliente_encontrado['id_cliente']}):")
        print(f"Razón Social: {cliente_encontrado['razonsocial_cliente']}")
        print(f"CUIT: {cliente_encontrado['cuit_cliente']}")
        print(f"Correo: {cliente_encontrado['correo_cliente']}")

        print("\nIngrese los nuevos datos (deje en blanco para mantener el actual):")
        nueva_razonsocial_input = input(f"Nueva Razón Social ({cliente_encontrado['razonsocial_cliente']}): ")
        nuevo_cuit_input = input(f"Nuevo CUIT ({cliente_encontrado['cuit_cliente']}): ")
        nuevo_correo_input = input(f"Nuevo Correo ({cliente_encontrado['correo_cliente']}): ")

        if nueva_razonsocial_input:
            cliente_encontrado['razonsocial_cliente'] = nueva_razonsocial_input
        if nuevo_cuit_input:
            if any(c['cuit_cliente'] == nuevo_cuit_input and c['id_cliente'] != cliente_encontrado['id_cliente'] for c in clientes_registrados):
                print("Error: El nuevo CUIT ya pertenece a otro cliente y no se puede usar. El CUIT actual se mantuvo.")
            else:
                cliente_encontrado['cuit_cliente'] = nuevo_cuit_input
        if nuevo_correo_input:
            cliente_encontrado['correo_cliente'] = nuevo_correo_input
        
        print(f"Cliente (ID: {cliente_encontrado['id_cliente']}) modificado exitosamente.")
    else:
        print("Cliente no encontrado.")
    pausa_sistema() #Pausamos para que el usuario pueda leer

def eliminar_cliente_existente(): # elimina un cliente del sistema
    print("\n--- Eliminar Cliente ---")
    if not clientes_registrados:
        print("No hay cliente para eliminar.")
        pausa_sistema() #Pausamos para que el usuario pueda leer
        return

    identificador_cliente = input("Ingrese el ID o CUIT del cliente a eliminar: ")
    cliente_a_eliminar = buscar_cliente_por_id_o_cuit(identificador_cliente)

    if cliente_a_eliminar:
        confirmacion = input(f"¿Está seguro de eliminar a '{cliente_a_eliminar['razonsocial_cliente']}' (ID: {cliente_a_eliminar['id_cliente']})? (S/N): ").upper()
        if confirmacion == 'S':
            clientes_registrados.remove(cliente_a_eliminar)
            print("Cliente eliminado exitosamente.")
        else:
            print("Operación cancelada.")
    else:
        print("Cliente no encontrado.")
    pausa_sistema() #Pausamos para que el usuario pueda leer



def submenu_gestionar_clientes(): #Maneja las opciones dentro del menú de Gestión de Clientes.
    while True:
        opciones_clientes = [   #opciones disponibles en una lista
            "Ver Clientes",
            "Agregar Cliente",
            "Modificar Cliente",
            "Eliminar Cliente",
            "Volver al Menú Principal"
        ]
        opcion_clientes_elegida = mostrar_menu_generico("Submenú Gestionar Clientes", opciones_clientes) #llama la funcion que recorre 
                                                                                                    #la lista en este caso opciones clientes
                                                                                                    # y devuelve la opcion que ingreso
#verifica que opcion de la lista ingrese  y inicializa la funcion indicada en cada caso
        if opcion_clientes_elegida == '1':
            ver_clientes_registrados()
        elif opcion_clientes_elegida == '2':
            agregar_nuevo_cliente()
        elif opcion_clientes_elegida == '3':
            modificar_cliente_existente()
        elif opcion_clientes_elegida == '4':
            eliminar_cliente_existente()
        elif opcion_clientes_elegida == '5':
            print("Volviendo al Menú Principal...")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            pausa_sistema() #Pausamos para que el usuario pueda leer

