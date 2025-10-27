from procesos import Proceso

def gestor_memoria_bestfit(proceso, memoria, lista_listos):
    particion_elegida = None
    mejor_ajuste = float('inf')

    for particion in memoria:
        if particion['Disponible'] and particion['TamanoParticion'] >= proceso.tamano:
            diferencia = particion['TamanoParticion'] - proceso.tamano
            if diferencia < mejor_ajuste:
                mejor_ajuste = diferencia
                particion_elegida = particion

    if particion_elegida:
        particion_elegida['Disponible'] = False
        particion_elegida['ProcesoAsignado'] = proceso.id
        particion_elegida['FragmentacionInterna'] = mejor_ajuste
        proceso.particion_asignada = particion_elegida['NroParticion']
        proceso.estado = "Listo"
        lista_listos.append(proceso)
        print(f"|| Proceso {proceso.id} asignado a particion {particion_elegida['NroParticion']} ({particion_elegida['TamanoParticion']}K) ||", end='')
        return True

    print(f"|| No hay particion disponible para el proceso {proceso.id} ({proceso.tamano}K) pasa a Listo y Suspendido ||", end='')
    
    return False
    
