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
        self.particion_asignada = None
        self.estado = None
        
        #Valores para las estadisticas
        self.tiempo_llegada_listos = 0 #El tiempo en que entra a listo
        self.tiempo_finalizacion = 0 #Tiempo en el que termina
        
        self.tiempo_retorno = 0 #Es el tiempo (finalizacion - arribo)
        self.tiempo_espera = 0 #Es el tiempo (retorno - irrupcion)

        #Sirve para imprimir los procesos de manera mas facil
    def __str__(self):
        return f"[ID: {self.id} | Tam: {self.tamano}K | Arr: {self.ta} | Irr: {self.ti} | Res: {self.tiempo_restante} | Est: {self.estado}]"
