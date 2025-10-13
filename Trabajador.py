class Trabajador():
    def __init__(self, codigo_Trabajador , nombre_trabajador, dni_trabajador, telefono_trabajador):
        self.__codigo_Trabajador = codigo_Trabajador
        self.__no_trabajador = nombre_trabajador

    def __str__(self):
        return f"Habitacion Numero: {self.__codigo_Trabajador} , Precio: {self.__no_trabajador}"
    
    def GetPrecio(self):
        return self.__precio
        