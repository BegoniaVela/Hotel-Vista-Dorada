import os
from datetime import datetime, timedelta
import pandas as pd
import csv
import sys

ROOM_SERVICE_TARIFA = 50.0
DATE_FMT = "%d/%m/%Y"

# ====== RUTAS CSV ======
CSV_REGISTROS = os.path.join("csv", "registros_hotel.csv")

# -------- Utilidades --------

class OpcionInvalida(Exception):
    pass

def pausar():
    input("\nPresione ENTER para continuar...")

def parse_fecha(s: str) -> datetime:
    return datetime.strptime(s.strip(), DATE_FMT)

def rango_se_solapa(a_inicio, a_fin, b_inicio, b_fin) -> bool:
    return a_inicio <= b_fin and b_inicio <= a_fin

def _leer_csv_seguro(path: str):
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))

def _grabar_csv_append(path: str, headers: list, row: dict):
    """Append con creación del encabezado si no existe."""
    file_exists = os.path.exists(path)
    with open(path, "a", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=headers)
        if not file_exists:
            w.writeheader()
        w.writerow({h: row.get(h, "") for h in headers})

def _proximo_id_registro() -> int:
    rows = _leer_csv_seguro(CSV_REGISTROS)
    if not rows:
        return 1
    try:
        return max(int(r.get("ID_Registro", 0)) for r in rows) + 1
    except Exception:
        return len(rows) + 1

# -------- MODELOS --------

class Cliente:
    def __init__(self, nombre, apellido, dni, celular):
        self.__nombre = nombre
        self.__apellido = apellido
        self.__dni = dni
        self.__celular = celular

    @property
    def nombre(self): return self.__nombre
    @property
    def apellido(self): return self.__apellido
    @property
    def dni(self): return self.__dni
    @property
    def celular(self): return self.__celular

    def __str__(self):
        return (f"Nombre: {self.__nombre} {self.__apellido} | "
                f"DNI: {self.__dni} | Celular: {self.__celular or '-'}")

class Habitacion:
    def __init__(self, id_habitacion, categoria, precio_noche):
        self.__id_habitacion = id_habitacion
        self.__categoria = categoria
        self.__precio_noche = float(precio_noche)

    @property
    def id_habitacion(self): return self.__id_habitacion
    @property
    def categoria(self): return self.__categoria
    @property
    def precio_noche(self): return self.__precio_noche

    def __str__(self):
        return f"{self.__id_habitacion} ({self.__categoria}) - S/ {self.__precio_noche:.2f}"

