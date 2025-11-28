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
    print("\n")
    mostrar_memoria(Memoria)

    if NUEVO:
        print("\nProcesos en estado NUEVO:")
        for proceso in NUEVO:
            print(proceso)

    if LISTO:
        LISTO.sort(key=lambda p: p.tiempo_restante)
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
def cargar_procesos_desde_archivo(ruta_csv, nombre_archivo, lista_destino):
    import csv

    with open(ruta_csv, newline='', encoding="utf-8") as f:
        lector = csv.DictReader(f)

        # Normalizar encabezados
        encabezados_norm = {h.lower().replace(" ", "").replace("(", "").replace(")", ""): h for h in lector.fieldnames}

        # Convertir Columnas CSV
        def obtener(nombre_busqueda):
            nombre_busqueda = nombre_busqueda.lower()
            for k, original in encabezados_norm.items():
                if nombre_busqueda in k:
                    return original
            return None

        col_id = obtener("proceso") or obtener("id")
        col_arribo = obtener("arribo") or obtener("t_arribo")
        col_mem = obtener("memoria") or obtener("memoriak") or obtener("tamano")
        col_irrup = obtener("irrup") or obtener("burst") or obtener("tiempo_irrupcion")

        if not all([col_id, col_arribo, col_mem, col_irrup]):
            raise ValueError("No se pudieron reconocer las columnas del CSV.")

        for fila in lector:
            try:
                pid = fila[col_id]
                arr = int(fila[col_arribo])
                mem = int(fila[col_mem])
                irr = int(fila[col_irrup])

                nuevo_proceso = Proceso(pid, mem, arr, irr)
                lista_destino.append(nuevo_proceso)

            except Exception as e:
                print(f"Error leyendo fila {fila}: {e}")

