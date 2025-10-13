class Habitacion():
    def __init__(self,numero, precio):
        self.__numero = numero
        self.__precio = precio

    def __str__(self):
        return f"Habitacion Numero: {self.__numero} , Precio: {self.__precio}"
    
    def GetPrecio(self):
        return self.__precio
        
    