class Reserva:
    def __init__(self, cliente: Cliente, habitacion: Habitacion,
                 fecha_entrada: datetime, dias: int,
                 consumo_minibar: float = 0.0, consumo_room_service: float = 0.0,
                 late_checkout: int = 0):
        self.__cliente = cliente
        self.__habitacion = habitacion
        self.__fecha_entrada = fecha_entrada
        self.__dias = int(dias)
        self.__fecha_salida = fecha_entrada + timedelta(days=self.__dias)
        self.__consumo_minibar = float(consumo_minibar)
        self.__consumo_room_service = float(consumo_room_service)
        self.__late_checkout = int(late_checkout)  # 1 sí / 0 no
        self.__estado = "Confirmada"
        self.__pagado = False
        self.__consumos = []

    # setters para checkout
    def set_minibar(self, monto: float): self.__consumo_minibar = float(monto or 0)
    def set_room_service(self, cantidad: int):
        cantidad = int(cantidad or 0)
        self.__consumo_room_service = ROOM_SERVICE_TARIFA * max(cantidad, 0)
    def set_late_checkout(self, valor_bool: bool): self.__late_checkout = 1 if valor_bool else 0

    @property
    def cliente(self): return self.__cliente
    @property
    def fecha_entrada(self): return self.__fecha_entrada
    @property
    def fecha_salida(self): return self.__fecha_salida
    @property
    def habitacion(self): return self.__habitacion
    @property
    def dias(self): return self.__dias
    @property
    def estado(self): return self.__estado
    @estado.setter
    def estado(self, valor): self.__estado = valor

    @property
    def total_hospedaje(self) -> float:
        return self.__habitacion.precio_noche * self.__dias

    @property
    def cargo_late_checkout(self) -> float:
        return (self.__habitacion.precio_noche / 6.0) if self.__late_checkout == 1 else 0.0

    @property
    def total_a_pagar(self) -> float:
        return self.total_hospedaje + self.__consumo_minibar + self.__consumo_room_service + self.cargo_late_checkout

    def marcar_pagado(self): self.__pagado = True
    def esta_pagado(self): return self.__pagado

    def agregar_consumo(self, nombre, precio, cantidad=1):
        self.__consumos.append({"nombre": nombre, "precio": float(precio), "cantidad": int(cantidad)})

    def get_consumos(self): return list(self.__consumos)
    def total_consumos(self):
        return sum(c["precio"] * c["cantidad"] for c in self.__consumos)

    def resumen(self) -> str:
        return (
            "-------- RESERVA --------\n"
            f"  Huésped: {self.__cliente.nombre} {self.__cliente.apellido}\n"
            f"  DNI: {self.__cliente.dni}\n"
            f"  Celular: {self.__cliente.celular or '-'}\n"
            f"  Ingreso: {self.__fecha_entrada.strftime(DATE_FMT)}\n"
            f"  Salida : {self.__fecha_salida.strftime(DATE_FMT)}\n"
            f"  Noches: {self.__dias}\n"
            f"  Habitación: {self.__habitacion.id_habitacion} ({self.__habitacion.categoria})\n"
            f"  Tarifa: S/ {self.__habitacion.precio_noche:.2f}\n"
            f"  Total (estancia): S/ {self.total_hospedaje:.2f}\n"
            f"  Consumo Minibar: S/ {self.__consumo_minibar:.2f}\n"
            f"  Room Service: S/ {self.__consumo_room_service:.2f}\n"
            f"  Late checkout: S/ {self.cargo_late_checkout:.2f}\n"
            f"  Total a pagar: S/ {self.total_a_pagar:.2f}\n"
           # f"  Estado : {self.__estado} | Pagado: {'Sí' if self.__pagado else 'No'}\n"
        )

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
        self.__categoria_precios = {h.categoria: h.precio_noche for h in self.__habitaciones}
        self.__reservas = []

    def obtener_habitacion(self): return self.__habitaciones
    def obtener_categorias(self): return self.__categoria_precios
    def obtener_reservas(self): return self.__reservas

    def buscar_reserva_por_dni(self, dni):
        for r in self.__reservas:
            if r.cliente.dni == dni:
                return r
        return None

    def habitaciones_disponibles(self, fecha_entrada:datetime, fecha_salida: datetime) -> list[str]:
        habitaciones = {h.id_habitacion for h in self.__habitaciones}
        ocupadas = set()
        for r in self.__reservas:
            he, hs = r.fecha_entrada, r.fecha_salida
            if rango_se_solapa(fecha_entrada, fecha_salida - timedelta(days=1), he, hs - timedelta(days=1)):
                ocupadas.add(r.habitacion.id_habitacion)
        return sorted(list(habitaciones - ocupadas))

# -------- Trabajador / Recepcionista --------

class Trabajador:
    def __init__(self, codigo_trabajador, nombre_trabajador, dni_trabajador, telefono_trabajador):
        self.__codigo_trabajador = codigo_trabajador
        self.__nombre_trabajador = nombre_trabajador
        self.__dni_trabajador = dni_trabajador
        self.__telefono_trabajador = telefono_trabajador

    def __str__(self):
        return (f"Código: {self.__codigo_trabajador} | "
                f"Nombre: {self.__nombre_trabajador} | "
                f"DNI: {self.__dni_trabajador} | "
                f"Tel.: {self.__telefono_trabajador}")

