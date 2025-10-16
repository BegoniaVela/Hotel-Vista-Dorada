import os
from datetime import datetime, timedelta
import pandas as pd

ROOM_SERVICE_TARIFA = 50.0  # fijo
DATE_FMT = "%d/%m/%Y"

#-----------
# Utilidades
#-----------

class OpcionInvalida(Exception):
    pass

def clear():
    os.system("cls" if os.name == "nt" else "clear")


def pausar():
    input("\nPresione ENTER para volver al menú...")


def parse_fecha(s: str) -> datetime:
    return datetime.strptime(s.strip(), DATE_FMT)


def rango_se_solapa(a_inicio, a_fin, b_inicio, b_fin) -> bool:
    # hay solape si el inicio A es <= fin B y el inicio B es <= fin A
    return a_inicio <= b_fin and b_inicio <= a_fin

def proximo_id_registro(registros) -> int:
    if not registros:
        return 1
    return max(int(r["ID_Registro"]) for r in registros) + 1
#-----------
#MODELOS
#-----------


# -------- CLIENTE --------
class Cliente:
    def __init__(self, nombre, apellido, dni, celular):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__celular = celular

    @property
    def nombre(self):
        return self.__nombre

    @property
    def apellido(self):
        return self.__apellido

    @property
    def dni(self):
        return self.__dni

    @property
    def celular(self):
        return self.__celular

    def __str__(self):
        return (f"""
        Nombre: {self.__nombre}
        Apellido: {self.__apellido}
        DNI:{self.__dni}
        Celular:{self.__celular}""")


# -------- HABITACION --------
class Habitacion:
    def __init__(self, id_habitacion, categoria, precio_noche):
        self.__id_habitacion = id_habitacion
        self.__categoria = categoria
        self.__precio_noche = float(precio_noche)

    @property
    def id_habitacion(self):
        return self.__id_habitacion

    @property
    def categoria(self):
        return self.__categoria

    @property
    def precio_noche(self):
        return self.__precio_noche

    def __str__(self):
        return f"""{self.__id_habitacion} ({self.__categoria}) - S/ {self.__precio_noche:.2f}"""


# -------- RESERVA --------
class Reserva:
    def __init__(self, cliente: Cliente, habitacion: Habitacion,
                 fecha_entrada: datetime, dias: int,
                 consumo_minibar: float = 0.0, consumo_room_service: float = 0.0, late_checkout: int = 0):
        self.__cliente = cliente
        self.__habitacion = habitacion
        self.__fecha_entrada = fecha_entrada
        self.__dias = int(dias)
        self.__fecha_salida = fecha_entrada + timedelta(days=self.__dias)
        self.__consumo_minibar = float(consumo_minibar)
        self.__consumo_room_service = float(consumo_room_service)
        self.__late_checkout = int(late_checkout)  # 1 sí / 0 no
        self.__estado = "Confirmada" #Se podra actualizar a Activa, Finalizada o Cancelada
    @property
    def cliente(self):
        return self.__cliente

    @property
    def fecha_entrada(self):
        return self.__fecha_entrada

    @property
    def fecha_salida(self):
        return self.__fecha_salida

    @property
    def habitacion(self):
        return self.__habitacion

    @property
    def estado(self):
        return self.__estado
    @estado.setter
    def estado(self,valor):
        self.__estado = valor

    @property
    def dias(self):
        return self.__dias

    @property
    def total_hospedaje(self) -> float:
        return self.__habitacion.precio_noche * self.__dias

    @property
    def cargo_late_checkout(self) -> float:
        # equivalente a 4 horas: precio/24*4 = precio/6
        return (self.__habitacion.precio_noche / 6.0) if self.__late_checkout == 1 else 0.0

    @property
    def total_a_pagar(self) -> float:
        return self.total_hospedaje + self.__consumo_minibar + self.__consumo_room_service + self.cargo_late_checkout

    def resumen(self) -> str:
        return (
            "--------MENU RECEPCIONISTA--------\n"
            "Reserva generada:\n"
            f"  Nombre: {self.__cliente.nombre} {self.__cliente.apellido}\n"
            f"  DNI: {self.__cliente.dni}\n"
            f"  Numero de celular: {self.__cliente.celular or '-'}\n"
            f"  Cantidad de invitados extra: 0\n"
            f"  Fecha Ingreso: {self.__fecha_entrada.strftime(DATE_FMT)}\n"
            f"  Fecha salida: {self.__fecha_salida.strftime(DATE_FMT)}\n"
            f"  Cantidad de dias: {self.__dias}\n"
            f"  Precio: {int(self.__habitacion.precio_noche)}\n"
            f"  Habitacion: {self.__habitacion.id_habitacion}\n"
            f"  Precio a cancelar: s/ {int(self.total_a_pagar)}\n"
            f"  Estado : {self.__estado}\n"
        )

