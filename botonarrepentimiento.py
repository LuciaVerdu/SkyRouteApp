#consultas de ventas y boton de arrepentimiento
from .gestiondatos import ventas_finalizadas # Importa la lista de ventas
from .funcionesutiles import pausa_sistema # Importa funciones de utilidad
def consultar_ventas_finalizadas(): #Muestra un listado de todas las ventas que han sido registradas.
    
    print("\n--- Consultar Ventas ---")
    if not ventas_finalizadas: #si esta vacia la lista de las ventas imprime los siguientes msjs
        print("No hay ventas registradas aún en el sistema.")
        print("Por favor, procese una reserva en '3. Gestionar Ventas' para registrar una venta.")
    else: #si no esta vacia la lista la muestra recorriendo cada n valor venta en la lista venta finalizadas
        print("Listado de Ventas Registradas:")
        for venta in ventas_finalizadas:
            print(f"\n--- Detalles de Venta ID: {venta['id_pasaje']} ---")
            print(f"Cliente: {venta['razonsocial_cliente']} (CUIT: {venta['cuit_cliente']})")
            print(f"Destino: {venta['destino']}")
            print(f"Precio: ${venta['precio']} ARS")
            print(f"Fecha de Venta: {venta['fecha_venta']}")
            print(f"Fecha de Vuelo: {venta['fecha_vuelo']}")
            print(f"Correo de Contacto: {venta['correo_cliente']}")
    pausa_sistema()

# --- Módulo de Botón de Arrepentimiento ---

def boton_arrepentimiento_venta(): #cancelar una venta ya finalizada, eliminándola del registro de la lista ventas finalizadas.
    print("\n--- Botón de Arrepentimiento ---")
    if not ventas_finalizadas: #si no existen datos de venta en la lista
        print("No hay ninguna venta registrada de la cual arrepentirse.")
        print("Para usar esta función, primero debe haber una venta procesada.")
        pausa_sistema() #pausa para leer error 
        return
#si existen valores en la lista
    print("\nVentas Registradas (para arrepentimiento):")
    for i, venta in enumerate(ventas_finalizadas):  #recorro la lista usando enumerate() es una función incorporada de Python.
                                                        #produce pares de datos: (índice, valor) i: recibe el índice,
                                                        #venta: recibe el valor del elemento de la lista en esa posición. 
                                                        #en este caso, reserva es el diccionario completo de una de las ventas finalizadas
    #muestro los datos que recorro en el for en cada posicion de la lista mostrando sus diccionarios 
    # (i+1) Le sumamos 1, porque si el usuario ve la posicion /indice 0 el lo reconoce como el 1 
        print(f"{i+1}. ID Venta: {venta['id_pasaje']}, Cliente: {venta['razonsocial_cliente']}, Destino: {venta['destino']}, Fecha Venta: {venta['fecha_venta']}")

    try:
        idx_venta_cancelar = int(input("Ingrese el NÚMERO de la venta a cancelar (arrepentirse): ")) - 1 
        #Pide al usuario que ingrese un número usamos int() para convertirlo a un número entero.
        # Le restamos 1, porque si el usuario ve "1." y lo elige, en la lista es el índice 0.
    
        if not (0 <= idx_venta_cancelar < len(ventas_finalizadas)): #veo si el id que ingrese el cliente esta fuera del rango de ventas finalizadas
            print("Número de venta inválido.")
            pausa_sistema() #pausa para leer error
            return #pide que ingrese otro numero
    except ValueError: #analizo si no ingresa un numero
        print("Entrada inválida. Por favor, ingrese un número.")
        pausa_sistema() #pausa para leer
        return #vuelve a pedir ingresar un numero

#si el ingreso fue correcto no ingresa al if ni al except y guarda
#en la variable venta a cancelar la info de la lista en ese id ingresado
    venta_a_cancelar = ventas_finalizadas[idx_venta_cancelar]
#Muestro los datos diccionario del id seleccionado y pregunto por teclado en la variable confirm arrepentimiento para confirmar la cancelacion
    print(f"La venta seleccionada (ID: {venta_a_cancelar['id_pasaje']}) es para {venta_a_cancelar['razonsocial_cliente']} con destino {venta_a_cancelar['destino']}.")
    confirmacion_arrepentimiento = input("¿Está seguro que desea cancelar esta venta? (S/N): ").upper()
#si ingresa que si, elimino de la lista ventas finalizadas con la funcion de python  pop, los datos del id ingresado 
    if confirmacion_arrepentimiento == 'S':
        ventas_finalizadas.pop(idx_venta_cancelar)
        print("¡Venta cancelada exitosamente! Los datos de la venta han sido eliminados.")
        print("Recuerde consultar las políticas de cancelación de vuelos.")
    elif confirmacion_arrepentimiento == 'N': # si ingresa que no, muestro el siguiente mensaje
        print("Operación de arrepentimiento cancelada.")
    else:
        print("Respuesta no válida.")
 #pausa para leer dependiendola opcion ingresada   
    pausa_sistema() 