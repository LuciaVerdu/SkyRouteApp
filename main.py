# main.py

# Importa las funciones de cada módulo
from .gestion_clientes import submenu_gestionar_clientes
from .gestion_pasajes import submenu_gestionar_destinos 
from .gestion_ventas import submenu_gestionar_ventas
from .botonarrepentimiento import consultar_ventas_finalizadas, boton_arrepentimiento_venta
from .funcionesutiles import pausa_sistema


def main():
    
    while True:
        # Menú Principal
        print("\n--- Bienvenidos a SkyRoute - Sistema de Gestión de Pasajes ---")
        print("1. Gestionar Clientes")
        print("2. Gestionar Destinos y Reservas") 
        print("3. Gestionar Ventas")
        print("4. Consultar Ventas")
        print("5. Botón de Arrepentimiento")
        print("6. Salir")
        print("----------------------------------------------------------")
#pido al usuario que ingrese una opcion por teclado del menu principal
        opcion_principal_elegida = input("Ingrese una opción: ")
#dependiendo que opcion elige llama a la funcion que corresponda-
        if opcion_principal_elegida == '1':
            submenu_gestionar_clientes()
        elif opcion_principal_elegida == '2':
            submenu_gestionar_destinos() 
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