# -------- GESTION DE LAS HABITACIONES --------
class GestionHotel:
    def __init__(self):
        self.__habitaciones = [
            Habitacion("G201", "Simple", 80),
            Habitacion("G202", "Matrimonial",120),
            Habitacion("G203", "Estandar",100),
            Habitacion("G204", "Matrimonial",120),
            Habitacion("G205", "Estandar",100),
            Habitacion("G206", "Estandar",100),
            Habitacion("G207", "Simple", 80),
            Habitacion("G208", "Simple", 80),
            Habitacion("G209", "Matrimonial", 120),
        ]

        self.__categoria_precios = {
            h.categoria: h.precio_noche for h in self.__habitaciones
        }

        self.__reservas = []

    def obtener_habitacion(self):
        return self.__habitaciones

    def obtener_categorias(self):
        return self.__categoria_precios

    def obtener_reservas(self):
        return self.__reservas


    def habitaciones_disponibles(self, fecha_entrada:datetime, fecha_salida: datetime) -> list[str]:
        """Devuelve Ids de habitaciones libres en el reango solicitado"""
        habitaciones = {h.id_habitacion for h in self.__habitaciones}
        registros = self.__reservas
        ocupadas = set()

        for r in registros:
            if r.estado == "Cancelado":
                continue

            try:
                he = r.fecha_entrada
                hs = r.fecha_salida
            except Exception:
                continue  # Si hay una fecha invalida, la salta

            if rango_se_solapa(fecha_entrada, fecha_salida - timedelta(days=1), he, hs - timedelta(days=1)):
                ocupadas.add(r.habitacion.id_habitacion)

        return sorted(list(habitaciones - ocupadas))

# -------- TRABAJADOR --------
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

