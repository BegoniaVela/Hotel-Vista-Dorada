class Habitacion:
    def __init__(self, numero_habitacion, precio_noche):
        self.__numero_habitacion = numero_habitacion
        self.__precio_noche = precio_noche

    def __str__(self):
        return f"Habitación N°: {self.__numero_habitacion}, Precio por noche: S/ {self.__precio_noche}"

    def get_precio(self):
        return self.__precio_noche
    
