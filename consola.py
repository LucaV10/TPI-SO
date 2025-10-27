import csv
from procesos import Proceso

#Mostrar tabla de memoria
def mostrar_memoria(Memoria):   
    print("Tabla de Particiones de Memoria:\n")
    print("Nro | Tamanio | Proceso Asignado | Fragmentacion | Disponible")
    print("-------------------------------------------------------------")
  
    for p in Memoria: #El >3 y esas cosas son para darle formato mas lindo
        estado = "Si" if p['Disponible'] else "No"
        print(f"{p['NroParticion']:>3} | {p['TamanoParticion']:>6}K | "
              f"{str(p['ProcesoAsignado']):>15} | "
              f"{p['FragmentacionInterna']:>13}K | "
              f"{estado:>11}")

#Mostrar estado de los procesos
def mostrar_estado_procesos (Memoria, NUEVO, LISTO, LISTOSUSPENDIDO, EJECUCION, TERMINADO):
    #Muestra todo lo que se mostraba antes en el main
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
        for proceso in EJECUCION:
            print(proceso)

    if TERMINADO:
        print("\nProcesos en estado TERMINADO:")
        for proceso in TERMINADO:
            print(proceso)

#Cargar procesos desde un archivo
def cargar_procesos_desde_archivo(ruta,nombre_archivo, lista_nuevo):
    with open(ruta, encoding='utf-8') as nombre_archivo:
        lector = csv.DictReader(nombre_archivo)
        for fila in lector:
            p = Proceso(
                fila['Id'],
                int(fila['Tamano']),
                int(fila['TiempoArribo']),
                int(fila['TiempoIrrupcion'])
            )
            lista_nuevo.append(p)
    return lista_nuevo
