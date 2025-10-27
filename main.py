import csv
import os
import sys
import time
from procesos import Proceso
from memoria import crear_memoria
from planificador import gestor_memoria_bestfit
from consola import mostrar_estado_procesos, mostrar_memoria, cargar_procesos_desde_archivo


# Listas de estados
NUEVO, LISTO, EJECUCION, LISTOSUSPENDIDO, TERMINADO = [], [], [], [], []
GRAD_MULTIPROG = 0
#Definimos un reloj para ir mostrando los avances.
clk = 0

#Pavadas decorativas para la consola
os.system('cls')
print("Iniciando simulacion...\n")
time.sleep(1)
os.system('cls')

print(f"------| Tiempo actual del sistema |------\n"
      f"------------------| {clk} |------------------\n\n"
      f"        | Mensajes del sistema |        \n")

# Crear memoria
Memoria = crear_memoria()
mostrar_memoria(Memoria)

ruta_csv = os.path.dirname(__file__) + "\\data\\Procesos.csv" #Solo sirve para cargar la ruta del archivo de ejemplo

# Cargar procesos desde CSV
cargar_procesos_desde_archivo(ruta_csv, 'Procesos.csv', NUEVO)


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

        print(f"------| Tiempo actual del sistema |------\n"
              f"------------------| {clk} |------------------\n\n"
              f"        | Mensajes del sistema |        \n")
        
        # Planificación SRTF
        if EJECUCION:
            tiempo_restante_ejecucion = EJECUCION[0].tiempo_restante
            # Verificar si el proceso en ejecucion ha terminado
            if EJECUCION[0].tiempo_restante == 0:
                #CONTROL DE SRTF LISTO Y SUSPENDIDO
                pausa = True
                GRAD_MULTIPROG -= 1
                proceso_terminado = EJECUCION.pop(0)
                proceso_terminado.estado = "Terminado"
                
                for particion in Memoria:
                    if particion['NroParticion'] == proceso_terminado.particion_asignada:
                        particion['Disponible']= True
                        particion['ProcesoAsignado'] = None
                        particion['FragmentacionInterna'] = 0
                proceso_terminado.particion_asignada = None
                TERMINADO.append(proceso_terminado)
                print(f"||El proceso {proceso_terminado.id} ha terminado su ejecucion||")
        else:
            tiempo_restante_ejecucion = float('inf')

        proceso_elegido = None
        if not EJECUCION:
            if LISTOSUSPENDIDO:
                tiempo_menor = float('inf')
                for p in LISTOSUSPENDIDO:
                    if p.tiempo_restante < tiempo_menor:
                        proceso_elegido = p
                        tiempo_menor = p.tiempo_restante
                if GRAD_MULTIPROG < 5:
                    if proceso_elegido.ta <= clk: # Comprobar si este proceso ya llegó
                        if gestor_memoria_bestfit(proceso_elegido, Memoria, LISTO):
                            LISTOSUSPENDIDO.remove(proceso_elegido) # Se asignó, sacarlo de NUEVO
                            print("|| El proceso pasa al estado LISTO ||")
                        pausa = True

        proceso_elegido = None
        for p in LISTO:
            if p.tiempo_restante < tiempo_restante_ejecucion:
                proceso_elegido = p
                tiempo_restante_ejecucion = p.tiempo_restante

        if proceso_elegido:
            pausa = True
            if EJECUCION:
                print(f"||El proceso {proceso_elegido.id} interrumpio el proceso {EJECUCION[0].id}||")
                proceso_elegido.estado = "Ejecucion"
                EJECUCION[0].estado = "Listo"
                LISTO.append(EJECUCION.pop(0))
                EJECUCION.append(proceso_elegido)
                LISTO.remove(proceso_elegido)
            else:
                proceso_elegido.estado = "Ejecucion"
                EJECUCION.append(proceso_elegido)
                LISTO.remove(proceso_elegido)
        
        if EJECUCION:
            EJECUCION[0].tiempo_restante -= 1

        # Asignar procesos con Best-Fit
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
        
        #Mostrar estado procesos
        mostrar_estado_procesos( Memoria, NUEVO, LISTO, LISTOSUSPENDIDO, EJECUCION, TERMINADO)

        if pausa:
            input("\nPresione Enter para continuar...")
            pausa = False 

        # Avanzar el reloj
        clk += 1
        time.sleep(1.25)
        os.system('cls')
    
except KeyboardInterrupt:
    print("\nSimulacion terminada por el usuario.")
