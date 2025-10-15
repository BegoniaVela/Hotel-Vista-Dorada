import os

class Cliente():
    def __init__(self, DNI, nombre, apellido, celular=""):
        self.__DNI = DNI
        self.__nombre = nombre
        self.__apellido = apellido
        self.__celular = celular

    def getDNI(self):
        return self.__DNI
    
    def getNombre(self):
        return self.__nombre
    
    def getApellido(self):
        return self.__apellido
    
    def getCelular(self):
        return self.__celular


class Reserva():
    def __init__(self, habitacion, fecha, diasDuracion, costo):
        self.__habitacion = habitacion
        self.__fecha = fecha
        self.__diasDuracion = diasDuracion
        self.__costo = costo
        self.__pagado = False
        self.__consumos = []

    def CostoTotal(self):
        return self.__costo * self.__diasDuracion
    
    def marcarPagado(self):
        self.__pagado = True
    
    def estaPagado(self):
        return self.__pagado
    
    def agregarConsumo(self, nombre, precio, cantidad=1):
        self.__consumos.append({"nombre": nombre, "precio": precio, "cantidad": cantidad})
    
    def getConsumos(self):
        return self.__consumos
    
    def totalConsumos(self):
        total = 0
        for consumo in self.__consumos:
            total += consumo["precio"] * consumo["cantidad"]
        return total


class Reservacion():
    def __init__(self):
        self.__clientes = []
        self.__reservas = []

    def agregarReservacion(self, cliente, reserva):
        self.__clientes.append(cliente)
        self.__reservas.append(reserva)
    
    def buscarReservaPorDNI(self, DNI):
        for i in range(len(self.__clientes)):
            if self.__clientes[i].getDNI() == DNI:
                return self.__clientes[i], self.__reservas[i]
        return None, None


# Instancia global
sistema = Reservacion()


def clear():
    if os.name == 'nt':
        _ = os.system('cls')
    else:
        _ = os.system('clear')


def GenerarDatosPrueba():
    # Persona 1: Daniel Zotelo
    reservaDaniel = Reserva(14, "25/10/25", 5, 100)
    reservaDaniel.agregarConsumo("Lavanderia", 20, 1)
    reservaDaniel.agregarConsumo("Agua", 4, 2)
    reservaDaniel.agregarConsumo("Vino", 30, 2)
    sistema.agregarReservacion(
        Cliente("72365278", "Daniel", "Zotelo", "922173481"),
        reservaDaniel
    )
    
    # Persona 2: Maria Gonzales
    reservaMaria = Reserva(10, "26/10/25", 3, 120)
    reservaMaria.agregarConsumo("Lavanderia", 20, 1)
    reservaMaria.agregarConsumo("Gaseosa", 6, 3)
    reservaMaria.agregarConsumo("Cifrut", 6, 2)
    sistema.agregarReservacion(
        Cliente("45678912", "Maria", "Gonzales", "987654321"),
        reservaMaria
    )
    
    # Persona 3: Carlos Ramirez
    reservaCarlos = Reserva(5, "27/10/25", 2, 80)
    reservaCarlos.agregarConsumo("Lavanderia", 20, 1)
    reservaCarlos.agregarConsumo("Agua", 4, 4)
    reservaCarlos.agregarConsumo("Vino", 30, 1)
    sistema.agregarReservacion(
        Cliente("11223344", "Carlos", "Ramirez", "912345678"),
        reservaCarlos
    )


# ========== MENU CAJERO ==========
def mostrarMenuCajero():
    print("""
--------MENU CAJERO--------
    
    Elija una opción:
\t1. Pagar Reserva
\t2. Check Out
\t3. Regresar al menú general
""")


