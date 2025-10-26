import csv
import os
import sys
import time
from procesos import Proceso
from memoria import crear_memoria, mostrar_memoria
from planificador import gestor_memoria_bestfit

# Listas de estados
NUEVO, LISTO, EJECUCION, LISTOSUSPENDIDO, TERMINADO = [], [], [], [], []
GRAD_MULTIPROG = 0

#Pavadas decorativas para la consola
os.system('cls')
print("Iniciando simulacion...\n")
time.sleep(1)
os.system('cls')

#Definimos un reloj para ir mostrando los avances.
clk = 0
print(f"Tiempo actual del sistema: {clk}\n")

# Crear memoria
Memoria = crear_memoria()
mostrar_memoria(Memoria)

ruta_csv = os.path.dirname(__file__) + "\\data\\Procesos.csv" #Solo sirve para cargar la ruta del archivo de ejemplo

# Cargar procesos desde CSV
with open(ruta_csv, encoding='utf-8') as Procesos:
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

#Decorativos
input("\nPresione Enter para asignar los procesos a memoria...")
os.system('cls')

#Bucle principal de la simulacion
ejecutando = True
pausa = False

try:
    while ejecutando:
        print(f"Tiempo actual del sistema: {clk}\n")
        
        # Asignar procesos con Best-Fit
        proceso = NUEVO[0]
        print("Asignando procesos a memoria...\n")
        # Iterar sobre una COPIA de NUEVO (con [:]), porque la vamos a modificar
        for proceso in NUEVO[:]: # Va a funcionar si es que la cola de listo no esta ordenada por tiempo de arribo
            if GRAD_MULTIPROG < 5:
                if proceso.ta <= clk: # Comprobar si este proceso ya llegó
                    if gestor_memoria_bestfit(proceso, Memoria, LISTO):
                        NUEVO.remove(proceso) # Se asignó, sacarlo de NUEVO
                    else:
                        # No hay memoria para este proceso que ya llegó
                        proceso.estado = "Listo y suspendido"
                        LISTOSUSPENDIDO.append(proceso)
                        NUEVO.remove(proceso)
                    pausa = True
                    GRAD_MULTIPROG = GRAD_MULTIPROG + 1 # Incrementar cupo
            else:
                # Ya no hay cupo de multiprogramación, dejar de revisar
                break

        proceso_elegido = None
        # Planificación SRTF
        
        if EJECUCION:
            tiempo_restante_ejecucion = EJECUCION[0].tiempo_restante
        else:
            tiempo_restante_ejecucion = float('inf')

        for p in LISTO:
            if p.tiempo_restante < tiempo_restante_ejecucion:
                proceso_elegido = p
                tiempo_restante_ejecucion = p.tiempo_restante
        if proceso_elegido:
            pausa = True
            if EJECUCION:
                print(f"\n||El proceso {proceso_elegido.id} interrumpio el proceso {EJECUCION[0].id}||")
                proceso_elegido.estado = "Ejecucion"
                EJECUCION[0].estado = "Listo"
                LISTO.append(EJECUCION.pop(0))
                EJECUCION.append(proceso_elegido)
                LISTO.remove(proceso_elegido)
            else:
                proceso_elegido.estado = "Ejecucion"
                EJECUCION.append(proceso_elegido)
                LISTO.remove(proceso_elegido)
        
        # Mostrar estado procesos
        print("\n")
        mostrar_memoria(Memoria)

        if NUEVO:
            print("\nProcesos en estado NUEVO:")
            for proceso in NUEVO:
                print(proceso)

        if LISTO:
            print("\nProcesos en estado LISTO:")
            for proceso in LISTO:
                print(proceso)
            
        if LISTOSUSPENDIDO:
            print("\nProcesos en estado LISTO y SUSPENDIDO:")
            for proceso in LISTOSUSPENDIDO:
                print(proceso)

        if EJECUCION:
            print("\nProcesos en estado EJECUCION:")
            # Se reduce el tiempo restante del proceso en ejecucion
            
            EJECUCION[0].tiempo_restante -= 1
            for proceso in EJECUCION:
                print(proceso)

        if TERMINADO:
            print("\nProcesos en estado TERMINADO:")
            for proceso in TERMINADO:
                print(proceso)

        if EJECUCION:
            # Verificar si el proceso en ejecucion ha terminado
            if EJECUCION[0].tiempo_restante == 0:
                pausa = True
                GRAD_MULTIPROG -= 1
                proceso_terminado = EJECUCION.pop(0)
                proceso_terminado.estado = "Terminado"
                
                for particion in Memoria:
                    if particion['NroParticion'] == proceso_terminado.particion_asignada:
                        particion['Disponible']= True
                        particion['ProcesoAsignado'] = None
                        particion['FragmentacionInterna'] = 0

                proceso_terminado.particion_asignada = 0
                TERMINADO.append(proceso_terminado)
                print(f"\n||El proceso {proceso_terminado.id} ha terminado su ejecucion||")

        if pausa:
            input("\nPresione Enter para continuar...")
            pausa = False 

        # Avanzar el reloj
        clk += 1
        time.sleep(1.25)
        os.system('cls')
    
except KeyboardInterrupt:
    print("\nSimulacion terminada por el usuario.")


