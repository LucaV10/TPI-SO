import csv
import os
from procesos import Proceso
from memoria import crear_memoria, mostrar_memoria
from planificador import gestor_memoria_bestfit

# Listas de estados
NUEVO, LISTO, EJECUCION, SUSPENDIDO, TERMINADO = [], [], [], [], []

# Crear memoria
Memoria = crear_memoria()
mostrar_memoria(Memoria)

ruta_csv = os.path.dirname(__file__) + "\\data\\Procesos.csv" #Solo sirve para cargar la ruta del archivo de ejemplo

# Cargar procesos desde CSV
with open(ruta_csv) as Procesos:
    lector = csv.DictReader(Procesos)
    for fila in lector:
        p = Proceso(
            fila['Id'],
            int(fila['Tamano']),
            int(fila['TiempoArribo']),
            int(fila['TiempoIrrupcion'])
        )
        NUEVO.append(p)

print("\nProcesos en estado NUEVO:")
for p in NUEVO:
    print(p)

# Asignar procesos con Best-Fit
print("\nAsignando procesos a memoria...\n")
for proceso in NUEVO[:]:  # usar copia para evitar problemas al modificar la lista
    if gestor_memoria_bestfit(proceso, Memoria, LISTO):
        NUEVO.remove(proceso)