# -------- RECEPCIONISTA --------
class Recepcionista(Trabajador):
    def __init__(self, codigo_trabajador , nombre_trabajador, dni_trabajador, telefono_trabajador, hotel: GestionHotel):
        super().__init__(codigo_trabajador , nombre_trabajador, dni_trabajador, telefono_trabajador)
        self.__hotel = hotel
        # self.__reserva = reserva
        # self.__cliente = cliente

    def generar_reserva(self):
        print("\n---GENERANDO RESERVA---")
        dni = input("DNI: ").strip()
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        telefono = input("Número de celular (opcional): ").strip()

        fecha_str = input("Fecha de ingreso (dd/mm/aaaa): ").strip()
        dias = int(input("Cantidad de días: ").strip())
        fecha_ingreso = parse_fecha(fecha_str)
        fecha_salida = fecha_ingreso + timedelta(days=dias)

        # MOSTRAR CATEGORIAS
        print("\n CATEGORIAS DISPONIBLES")
        categorias = list(self.__hotel.obtener_categorias().items())
        for i, (categoria, precio) in enumerate(categorias, start=1):
            print(f"{i}.{categoria} - s/{precio:.2f} por noche")

        #EXCEPCION: INGRESAR UN NUMERO INVALIDO
        try:
            elegir_categoria = int(input("Escriba la categoria que desea consultar: "))
            categoria_elegida = categorias[elegir_categoria - 1][0]
        except(ValueError, IndexError):
            print("La opcion ingresada no es valida")
            return

        #BUSCAR HABITACIONES DISPONIBLES
        disponibles_id = self.__hotel.habitaciones_disponibles(fecha_ingreso,fecha_salida)
        disponibles=[
            h for h in self.__hotel.obtener_habitacion()
            if h.id_habitacion in disponibles_id and h.categoria == categoria_elegida
        ]

        if not disponibles:
            print("No hay habitaciones disponibles para esta categoria.")
            return

        print("\n HABITACIONES DISPONIBLES")
        for i, hab in enumerate(disponibles, start=1):
            print(f"{i}. {hab}")

        #EXCEPCION AL INGRESAR UNA HABITACION INCORRECTA
        try:
            num_hab = int(input("\n Ingrese el numero de la habitacion:"))
            habitacion = disponibles[num_hab - 1]
        except(ValueError, IndexError):
            print("La opcion ingresada no es valida")
            return

        cliente = Cliente(nombre, apellido, dni, telefono)
        reserva = Reserva(cliente, habitacion, fecha_ingreso, dias)

        self.__hotel.obtener_reservas().append(reserva)

        print("\n Reserva generada extosamente")
        print(reserva.resumen())
        pausar()

    def check_in(self):
        print("\n REALIZANDO CHECK IN")

        reservas = self.__hotel.obtener_reservas()
        encontrado = False
        dni = input("Ingrese el DNI: ").strip()

        for reserva in reservas:
            cliente = reserva.cliente

            if cliente.dni == dni:
                encontrado = True

                if reserva.estado == "Confirmada":
                    reserva.estado = "Activa"
                    print(f"\nCheck In realizado exitosamente")
                    print(f"    Cliente: {cliente.nombre} {cliente.apellido}")
                    print(f"    Habitacion: {reserva.habitacion}")
                    print(f"    Estado: {reserva.estado}")

        if not encontrado:
            print("No se encontro ninguna reserva con el DNI ingresado")

        pausar()


    def cancelar_reserva_dni(self):
        print("\n CANCELAR RESERVA:")
        reservas = self.__hotel.obtener_reservas()
        encontrado = False
        dni = input("Ingrese el DNI").strip()

        for reserva in reservas:
            cliente = reserva.cliente
            if cliente.dni == dni:
                print("\n RESERVA ENCONTRADA")
                print(reserva.resumen())

                confirmar = input("¿Desea cancelar la reserva? (s/n)").strip().lower()
                if confirmar == "s":
                    reserva.estado = "Cancelado"
                    print("Reserva cancelada, la habitacion queda disponible")
                else:
                    print("Cancelacion abortada")

                encontrado = True
                break

        if not encontrado:
            print("No se encontro ninguna reserva asociada a ese DNI")
        
        pausar()

    def cancelar_reserva_lista(self):
        print("\n CANCELAR RESERVA:")
        reservas = self.__hotel.obtener_reservas()

        if not reservas:
            print("No se han registrado reservas")
            return

        print("\n LISTA DE RESERVAS:")
        for i,reserva in enumerate(reservas, start=1):
            cliente = reserva.cliente
            print(f"{i}. {cliente.nombre} {cliente.apellido}, DNI: {cliente.dni}, Estado: {reserva.estado} ")

        #EXCEPCION AL INGRESAR UN NUMERO DE LA LISTA ERRONEAMENTE
        try:
            num = int(input("\n Ingrese el numero de la reserva a cancelar: "))
            if num < 1 or num > len(reservas):
                raise IndexError
            reserva = reservas[num - 1]
        except(ValueError, IndexError):
            print("Opcion invalida, Intente nuevamente")
            return

        print("\n Reserva seleccionada:")
        print(reserva.resumen())

        confirmar = input("¿Desea cancelar la reserva? (s/n): ").strip().lower()
        if confirmar == "s":
            reserva.estado = "Cancelado"
            print("Reserva cancelada, la habitcion queda disponible")
        else:
            print("Cancelacion abortada")

        pausar()

    # ---------MENU CANCELAR----------------
    def menu_cancelar(self):
        while True:
            try:
                clear()

                print("""
-----MENU RECEPCIONISTA ------)
Cancelar: 
1. lista de Reservas
2. Busqueda por DNI
3. Volver al menu""")

                opcion = input("Seleccione una opcion(1-3): ").strip()

                if opcion not in {"1", "2", "3"}:
                    raise OpcionInvalida("Opcion invalida. Intente nuevamente")

                if opcion == "1":
                    self.cancelar_reserva_lista()
                elif opcion == "2":
                    self.cancelar_reserva_dni()
                elif opcion == "3":
                    print("\n Regresando al menu general")
                    break
            except OpcionInvalida as e:
                print(e)
                pausar()
            except Exception as e:
                print(f"Ocurrio un error: {e}")
                pausar()

    # ---------MENU RECEPCIONISTA----------------
    def menu_recepcionista(self):
        while True:
            try:
                clear()
                print("""
-------- MENU RECEPCIONISTA --------
1) Generar Reserva
2) Check-In
3) Check-out
4) Cancelar Reserva
5) Regresar al menu general""")

                opcion = input("Seleccione una opcion(1-5): ").strip()

                if opcion not in {"1", "2", "3", "4", "5"}:
                    raise OpcionInvalida("Opcion invalida. Intente nuevamente")

                if opcion == "1":
                    self.generar_reserva()
                elif opcion == "2":
                    self.check_in()
                elif opcion == "3":
                    self.check_out()
                elif opcion == "4":
                    self.menu_cancelar()
                elif opcion == "5":
                    print("\n Regresando al menu general")
                    break
            except OpcionInvalida as e:
                print(e)

            except Exception as e:
                print(f"Ocurrio un error: {e}")
                pausar()

    # def consumo_minibar(self):
    #     items = [
    #         "Agua",
    #         "Gaseosa",
    #         "Frugos",
    #         "Vino",
    #         "Cerveza Corona"
    #     ]
    #     precios = [4 ,
    #                5 ,
    #                4 ,
    #                40 ,
    #                10]
    #
    #     print("\n REGISTRAR CONSUMO DEL MINIBAR")
    #     dni = input("Ingrese el DNI").strip()
    #     reservas = self.__hotel.obtener_reservas()
    #
    #     for reserva in reservas:
    #         cliente = reserva.cliente
    #         if cliente.dni == dni:
    #             try:
    #

