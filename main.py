import os
import random

class Cliente():
    def __init__(self,DNI, nombre,apellido):
        self.__DNI = DNI
        self.__nombre = nombre
        self.__apellido = apellido

    def __str__(self):
        return f"DNI: {self.__DNI}, Nombre: {self.__nombre}, Apellido: {self.__apellido} "
    
    def getDNI(self):
        return self.__DNI


class Reserva():
    def __init__(self,habitacion,fecha, diasDuracion, costo):
        self.__habitacion = habitacion
        self.__fecha = fecha
        self.__diasDuracion = diasDuracion
        self.__costo = costo

    def DondeCuando(self):
        return f"Habitacion: {self.__habitacion}, Fecha :{self.__fecha}"

    def CostoTotal(self):
        return self.__costo * self.__diasDuracion
    
    def __str__(self):
        return f"{self.DondeCuando()} - Costo: {self.CostoTotal()}"

class Reservacion():
    def __init__(self):
        self.__cliente = []
        self.__reserva = []

    def agregarReservacion(self,cliente , reserva): #Generar
        self.__cliente.append(cliente)
        self.__reserva.append(reserva)

    def MostrarReservaciones(self): #Historial
        if len(self.__cliente) > 0:
            for c in range(len(self.__cliente)):
                print(f"{self.__cliente[c]} - {self.__reserva[c]} \n")
        else:
            print("no se ha hecho ninguna reserva")

    def dn(self):
        self.__cliente[0].getDNI()

    def ConsultarReservaciones(self,DNI): #Consultar

        if len(self.__cliente) > 0:
            a = False
            for c in range(len(self.__cliente)):
                if self.__cliente[c].getDNI() == DNI:
                    print(f"{self.__cliente[c]} - {self.__reserva[c]}")
                    a = True
                    break  
            if a == False:
                print("no se ha hecho ninguna reserva")
        else:
            print("no se ha hecho ninguna reserva")

res = Reservacion()
habitacionesDisponibles = [14,10,5]
Precios = [120,100,80]

def GenerarPrueba():
    
    #(DNI - Nombre - Apellido) - (numero de habitacion - FechaDeLaReservacion - CuantosDias - CostoPorDia)
    res.agregarReservacion(Cliente("1234","nombre1","apellido1"),Reserva(12,"27/09/25",2,120))
    res.agregarReservacion(Cliente("1235","nombre2","apellido2"),Reserva(13,"26/09/25",1,120))
    res.agregarReservacion(Cliente("1236","nombre3","apellido3"),Reserva(14,"25/09/25",3,120))
    res.MostrarReservaciones()
    print("-----------------")
    

def clear():
    # For Windows
    if os.name == 'nt':
        _ = os.system('cls')
    # For macOS and Linux
    else:
        _ = os.system('clear')

def UImenu():
    
    print("""
--------MENU RECEPCIONISTA---------
    Elija una opcion:
        1. Consultar
        2. Reservar
        3. Check out 
        4. Historial
        5. Cancelar
        
""")
#1
def UIconsulta():
    print("""
--------MENU RECEPCIONISTA---------
-------------CONSULTA--------------
    Ingrese el DNI: 
        
""")

def Exconsulta():
    dni = input("DNI: ").strip()
    res.ConsultarReservaciones(dni)

    continuar = input("presione enter para volver... ").strip()
    if continuar == "":
        inicio()


#2
def UIgenerar():
    print("""
    --------MENU RECEPCIONISTA---------
    -------------RESERVA---------------     
    """)

def Exgenerar():
    #(DNI - Nombre - Apellido) - (numero de habitacion - FechaDeLaReservacion - CuantosDias - CostoPorDia)

    dni = input("DNI: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    fecha = input("Fecha: ").strip()
    duracion = input("Dias: ").strip()
    print(f"precios de las habitaciones : {Precios}")
    precio = input("Precio: ").strip()
    print(f"Habitaciones disponibles : {habitacionesDisponibles}")
    numeroHabitacion = input("Numero de habitacion: ").strip()
    habitacionesDisponibles.remove(int(numeroHabitacion))
    res.agregarReservacion(Cliente(dni,nombre,apellido),Reserva(int(numeroHabitacion),fecha,int(duracion),int(precio)))
    print("Se a generado correctamente")
    continuar = input("presione enter para volver... ").strip()
    if continuar == "":
        inicio()

#3
def UICheckOut():
    print("""
    --------MENU RECEPCIONISTA---------
    ------------Check Out--------------   
          
        Se envio personal de limpieza a revisar la habitación  
          
    """)

    estado = random.randint(1, 2)
    pedidos = random.randint(1, 2)

    if estado == 1:
        print("el estado de la habitacion esta en orden")
    elif estado ==2:
        print("el estado de la habitacion esta en desorden")

    if estado == 1:
        print("el huesped a pedido algunas bebidas")
    elif estado ==2:
        print("el huesped no a pedido nada")


def ExCheckOut():
    confirm = input("¿Se añadira algo? Y / N: ").strip()
    if confirm == "N":
        print("Se confirmo el Chek3Out, no se añadira nada")
        continuar = input("presione enter para volver... ").strip()
        if continuar == "":
            inicio()

    elif confirm == "Y":
        print("Se confirmo el Chek3Out, se añadiran cargos")
        continuar = input("presione enter para volver... ").strip()
        if continuar == "":
            inicio()

    else:
        clear()
        UICheckOut()
        print("valor enviado no valido")
        ExCheckOut()


#4
def UIHistorial():
    print("\n===== Historial =====")
    res.MostrarReservaciones()

    continuar = input("presione enter para volver... ").strip()
    if continuar == "":
        inicio()


def Exmenu():
    opcion = input("Seleccione una opción (1-5): ").strip()
    
    if opcion == "1":
        clear()
        UIconsulta()
        Exconsulta()

    elif opcion == "2":
        clear()
        UIgenerar()
        Exgenerar()

    elif opcion == "3":
        clear()
        UICheckOut()
        ExCheckOut()

    elif opcion == "4":
        clear()
        UIHistorial()

    elif opcion == "5":
        clear()

    else:
        clear()
        UImenu()
        print("valor enviado no valido")
        Exmenu()

def inicio():
    clear()
    UImenu()
    Exmenu()


def main():
    GenerarPrueba()
    inicio()

main()