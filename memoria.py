def crear_memoria():
    tamanos = [100, 250, 150, 50]
    memoria = []
    dir_inicio = [0, 100, 350, 500]
    
    for i in range(4):
        particion = {
            'NroParticion': i + 1,
            'DirInicio': dir_inicio[i],
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


def tamano_valido(proceso, particiones): #Funcion para verificar si un proceso puede en algun instante de tiempo entrar a memoria, es decir que si alguna particion tiene mayor tamaño que el
    for part in particiones: 
        if part["TamanoParticion"] >= getattr(proceso, "tamano", getattr(proceso, "tamaño", 0)):
            return True
    return False