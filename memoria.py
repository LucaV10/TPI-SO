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


