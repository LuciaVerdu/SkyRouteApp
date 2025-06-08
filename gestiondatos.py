# data.py
#defino las tres listas principales que contendran los diccionarios de datos de cada uno de los modulos
clientes_registrados = []
reservas_pendientes = []
ventas_finalizadas = []


#diccionario de destinos 
destinos_disponibles = {
    'BRC': {'nombre': 'San Carlos de Bariloche', 'precio': 141863},
    'MDZA': {'nombre': 'Mendoza', 'precio': 62046},
    'BSAS': {'nombre': 'Buenos Aires', 'precio': 44341},
    'SLTA': {'nombre': 'Salta', 'precio': 80163},
    'NEUQ': {'nombre': 'Neuquén', 'precio': 89854},
    'COM RIV': {'nombre': 'Comodoro Rivadavia', 'precio': 171067},
    'SANTIAGO': {'nombre': 'Santiago de Chile', 'precio': 332378},
    'JUJUY': {'nombre': 'San Salvador de Jujuy', 'precio': 133271},
    'LIMA': {'nombre': 'Lima, Perú', 'precio': 616715}
}

# Los IDs ahora deberían manejarse dentro de cada función o pasarse
# No necesariamente necesitas que sean globales aquí si cada función los gestiona al crearlos.
# Pero los dejamos para mantener la coherencia con tu diseño original si así lo prefieres.
# Una alternativa más robusta sería leer el último ID de la lista cada vez.
id_cliente = 0
id_reserva = 0
id_venta = 0