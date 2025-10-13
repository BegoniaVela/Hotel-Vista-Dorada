import csv
import os
from datetime import datetime, timedelta

CSV_DIR = "csv"
HABITACIONES_CSV = os.path.join(CSV_DIR, "habitaciones_hotel.csv")
REGISTROS_CSV = os.path.join(CSV_DIR, "registros_hotel.csv")

ROOM_SERVICE_TARIFA = 50.0  # fijo
DATE_FMT = "%d/%m/%Y"


# Utilidades
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


def leer_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def escribir_csv(path, filas, fieldnames):
    nuevo = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        if nuevo:
            w.writeheader()
        for row in filas:
            w.writerow(row)


# Modelos
class Cliente:
    def __init__(self, dni: str, nombre: str, apellido: str, telefono: str = ""):
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono

    def __str__(self):
        return f"DNI: {self.dni}, Nombre: {self.nombre} {self.apellido}"


class Habitacion:
    def __init__(self, id_habitacion: str, categoria: str, precio_noche: float):
        self.id = id_habitacion
        self.categoria = categoria
        self.precio_noche = float(precio_noche)

    def __str__(self):
        return f"{self.id} ({self.categoria}) - S/ {self.precio_noche:.2f}"


class Reserva:
    def __init__(self, cliente: Cliente, habitacion: Habitacion,
                 fecha_entrada: datetime, dias: int,
                 consumo_minibar: float = 0.0, consumo_room_service: float = 0.0, late_checkout: int = 0):
        self.cliente = cliente
        self.habitacion = habitacion
        self.fecha_entrada = fecha_entrada
        self.dias = int(dias)
        self.fecha_salida = fecha_entrada + timedelta(days=self.dias)
        self.consumo_minibar = float(consumo_minibar)
        self.consumo_room_service = float(consumo_room_service)
        self.late_checkout = int(late_checkout)  # 1 sí / 0 no

    @property
    def total_hospedaje(self) -> float:
        return self.habitacion.precio_noche * self.dias

    @property
    def cargo_late_checkout(self) -> float:
        # equivalente a 4 horas: precio/24*4 = precio/6
        return (self.habitacion.precio_noche / 6.0) if self.late_checkout == 1 else 0.0

    @property
    def total_a_pagar(self) -> float:
        return self.total_hospedaje + self.consumo_minibar + self.consumo_room_service + self.cargo_late_checkout

    def resumen(self) -> str:
        return (
            "--------MENU RECEPCIONISTA--------\n"
            "Reserva generada:\n"
            f"  Nombre: {self.cliente.nombre} {self.cliente.apellido}\n"
            f"  DNI: {self.cliente.dni}\n"
            f"  Numero de celular: {self.cliente.telefono or '-'}\n"
            f"  Cantidad de invitados extra: 0\n"
            f"  Fecha Ingreso: {self.fecha_entrada.strftime(DATE_FMT)}\n"
            f"  Fecha salida: {self.fecha_salida.strftime(DATE_FMT)}\n"
            f"  Cantidad de dias: {self.dias}\n"
            f"  Precio: {int(self.habitacion.precio_noche)}\n"
            f"  Habitacion: {self.habitacion.id}\n"
            f"  Precio a cancelar: s/ {int(self.total_a_pagar)}\n"
        )


# Capa de datos
def cargar_habitaciones() -> list[Habitacion]:
    rows = leer_csv(HABITACIONES_CSV)
    return [Habitacion(r["ID_Habitacion"], r["Categoria"], float(r["Precio"])) for r in rows]


def cargar_registros():
    if not os.path.exists(REGISTROS_CSV):
        return []
    return leer_csv(REGISTROS_CSV)


def proximo_id_registro(registros) -> int:
    if not registros:
        return 1
    return max(int(r["ID_Registro"]) for r in registros) + 1


def habitaciones_disponibles(fecha_entrada: datetime, fecha_salida: datetime) -> list[str]:
    """Devuelve IDs de habitaciones libres en el rango solicitado."""
    habitaciones = {h.id for h in cargar_habitaciones()}
    registros = cargar_registros()
    ocupadas = set()

    for r in registros:
        he = parse_fecha(r["Fecha_Entrada"])
        hs = parse_fecha(r["Fecha_Salida"])
        if rango_se_solapa(fecha_entrada, fecha_salida - timedelta(days=1), he, hs - timedelta(days=1)):
            ocupadas.add(r["ID_Habitacion"])

    return sorted(list(habitaciones - ocupadas))


def guardar_reserva_csv(reserva: Reserva, id_cliente: str = "A000"):
    registros = cargar_registros()
    nuevo_id = proximo_id_registro(registros)

    row = {
        "ID_Registro": str(nuevo_id),
        "ID_Cliente": id_cliente,  # puedes mapear tu DNI a un ID real si gustas
        "ID_Habitacion": reserva.habitacion.id,
        "Fecha_Entrada": reserva.fecha_entrada.strftime(DATE_FMT),
        "Fecha_Salida": reserva.fecha_salida.strftime(DATE_FMT),
        "Cantidad_dias": str(reserva.dias),
        "Precio_Noche": str(int(reserva.habitacion.precio_noche)),
        "Consumo_Minibar": str(int(reserva.consumo_minibar)),
        "Consumo_RoomService": str(int(reserva.consumo_room_service)),
        "LateCheckout": str(reserva.late_checkout),
    }

    escribir_csv(
        REGISTROS_CSV,
        [row],
        fieldnames=list(row.keys())
    )
    return nuevo_id


