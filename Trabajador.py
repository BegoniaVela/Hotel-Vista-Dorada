class Trabajador():
    def __init__(self, codigo_trabajador , nombre_trabajador, dni_trabajador, telefono_trabajador):
        self.__codigo_trabajador = codigo_trabajador
        self.__no_trabajador = nombre_trabajador
        self.__dni_trabajador = dni_trabajador
        self.__telefono_trabajador = telefono_trabajador

    def __str__(self):
        return f"Codigo del Trabajador: {self.__codigo_trabajador} , Nombre: {self.__no_trabajador}, Numero de DNI: {self.__dni_trabajador}, Numero Telefonico: {self.__telefono_trabajador}"
    
    def CheckOut(self):
        pass
        