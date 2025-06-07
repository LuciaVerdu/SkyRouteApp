# main.py

# Importa las funciones de cada módulo
from .clientes import clientes_registrados 
from .clientes import submenu_gestionar_clientes
from .reservas import gestionar_destinos_y_reservas
from .ventas import submenu_gestionar_ventas
from .botonarrpentimiento import consultar_ventas_finalizadas, boton_arrepentimiento_venta





def main():
   
    while True:
        # Menú Principal
        print("\n--- Bienvenidos a SkyRoute - Sistema de Gestión de Pasajes ---")
        print("1. Gestionar Clientes")
        print("2. Gestionar Destinos")
        print("3. Gestionar Ventas")
        print("4. Consultar Ventas")
        print("5. Botón de Arrepentimiento")
        print("6. Salir")
        print("----------------------------------------------------------")
    #pido al client que ingrese una opcion por teclado del menu principal
        opcion_principal_elegida = input("Ingrese una opción: ")
#dependiendo que opcion elige llama a la funcion que corresponda-
        if opcion_principal_elegida == '1':
            submenu_gestionar_clientes()
        elif opcion_principal_elegida == '2':
            gestionar_destinos_y_reservas()
        elif opcion_principal_elegida == '3':
            submenu_gestionar_ventas()
        elif opcion_principal_elegida == '4':
            consultar_ventas_finalizadas()
        elif opcion_principal_elegida == '5':
            boton_arrepentimiento_venta()
        elif opcion_principal_elegida == '6':
            print("Saliendo de SkyRoute - Sistema de Gestión de Pasajes. ¡Vuelva pronto!")
            break
        else:
            print("Opción no válida. Intente de nuevo.")
            pausa_sistema()

# Punto de entrada del programa
if __name__ == "__main__":
    main()

