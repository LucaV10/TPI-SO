def crear_memoria():
    tamanos = [100, 250, 150, 50]
    memoria = []

    for i in range(4):
        particion = {
            'NroParticion': i + 1,
            'TamanoParticion': tamanos[i],
            'FragmentacionInterna': 0,
            'ProcesoAsignado': None,
            'Disponible': True
        }

        if i == 0:
            particion['ProcesoAsignado'] = 'SO'
            particion['Disponible'] = False
        memoria.append(particion)
    return memoria


def mostrar_memoria(memoria):   
    print("Tabla de Particiones de Memoria:\n")
    print("Nro | Tamanio | Proceso Asignado | Fragmentacion | Disponible")
    print("-------------------------------------------------------------")
  
    for p in memoria: #El >3 y esas cosas son para darle formato mas lindo
        estado = "Si" if p['Disponible'] else "No"
        print(f"{p['NroParticion']:>3} | {p['TamanoParticion']:>6}K | "
              f"{str(p['ProcesoAsignado']):>15} | "
              f"{p['FragmentacionInterna']:>13}K | "
              f"{estado:>11}")
