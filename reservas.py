#PASAJES Y RESERVAS
import datetime
from .datos import reservas_pendientes, destinos_disponibles, clientes_registrados # Importa las listas y diccionario
from .funcionesutiles import obtener_siguiente_id, pausa_sistema # Importa funciones de utilidad
from .clientes import buscar_cliente_por_id_o_cuit, ver_clientes_registrados # Importa funciones de clientes que necesita
# --- MODULO Gestión de Destinos y Reservas ---

def gestionar_destinos_y_reservas():  #funcion para ingresar el destino, toma datos del diccionario de destinos 
    global id_reserva       #llamo la variable contador del id reserva definida al comienzo para incrementarla aca.
    print("\n--- Gestionar Destinos ---")
    print("Listado de destinos disponibles:")
    for sigla, info_destino in destinos_disponibles.items():  #recorre el diccionario la sigla y su correspondiente destino en el diccionario
        print(f"°{sigla} ({info_destino['nombre']}) - ${info_destino['precio']} ARS") # lo imprime
    #ingresa por teclado las siglas del destino que quiere reservar. Lo pongo con mayusculas para que convierta lo que ingrese a mayusc
    destino_seleccionado_sigla = input("Ingrese siglas del destino a consultar precio (o 'SALIR' para volver): ").upper()

    if destino_seleccionado_sigla == 'SALIR':
        return #salgo al menu principal

    if destino_seleccionado_sigla in destinos_disponibles:  #verifico que la sigla ingresada este en mi diccionario 
        info_destino_elegido = destinos_disponibles[destino_seleccionado_sigla]  #guardo en esta variable los datos tipo lista del destino que selecciono
        preciovuelo_elegido = info_destino_elegido['precio']  #en esta variable guardo el valor del precio que busco en la lista de info anterior
        print(f"El costo de su viaje a {info_destino_elegido['nombre']} es de ${preciovuelo_elegido} ARS") #muestro los datos recolectados

        confirmacion_reserva = input("Ingrese Y para confirmar el boleto, ingrese N para cancelar la operación: ").upper() #variable para ingresar y confirmar la reserva
        #si confirma la reserva le pide ingresar una fecha y genero una variable en NONE para luego llenarlo con el de la reserva
        if confirmacion_reserva == 'Y':
            fecha_ida_reserva = input("Ingrese la fecha de ida para su reserva (DD-MM-AAAA): ")
            id_cliente_asociado_reserva = None
            
            if clientes_registrados:  #si hay lista disponible
                print("\nPara esta reserva, asocie un cliente existente:")
                ver_clientes_registrados()   #llamo la funcion que recorre la lista de registro de clientes y los muestra
                #ingreso por teclado id o cuit a buscar y llamo la funcion buscar cliente dandole el valor de la busqueda a cliente_asociado_encotnrado
                cliente_id_o_cuit_input = input("Ingrese el ID o CUIT del cliente para esta reserva (o deje en blanco para no asociar ahora): ")
                cliente_asociado_encontrado = buscar_cliente_por_id_o_cuit(cliente_id_o_cuit_input) #guarda en esta variable la info de la lista de registros
                if cliente_asociado_encontrado: #si la funcion encuentra el cliente con la funcion anterior, guarda el id 
                                                #en la siguiente variable antes definida como none 
                    id_cliente_asociado_reserva = cliente_asociado_encontrado['id_cliente']
                    print(f"Reserva asociada al cliente: {cliente_asociado_encontrado['razonsocial_cliente']}.") #muestra de la info de lista la posicicion del diccionario razoncliente
                else:
                    print("Cliente no encontrado o no se asoció cliente a la reserva en este momento.") 
            else:
                print("No hay clientes registrados. Cree uno antes de asociar a la reserva.")

            id_reserva = obtener_siguiente_id(reservas_pendientes, 'id_reserva') #Llamo a la funcion que incrementa el id reserva y lo guardo en id_reserva
            #creo un diccionario y guardo los datos ingresados anteriormente
            nueva_reserva = {
                'id_reserva': id_reserva,      #generado con la funcion obtener id 
                'destino_sigla': destino_seleccionado_sigla,
                'destino_nombre': info_destino_elegido['nombre'],
                'preciovuelo': preciovuelo_elegido,
                'fecha_ida': fecha_ida_reserva,
                'id_cliente_asociado': id_cliente_asociado_reserva
            }
            reservas_pendientes.append(nueva_reserva)    #guardo cada registro en la lista de reservas pendientes
            print("\n--- ¡Boleto reservado! ---")
            print("Por favor, diríjase a '3. Gestionar Ventas' para completar la compra.") #termino y muestro los datos que guarde en el diccionario
            print(f"Reserva ID: {nueva_reserva['id_reserva']} para: {nueva_reserva['destino_nombre']} el {nueva_reserva['fecha_ida']} por ${nueva_reserva['preciovuelo']} ARS")

#si no confirma la reserva
        elif confirmacion_reserva == 'N':
            print("Operación de reserva cancelada.")
#si no selecciona ni S ni N
        else:
            print("Respuesta no válida.")
#si no ingresa bien las siglas del destino
    else:
        print("Destino no reconocido o no disponible.")
    pausa_sistema()  #Pausamos para que el usuario pueda leer