class Recepcionista(Trabajador):
    def __init__(self, codigo_trabajador , nombre_trabajador, dni_trabajador, telefono_trabajador, hotel: GestionHotel):
        super().__init__(codigo_trabajador , nombre_trabajador, dni_trabajador, telefono_trabajador)
        self.__hotel = hotel

    # ---- Reserva
    def generar_reserva(self):
        print("\n--- GENERAR RESERVA ---")
        dni = input("DNI: ").strip()
        nombre = input("Nombre: ").strip()
        apellido = input("Apellido: ").strip()
        telefono = input("Número de celular (opcional): ").strip()
        try:
            fecha_str = input("Fecha de ingreso (dd/mm/aaaa): ").strip()
            dias = int(input("Cantidad de días: ").strip())
            fecha_ingreso = parse_fecha(fecha_str)
            fecha_salida = fecha_ingreso + timedelta(days=dias)
        except Exception:
            print("Fecha o días inválidos.")
            pausar(); return

        print("\nCATEGORÍAS DISPONIBLES")
        categorias = list(self.__hotel.obtener_categorias().items())
        for i, (categoria, precio) in enumerate(categorias, start=1):
            print(f"{i}. {categoria} - S/ {precio:.2f} por noche")

        try:
            elegir = int(input("Elija categoría: "))
            categoria_elegida = categorias[elegir - 1][0]
        except (ValueError, IndexError):
            print("Opción inválida. Por favor seleccione una opción del menú.")
            pausar(); return

        disponibles_id = self.__hotel.habitaciones_disponibles(fecha_ingreso, fecha_salida)
        disponibles = [h for h in self.__hotel.obtener_habitacion()
                       if h.id_habitacion in disponibles_id and h.categoria == categoria_elegida]

        if not disponibles:
            print("No hay habitaciones disponibles para esta categoría/fechas.")
            pausar(); return

        print("\nHABITACIONES DISPONIBLES")
        for i, hab in enumerate(disponibles, start=1):
            print(f"{i}. {hab}")

        try:
            idx = int(input("Elija habitación: "))
            habitacion = disponibles[idx - 1]
        except (ValueError, IndexError):
            print("Opción inválida. Por favor seleccione una opción del menú.")
            pausar(); return

        cliente = Cliente(nombre, apellido, dni, telefono)
        reserva = Reserva(cliente, habitacion, fecha_ingreso, dias)
        self.__hotel.obtener_reservas().append(reserva)

        # Guardar inmediatamente en CSV (histórico)
        self._guardar_reserva_en_csv(reserva)

        print("\n✅ Reserva generada exitosamente.")
        print(reserva.resumen())
        pausar()

    # ---- Check-in
    def check_in(self):
        print("\n--- CHECK-IN ---")
        dni = input("DNI: ").strip()
        r = self.__hotel.buscar_reserva_por_dni(dni)
        if not r:
            print("No se encontró ninguna reserva con ese DNI.")
        else:
            if r.estado == "Confirmada":
                r.estado = "Activa"
                print("Check-in realizado.")
                print(r.resumen())
            else:
                print(f"No se puede hacer check-in: estado actual '{r.estado}'.")
        pausar()

    # ---- Pagar reserva
    def pagar_reserva(self):
        print("\n--- PAGAR RESERVA ---")
        dni = input("DNI: ").strip()
        r = self.__hotel.buscar_reserva_por_dni(dni)
        if not r:
            print("No se encontró ninguna reserva con ese DNI."); pausar(); return
        if r.esta_pagado():
            print("Esta reserva ya fue pagada."); pausar(); return

        print(r.resumen())
        metodo = input("Método de pago (Tarjeta/Efectivo): ").strip().lower()
        total_con_comision = round(r.total_a_pagar * 1.05, 2)
        print(f"Total con comisión (5%): S/ {total_con_comision:.2f} - Método: {metodo.capitalize()}")
        r.marcar_pagado()
        print("✅ Pago registrado.")
        pausar()

    # ---- Check-out con consumos y late
    def check_out(self):
        print("\n--- CHECK-OUT ---")
        dni = input("DNI: ").strip()
        r = self.__hotel.buscar_reserva_por_dni(dni)
        if not r:
            print("No se encontró ninguna reserva con ese DNI."); pausar(); return

        # Consumos/Late opcionales
        try:
            usar_minibar = input("¿Registrar consumo de minibar? (s/n): ").strip().lower() == "s"
            if usar_minibar:
                monto_minibar = float(input("  Monto total de minibar (S/): ").strip() or "0")
                r.set_minibar(monto_minibar)

            usar_rs = input("¿Registrar Room Service? (s/n): ").strip().lower() == "s"
            if usar_rs:
                cant_rs = int(input("  Cantidad de room service (S/50 c/u): ").strip() or "0")
                r.set_room_service(cant_rs)

            usar_late = input("¿Aplicar Late Checkout? (s/n): ").strip().lower() == "s"
            r.set_late_checkout(usar_late)

        except Exception:
            print("Entrada inválida en consumos/late. No se aplicaron adicionales.")

        r.estado = "Finalizada"

        print("\n>>> Resumen final con adicionales:")
        print(r.resumen())
        pausar()

    # ---- Persistencia de reservas nuevas
    def _guardar_reserva_en_csv(self, r: Reserva):
        headers = ["ID_Registro","ID_Cliente","Nombre","DNI","Numero_de_celular",
                   "ID_Habitacion","Fecha_Entrada","Fecha_Salida","Cantidad_noches","TotalAPagar"]

        id_reg = _proximo_id_registro()
        id_cliente = f"C{r.cliente.dni}"

        row = {
            "ID_Registro": id_reg,
            "ID_Cliente": id_cliente,
            "Nombre": f"{r.cliente.nombre} {r.cliente.apellido}",
            "DNI": r.cliente.dni,
            "Numero_de_celular": r.cliente.celular,
            "ID_Habitacion": r.habitacion.id_habitacion,
            "Fecha_Entrada": r.fecha_entrada.strftime(DATE_FMT),
            "Fecha_Salida": r.fecha_salida.strftime(DATE_FMT),
            "Cantidad_noches": r.dias,
            "TotalAPagar": round(r.total_a_pagar, 2),
        }
        _grabar_csv_append(CSV_REGISTROS, headers, row)

    # ---- Menú del recepcionista
    def menu_recepcionista(self):
        while True:
            try:
                print("""
-------- MENÚ RECEPCIONISTA --------
1) Generar Reserva
2) Check-In
3) Pagar Reserva
4) Check-Out (consumos/late opcional)
5) Volver al Menú Principal
""")
                opcion = input("Seleccione una opción (1-5): ").strip()
                if opcion == "1":
                    self.generar_reserva()
                elif opcion == "2":
                    self.check_in()
                elif opcion == "3":
                    self.pagar_reserva()
                elif opcion == "4":
                    self.check_out()
                elif opcion == "5":
                    break
                else:
                    raise OpcionInvalida("Opción inválida. Por favor seleccione una opción del menú.")
            except OpcionInvalida as e:
                print(e); pausar()
            except Exception as e:
                print(f"Ocurrió un error: {e}"); pausar()