#-------------------------
# REPORTES
#-------------------------

def exportar_reservas_excel(hotel: GestionHotel, nombre_archivo = "reporte_reservas.xlsx"):

    reservas = hotel.obtener_reservas()

    if not reservas:
        print("No hay reservas para exportar")
        return
    
    datos_excel = []
    for r in reservas:
        datos_excel.append({
            "Cliente DNI": r.cliente.dni,
            "Nombre Cliente": r.cliente.nombre,
            "Apellido Cliente": r.cliente.apellido,
            "Celular": r.cliente.celular,
            "Habitación": r.habitacion.id_habitacion,
            "Categoría": r.habitacion.categoria,
            "Fecha Entrada": r.fecha_entrada.strftime(DATE_FMT),
            "Fecha Salida": r.fecha_salida.strftime(DATE_FMT),
            "Días": r.dias,
            "Total a Pagar (S/)": r.total_a_pagar,
            "Estado": r.estado
        })

    df = pd.DataFrame(datos_excel)

    try:
        df.to_excel(nombre_archivo, index=False, engine="openpyxl")
        print(f"Reserva guardada exitosamente ene el atchivo '{nombre_archivo}'")
    except Exception as e:
        print(f"\n Ocurrio un erro al tratar de guardar en el archivo Excel: {e}")

                            

def mostrar_reservaciones(hotel: GestionHotel):  # Historial
    lista = hotel.obtener_reservas()
    if not lista:
        print("No se ha hecho ninguna reserva todavia.")
        return

    print("---HISOTRIAL DE RESERVAS---")
    for c, reserva in enumerate(lista, start=1):
        print(f"\n {c}. {reserva.resumen()}")

#---------MENU GENERAL-----------
def menu_principal(recepcionista: Recepcionista, hotel: GestionHotel):
    while True:
        try:
            clear()
            print("""
-----------------------------
     HOTEL VISTA DORADA
-----------------------------
        
-------MENU GENERAL---------      
1. RECEPCIONISTA
2. CAJERO
3. EXPORTAR REPORTE DE RESERVAS A EXCEL
4. SALIR""")
            opcion = input("Seleccione una opcion(1-4): ").strip()

            if opcion not in {"1", "2", "3", "4"}:
                raise OpcionInvalida ("Opcion invalida. Intente nuevamente")

            if opcion == "1":
                recepcionista.menu_recepcionista()
            elif opcion == "2":
                recepcionista.menu_cancelar()
            elif opcion == "3":
                exportar_reservas_excel(hotel)
                input("\n Presione ENTER para volver al menu principal...")
            elif opcion == "4":
                print("Saliendo del sistema")
                break

        except OpcionInvalida as e:
            print(e)
            input("Presiones ENTER para continuar")

        except Exception as e:
            print(f"Error: {e}")
            input("Presiones ENTER para continuar")

def main():
    hotel = GestionHotel()
    recepcionista1 = Recepcionista("T722152", "Gabriela", 722152, 904229818, hotel)
    menu_principal(recepcionista1, hotel)

if __name__ == "__main__":

    main()