# Menus
def ui_menu():
    print("""
-------- MENU RECEPCIONISTA --------
1) Consultar reserva por DNI
2) Generar reserva
3) Check-out
4) Historial (CSV)
5) Salir
""")


def input_opcion(msg="Seleccione una opción: "):
    op = input(msg).strip()
    if op not in {"1", "2", "3", "4", "5"}:
        raise OpcionInvalida("Opción inválida. Por favor seleccione una opción del menú.")
    return op


def flujo_consultar():
    dni = input("Ingrese DNI a consultar: ").strip()
    regs = cargar_registros()
    encontrados = [r for r in regs if r["ID_Cliente"] == dni or r["ID_Cliente"] == f"A{dni}"]
    if not encontrados:
        print("No se encontraron reservas para ese DNI.")
    else:
        print("\n--- Reservas ---")
        for r in encontrados:
            print(r)
    pausar()


def flujo_generar_reserva():
    print("------ Generando Reserva ------")
    dni = input("DNI: ").strip()
    nombre = input("Nombre: ").strip()
    apellido = input("Apellido: ").strip()
    telefono = input("Número de celular (opcional): ").strip()
    fecha_txt = input("Fecha de ingreso (dd/mm/aaaa): ").strip()
    dias = int(input("Cantidad de días: ").strip())

    fecha_entrada = parse_fecha(fecha_txt)
    fecha_salida = fecha_entrada + timedelta(days=dias)

    libres = habitaciones_disponibles(fecha_entrada, fecha_salida)
    if not libres:
        print("\nNo hay habitaciones disponibles para ese rango de fechas.")
        pausar()
        return

    print(f"\nHabitaciones disponibles: {libres}")
    eleccion = input("Seleccione ID de habitación: ").strip()
    if eleccion not in libres:
        print("Habitación no disponible o inválida.")
        pausar()
        return

    # Obtener precio y categoría desde CSV
    hab_match = [h for h in cargar_habitaciones() if h.id == eleccion][0]
    cliente = Cliente(dni, nombre, apellido, telefono)
    reserva = Reserva(cliente, hab_match, fecha_entrada, dias)

    print("\n" + reserva.resumen())

    guardar_reserva_csv(reserva, id_cliente=dni)
    pausar()


def flujo_checkout():
    print("------ Check-out ------")
    id_registro = input("ID_Registro (según CSV): ").strip()
    registros = cargar_registros()
    r = next((x for x in registros if x["ID_Registro"] == id_registro), None)
    if not r:
        print("Registro no encontrado.")
        pausar()
        return

    # Calcular cargo LateCheckout
    hab = next(h for h in cargar_habitaciones() if h.id == r["ID_Habitacion"])
    precio_noche = float(hab.precio_noche)

    minibar = float(r.get("Consumo_Minibar", 0) or 0)
    rs = float(r.get("Consumo_RoomService", 0) or 0)

    aplicar_rs = input("¿Agregar un Room Service? (s/n): ").strip().lower() == "s"
    if aplicar_rs:
        rs += ROOM_SERVICE_TARIFA

    aplicar_lc = input("¿Late checkout? (s/n): ").strip().lower() == "s"
    cargo_lc = (precio_noche / 6.0) if aplicar_lc else 0.0

    total_hospedaje = precio_noche * int(r["Cantidad_dias"])
    total = total_hospedaje + minibar + rs + cargo_lc

    print("\n--- Resumen Check-out ---")
    print(f"Habitación: {r['ID_Habitacion']}  |  Noches: {r['Cantidad_dias']}")
    print(f"Precio por noche: S/ {precio_noche:.2f}")
    print(f"Consumo minibar: S/ {minibar:.2f}")
    print(f"Room service: S/ {rs:.2f}")
    print(f"Late checkout: S/ {cargo_lc:.2f}")
    print(f"TOTAL A PAGAR: S/ {total:.2f}")

    # Actualizar fila en CSV
    for row in registros:
        if row["ID_Registro"] == id_registro:
            row["Consumo_RoomService"] = str(int(rs))
            row["LateCheckout"] = "1" if aplicar_lc else "0"
            break

    # Archivo con cambios
    with open(REGISTROS_CSV, "w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "ID_Registro", "ID_Cliente", "ID_Habitacion", "Fecha_Entrada", "Fecha_Salida",
            "Cantidad_dias", "Precio_Noche", "Consumo_Minibar", "Consumo_RoomService", "LateCheckout"
        ]
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for row in registros:
            w.writerow(row)

    pausar()


def flujo_historial():
    print("\n===== Historial (registros_hotel.csv) =====\n")
    for r in cargar_registros():
        print(r)
    pausar()


# Loop principal
def main():
    while True:
        clear()
        ui_menu()
        try:
            opcion = input_opcion()
            if opcion == "1":
                clear()
                flujo_consultar()
            elif opcion == "2":
                clear()
                flujo_generar_reserva()
            elif opcion == "3":
                clear()
                flujo_checkout()
            elif opcion == "4":
                clear()
                flujo_historial()
            elif opcion == "5":
                print("¡Hasta luego!")
                break
        except OpcionInvalida as e:
            print(str(e))
            pausar()
        except Exception as e:
            print(f"Error: {e}")
            pausar()


if __name__ == "__main__":
    main()
