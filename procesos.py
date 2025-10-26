#Procesos
class Proceso:
    #Representacion de los procesos
    def __init__(self, idproceso,tamano, ta, ti):
        #Valores iniciales de un proceso
        self.id = idproceso
        self.tamano = tamano
        self.ta = ta
        self.ti = ti

        #Valores para el control
        self.tiempo_restante = ti #Tiempo restante va a servir mucho para SRTF
        self.particion_asignada = 0
        self.estado = "Nuevo"
        
        #Valores para las estadisticas
        self.tiempo_llegada_listos = 0 #El tiempo en que entra a listo
        self.tiempo_finalizacion = 0 #Tiempo en el que termina
        
        self.tiempo_retorno = 0 #Es el tiempo (finalizacion - arribo)
        self.tiempo_espera = 0 #Es el tiempo (retorno - irrupcion)

        #Sirve para imprimir los procesos de manera mas facil
    
    def __str__(self):
        # Ajusta los números (2, 4, 10) según tus necesidades
        
        # {self.id: >2} -> ID alineado a la derecha en 2 espacios
        # {self.tamano: >4} -> Tamano alineado a la derecha en 4 espacios
        # {self.estado: <10} -> Estado alineado a la izquierda en 10 espacios
        return (f"| ID: {self.id: >3} | "
                f"Tam: {self.tamano: >4}K | "
                f"Arr: {self.ta: >2} | "
                f"Irr: {self.ti: >2} | "
                f"Res: {self.tiempo_restante: >2} | "
                f"Est: {self.estado: <10}|" )
