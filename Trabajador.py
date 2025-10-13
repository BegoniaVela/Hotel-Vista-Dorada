class Trabajador:
    def __init__(self, codigo_trabajador, nombre_trabajador, dni_trabajador, telefono_trabajador):
        self.__codigo_trabajador = codigo_trabajador
        self.__nombre_trabajador = nombre_trabajador
        self.__dni_trabajador = dni_trabajador
        self.__telefono_trabajador = telefono_trabajador

    def __str__(self):
        return (
            f"Código del Trabajador: {self.__codigo_trabajador}, "
            f"Nombre: {self.__nombre_trabajador}, "
            f"DNI: {self.__dni_trabajador}, "
            f"Teléfono: {self.__telefono_trabajador}"
        )

    def check_out(self):
        # Aquí más adelante se podría registrar salida, hora o actualizar estado
        pass


        