def pagarReserva():
    clear()
    print("""
--------MENU CAJERO--------
    Pagar Reserva:""")
    dni = input("\tIngresar DNI: ").strip()
    
    cliente, reserva = sistema.buscarReservaPorDNI(dni)
    
    if cliente is None:
        print("\n\tNo se encontró ninguna reserva con ese DNI")
        input("\n\tPresione ENTER para volver al menú 'Cajero'... ")
        menuCajero()
        return
    
    if reserva.estaPagado():
        print("\n\tEsta reserva ya ha sido pagada")
        input("\n\tPresione ENTER para volver al menú 'Cajero'... ")
        menuCajero()
        return
    
    # Mostrar información del huésped
    clear()
    print("""
--------MENU CAJERO--------
    Pagar Reserva:
\tHuésped consultado:""")
    print(f"\t    Nombre: {cliente.getNombre()} {cliente.getApellido()}")
    print(f"\t    DNI: {cliente.getDNI()}")
    print(f"\t    Numero de celular: {cliente.getCelular()}")
    precio = reserva.CostoTotal()
    print(f"\t    Precio Reserva: s/ {precio}")
    
    metodo = input(f"\t    Proceder a pagar(Tarjeta / Efectivo): ").strip().lower()
    
    # Calcular precio final con comisión del 5%
    comision = precio * 0.05
    precioFinal = int(precio + comision)
    
    clear()
    print("""
--------MENU CAJERO--------
    Pagar Reserva:
\tPrecio Actualizado(5% comision): s/""", precioFinal)
    print("""    
\tPago Realizado: Si""")
    
    reserva.marcarPagado()
    
    print("""
--------MENU CAJERO--------
    Pagar Reserva:
\tRESERVA CANCELADA""")
    
    input("\n\tPresione ENTER para volver al menú 'Cajero'... ")
    menuCajero()


def checkOutCajero():
    clear()
    print("""
--------MENU CAJERO--------
    Check Out:""")
    dni = input("\t    Ingresar DNI: ").strip()
    
    cliente, reserva = sistema.buscarReservaPorDNI(dni)
    
    if cliente is None:
        print("\n\t    No se encontró ninguna reserva con ese DNI")
        input("\n\tPresione ENTER para volver al menú 'Cajero'... ")
        menuCajero()
        return
    
    # Mostrar resumen
    clear()
    print("""
--------MENU CAJERO--------
    Check Out:
\t    Resumen:""")
    print(f"\t\tNombre: {cliente.getNombre()} {cliente.getApellido()}")
    print(f"\t\tDNI: {cliente.getDNI()}")
    
    # Mostrar consumos
    for consumo in reserva.getConsumos():
        if consumo["cantidad"] > 1:
            print(f"\t\t    - {consumo['nombre']}(s/ {consumo['precio']}) : {consumo['cantidad']}")
        else:
            print(f"\t\t    - {consumo['nombre']}: s/ {consumo['precio']}")
    
    totalConsumos = reserva.totalConsumos()
    print(f"\t\t    Total a pagar por consumos : s/ {totalConsumos}")
    
    metodo = input("\t\t    Proceder a pagar(Tarjeta / Efectivo) : ").strip().lower()
    
    # Calcular precio final con comisión del 5%
    comision = totalConsumos * 0.05
    precioFinal = totalConsumos + comision
    
    clear()
    print("""
--------MENU CAJERO--------
    Check Out:
\t    Precio Actualizado(5% comision) : s/""", precioFinal)
    print("\t    Pago Realizado: Si")
    
    print("""
--------MENU CAJERO--------
    Check Out:
\t    CONSUMOS CANCELADOS""")
    
    input("\n\tPresione ENTER para volver al menú 'Cajero'... ")
    menuCajero()


def ejecutarMenuCajero():
    opcion = input("Seleccione una opción (1-3): ").strip()
    
    if opcion == "1":
        pagarReserva()
    elif opcion == "2":
        checkOutCajero()
    elif opcion == "3":
        print("\nRegresando al menú principal...")
        return
    else:
        clear()
        mostrarMenuCajero()
        print("Valor enviado no válido")
        ejecutarMenuCajero()


def menuCajero():
    clear()
    mostrarMenuCajero()
    ejecutarMenuCajero()


# ========== PROGRAMA PRINCIPAL ==========
def main():
    GenerarDatosPrueba()
    menuCajero()


main()