# -------- Mostrar reservaciones (DataFrame) --------

def mostrar_reservaciones(hotel=None, ruta_csv=CSV_REGISTROS):
    """
    Muestra el contenido completo de 'csv/registros_hotel.csv'
    utilizando pandas DataFrame para un formato de tabla limpio.
    """
    if not os.path.exists(ruta_csv):
        print(f"⚠️  No existe el archivo: {ruta_csv}")
        pausar()
        return

    try:
        df = pd.read_csv(ruta_csv, encoding="utf-8-sig")
        if df.empty:
            print("No existen reservas registradas aún.")
            pausar(); return

        df.columns = df.columns.str.strip().str.replace(" ", "_")
        if "Cantidad_noches" not in df.columns and "Cantidad_dias" in df.columns:
            df.rename(columns={"Cantidad_dias": "Cantidad_noches"}, inplace=True)

        columnas_orden = [
            "ID_Registro","ID_Cliente","Nombre","DNI","Numero_de_celular",
            "ID_Habitacion","Fecha_Entrada","Fecha_Salida","Cantidad_noches","TotalAPagar"
        ]
        presentes = [c for c in columnas_orden if c in df.columns]
        df = df[presentes]

        if "ID_Registro" in df.columns:
            try:
                df["ID_Registro"] = pd.to_numeric(df["ID_Registro"], errors="coerce")
                df = df.sort_values("ID_Registro")
            except Exception:
                pass

        print("\n--- HISTORIAL DE RESERVAS (CSV) ---")
        print(df.to_string(index=False))
        print(f"\nTotal de reservas: {len(df)}")
    except Exception as e:
        print(f"❌ Error al leer o mostrar el archivo CSV: {e}")

    pausar()

# -------- Menú principal / main --------

def menu_principal(recepcionista: Recepcionista, hotel: GestionHotel):
    while True:
        try:
            print("""
-----------------------------
     HOTEL VISTA DORADA
-----------------------------
1) Recepcion
2) Mostrar Reservaciones
3) Salir
""")
            opcion = input("Seleccione una opción (1-3): ").strip()
            if opcion == "1":
                recepcionista.menu_recepcionista()
            elif opcion == "2":
                mostrar_reservaciones(hotel)
            elif opcion == "3":
                print("👋 Saliendo del sistema... ¡Hasta pronto!")
                sys.exit(0)
            else:
                raise OpcionInvalida("Opción inválida. Por favor seleccione una opción del menú.")
        except OpcionInvalida as e:
            print(e); pausar()
        except Exception as e:
            print(f"Error: {e}"); pausar()

def main():
    hotel = GestionHotel()
    recepcionista = Recepcionista("T722152", "Gabriela", 722152, 904229818, hotel)
    menu_principal(recepcionista, hotel)

if __name__ == "__main__":
    main()
