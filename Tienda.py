from datetime import date, timedelta
from decimal import Decimal
import tkinter as tk

class Usuario:
    def __init__(
        self,
        identificador: str,
        rol_seleccionado: str = "",
        historial_compras: list = None,
        historial_prestamos: list = None,
    ):
        self.identificador = identificador
        self.rol_seleccionado = rol_seleccionado
        self.historial_compras = historial_compras 
        self.historial_prestamos = historial_prestamos 

    def seleccionar_rol(self, rol: str):
        self.rol_seleccionado = rol
        print(f"El rol '{rol}' ha sido seleccionado.")

    def ver_historial(self):
        print(f"\nHistorial del usuario: {self.identificador}")
        print("Compras realizadas:")
        if self.historial_compras:
            for compra in self.historial_compras:
                print(f" - {compra}")
        else:
            print(" (sin compras registradas)")

        print("\nPréstamos realizados:")
        if self.historial_prestamos:
            for prestamo in self.historial_prestamos:
                print(f" - {prestamo}")
        else:
            print(" (sin préstamos registrados)")

    def solicitar_prestamo(self, codigo_articulo: str, servicio_stock, lista_prestamos: list):
        if self.rol_seleccionado != "Usuario":
            print("Para solicitar un préstamo debe tener el rol 'Usuario'.")
            return False
        if not servicio_stock.verificar_disponibilidad(codigo_articulo):
            print("El artículo no está disponible para préstamo.")
            return False
        servicio_stock.reservar_por_prestamo(codigo_articulo, 1)
        id_prestamo = f"prestamo{len(lista_prestamos) + 1}"
        prestamo = Prestamo(
            prestamo_id=id_prestamo,
            item_ids=[codigo_articulo],
            user_id=self.identificador,
            fecha_inicio=date.today(),
            fecha_devolucion=date.today() + timedelta(days=7),
            estado="activo",
        )
        lista_prestamos.append(prestamo)
        self.historial_prestamos.append(id_prestamo)
        print(f"Préstamo registrado: id={id_prestamo}, usuario={self.identificador}, artículo={codigo_articulo}")
        return True

    def comprar(self, codigo_articulo: str, carrito, servicio_stock):
        if self.rol_seleccionado != "Usuario":
            print("Para realizar una compra debe tener el rol 'Usuario'.")
            return False
        carrito.agregar_item(codigo_articulo, 1)
        print(f"Artículo {codigo_articulo} agregado al carrito de {self.identificador}.")
        return True


class Administrador(Usuario):
    def __init__(
        self,
        identificador: str,
        rol_seleccionado: str = "Admin",
        historial_compras: list = None,
        historial_prestamos: list = None,
    ):
        super().__init__(identificador, rol_seleccionado, historial_compras, historial_prestamos)

    def agregar_item(self, articulo, catalogo: dict):
        catalogo[articulo.codigo] = articulo
        print(f"Artículo agregado: {articulo.codigo} - {articulo.titulo}")

    def editar_item(self, codigo_item: str, cambios: dict, catalogo: dict):
        if codigo_item not in catalogo:
            print("Artículo no encontrado.")
            return
        articulo = catalogo[codigo_item]
        if "titulo" in cambios:
            articulo.titulo = cambios["titulo"]
        if "precio" in cambios:
            articulo.precio = Decimal(str(cambios["precio"]))
        if "stock" in cambios:
            articulo.stock = cambios["stock"]
        print(f"Artículo {codigo_item} actualizado.")

    def eliminar_item(self, codigo_item: str, catalogo: dict):
        if codigo_item in catalogo:
            del catalogo[codigo_item]
            print(f"Artículo {codigo_item} eliminado.")
        else:
            print("Artículo no encontrado.")

    def ver_reporte(self, tipo: str, catalogo: dict, lista_usuarios: list):
        if tipo == "items":
            print("Reporte de artículos:")
            for it in catalogo.values():
                print(f"- {it.codigo} | {it.titulo} | stock: {it.stock} | precio: {it.precio}")
        elif tipo == "usuarios":
            print("Reporte de usuarios:")
            for u in lista_usuarios:
                print(f"- {u.identificador} | rol: {u.rol_seleccionado}")
        else:
            print("Tipo de reporte desconocido. Use 'items' o 'usuarios'.")


class Carrito:
    def __init__(self, identificador_carrito: str, articulos: dict = None, total: Decimal = Decimal("0.0")):
        self.identificador_carrito = identificador_carrito
        self.articulos = articulos or {}
        self.total = total

    def agregar_item(self, codigo_item: str, cantidad: int):
        if codigo_item in self.articulos:
            self.articulos[codigo_item] += cantidad
        else:
            self.articulos[codigo_item] = cantidad

    def remover_item(self, codigo_item: str):
        if codigo_item in self.articulos:
            del self.articulos[codigo_item]

    def calcular_total(self, catalogo: dict) -> Decimal:
        total = Decimal("0.0")
        for codigo_item, cantidad in self.articulos.items():
            articulo = catalogo.get(codigo_item)
            if articulo:
                total += articulo.precio * cantidad
        self.total = total
        return total

    def checkout(self, usuario: Usuario, servicio_stock, catalogo: dict):
        for codigo_item, cantidad in list(self.articulos.items()):
            articulo = catalogo.get(codigo_item)
            if not articulo:
                print(f"Artículo {codigo_item} no existe, se omite.")
                continue
            if articulo.stock < cantidad:
                print(f"No hay suficiente stock para {articulo.titulo}. Disponible: {articulo.stock}, pedido: {cantidad}")
                return False
        for codigo_item, cantidad in list(self.articulos.items()):
            servicio_stock.decrementar_por_compra(codigo_item, cantidad)
            usuario.historial_compras.append(codigo_item)
        total = self.calcular_total(catalogo)
        print(f"Compra realizada por {usuario.identificador}. Total: {total} (artículos: {self.articulos})")
        self.articulos = {}
        self.total = Decimal("0.0")
        return True


class Prestamo:
    def __init__(self, prestamo_id: str, item_ids: list, user_id: str, fecha_inicio: date, fecha_devolucion: date, estado: str = "activo"):
        self.prestamo_id = prestamo_id
        self.item_ids = item_ids
        self.user_id = user_id
        self.fecha_inicio = fecha_inicio
        self.fecha_devolucion = fecha_devolucion
        self.estado = estado

    def renovar(self, dias: int = 7):
        if self.estado != "activo":
            print("No se puede renovar un préstamo que no está activo.")
            return False
        self.fecha_devolucion = self.fecha_devolucion + timedelta(days=dias)
        print(f"Préstamo {self.prestamo_id} renovado. Nueva devolución: {self.fecha_devolucion}")
        return True

    def devolver(self, servicio_stock):
        if self.estado != "activo":
            print("El préstamo ya no está activo.")
            return False
        for codigo_item in self.item_ids:
            servicio_stock.restaurar_por_devolucion(codigo_item, 1)
        self.estado = "devuelto"
        print(f"Préstamo {self.prestamo_id} marcado como devuelto.")
        return True

    def calcular_multa(self) -> Decimal:
        hoy = date.today()
        if hoy <= self.fecha_devolucion:
            return Decimal("0.0")
        dias_atraso = (hoy - self.fecha_devolucion).days
        multa = Decimal("0.5") * dias_atraso * len(self.item_ids)
        return multa


class ServicioStock:
    def __init__(self, catalogo: dict):
        self.catalogo = catalogo

    def decrementar_por_compra(self, codigo_item: str, cantidad: int):
        articulo = self.catalogo.get(codigo_item)
        if not articulo:
            return False
        articulo.stock = max(0, articulo.stock - cantidad)
        return True

    def reservar_por_prestamo(self, codigo_item: str, cantidad: int):
        articulo = self.catalogo.get(codigo_item)
        if not articulo or articulo.stock < cantidad:
            return False
        articulo.stock -= cantidad
        return True

    def restaurar_por_devolucion(self, codigo_item: str, cantidad: int):
        articulo = self.catalogo.get(codigo_item)
        if not articulo:
            return False
        articulo.stock += cantidad
        return True

    def verificar_disponibilidad(self, codigo_item: str) -> bool:
        articulo = self.catalogo.get(codigo_item)
        return bool(articulo and articulo.stock > 0)


class Item:
    def __init__(self, codigo: str, titulo: str, stock: int, disponibilidad: list = None, precio: Decimal = Decimal("0.0")):
        self.codigo = codigo
        self.titulo = titulo
        self.stock = stock
        self.disponibilidad = disponibilidad or []
        self.precio = Decimal(str(precio))

    def consultar_detalles(self):
        print(f"CÓDIGO: {self.codigo}")
        print(f"Título: {self.titulo}")
        print(f"Stock: {self.stock}")
        print(f"Disponibilidad: {self.disponibilidad}")
        print(f"Precio: {self.precio}")

    def actualizar_stock(self, delta: int):
        self.stock += delta

    def cambiar_disponibilidad(self, tipo: str):
        if tipo in self.disponibilidad:
            self.disponibilidad.remove(tipo)
        else:
            self.disponibilidad.append(tipo)

    def actualizar_precio(self, nuevo_precio):
        self.precio = Decimal(str(nuevo_precio))

    def esta_disponible_para(self, tipo: str) -> bool:
        return tipo in self.disponibilidad or not self.disponibilidad


def crear_datos_iniciales():
    usuarios = []
    catalogo_items = {}
    prestamos = []

    u1 = Usuario("usuario1", rol_seleccionado="Usuario")
    u2 = Administrador("administrador1", rol_seleccionado="Admin")
    usuarios.extend([u1, u2])

    a1 = Item("art1", "Juego: Aventura", stock=3, disponibilidad=["prestamo", "venta"], precio=Decimal("19.99"))
    a2 = Item("art2", "Película: Ciencia Ficción", stock=2, disponibilidad=["venta"], precio=Decimal("9.50"))
    a3 = Item("art3", "Disco: Pop Hits", stock=5, disponibilidad=["prestamo", "venta"], precio=Decimal("7.25"))
    catalogo_items[a1.codigo] = a1
    catalogo_items[a2.codigo] = a2
    catalogo_items[a3.codigo] = a3

    servicio_stock = ServicioStock(catalogo_items)

    return usuarios, catalogo_items, prestamos, servicio_stock


def mostrar_catalogo(catalogo: dict):
    print("\n--- Catálogo de artículos ---")
    for it in catalogo.values():
        print(f"{it.codigo} | {it.titulo} | stock: {it.stock} | precio: {it.precio}")


def buscar_primer_usuario_por_rol(rol: str, lista_usuarios: list):
    for u in lista_usuarios:
        if u.rol_seleccionado and u.rol_seleccionado.lower() == rol.lower():
            return u
    return None


def menu_principal(lista_usuarios: list, catalogo: dict, lista_prestamos: list, servicio_stock):
    while True:
        print("\n--- MENÚ PRINCIPAL ---")
        print("1) Entrar como Usuario")
        print("2) Entrar como Administrador")
        print("3) Ver catálogo")
        print("4) Salir")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            existente = buscar_primer_usuario_por_rol("Usuario", lista_usuarios)
            if existente:
                usuario_actual = existente
            else:
                usuario_actual = Usuario("usuario_temporal", rol_seleccionado="Usuario")
            carrito_actual = Carrito(f"carrito_{usuario_actual.identificador}")
            print(f"Sesión iniciada como USUARIO (id: {usuario_actual.identificador}).")
            menu_usuario(usuario_actual, carrito_actual, catalogo, lista_prestamos, servicio_stock)
        elif opcion == "2":
            existente = buscar_primer_usuario_por_rol("Admin", lista_usuarios)
            if existente:
                administrador_actual = existente
            else:
                administrador_actual = Administrador("admin_temporal", rol_seleccionado="Admin")
            print(f"Sesión iniciada como ADMIN (id: {administrador_actual.identificador}).")
            menu_admin(administrador_actual, catalogo, lista_usuarios)
        elif opcion == "3":
            mostrar_catalogo(catalogo)
        elif opcion == "4":
            print("Saliendo... chao.")
            break
        else:
            print("Opción inválida.")


def menu_usuario(usuario: Usuario, carrito: Carrito, catalogo: dict, lista_prestamos: list, servicio_stock):
    while True:
        print("\n--- MENÚ USUARIO ---")
        print("1) Ver catálogo")
        print("2) Ver detalle artículo")
        print("3) Agregar artículo al carrito")
        print("4) Ver carrito")
        print("5) Pagar / Comprar")
        print("6) Solicitar préstamo")
        print("7) Ver historial")
        print("8) Cerrar sesión")
        opcion = input("Elige una opción: ").strip()

        if opcion == "1":
            mostrar_catalogo(catalogo)
        elif opcion == "2":
            codigo = input("Código del artículo: ").strip()
            articulo = catalogo.get(codigo)
            if articulo:
                articulo.consultar_detalles()
            else:
                print("Artículo no encontrado.")
        elif opcion == "3":
            codigo = input("Código del artículo a agregar al carrito: ").strip()
            cantidad_input = input("Cantidad (enter para 1): ").strip()
            cantidad = int(cantidad_input) if cantidad_input else 1
            carrito.agregar_item(codigo, cantidad)
            print("Agregado al carrito.")
        elif opcion == "4":
            print(f"Contenido del carrito: {carrito.articulos}")
            print(f"Total: {carrito.calcular_total(catalogo)}")
        elif opcion == "5":
            confirmado = input("Confirmar compra del carrito? (s/n): ").strip().lower()
            if confirmado == "s":
                carrito.checkout(usuario, servicio_stock, catalogo)
        elif opcion == "6":
            codigo = input("Código del artículo a solicitar en préstamo: ").strip()
            usuario.solicitar_prestamo(codigo, servicio_stock, lista_prestamos)
        elif opcion == "7":
            usuario.ver_historial()
        elif opcion == "8":
            print("Cerrando sesión.")
            break
        else:
            print("Opción inválida.")


def menu_admin(administrador: Administrador, catalogo: dict, lista_usuarios: list):
    while True:
        print("\n--- MENÚ ADMIN ---")
        print("1) Agregar artículo")
        print("2) Editar artículo")
        print("3) Eliminar artículo")
        print("4) Ver reporte de artículos")
        print("5) Ver reporte de usuarios")
        print("6) Volver al menú principal")
        opcion_admin = input("Elige una opción: ").strip()
        if opcion_admin == "1":
            titulo = input("Título: ").strip()
            stock = int(input("Stock inicial: ").strip() or "0")
            precio = input("Precio (ej: 19.99): ").strip() or "0.0"
            codigo = f"art{len(catalogo) + 1}"
            nuevo = Item(codigo, titulo, stock, disponibilidad=["venta", "prestamo"], precio=Decimal(str(precio)))
            administrador.agregar_item(nuevo, catalogo)
        elif opcion_admin == "2":
            codigo = input("Código del artículo a editar: ").strip()
            cambios = {}
            nuevo_titulo = input("Nuevo título (enter para omitir): ").strip()
            if nuevo_titulo:
                cambios["titulo"] = nuevo_titulo
            nuevo_precio = input("Nuevo precio (enter para omitir): ").strip()
            if nuevo_precio:
                cambios["precio"] = nuevo_precio
            nuevo_stock = input("Nuevo stock (enter para omitir): ").strip()
            if nuevo_stock:
                cambios["stock"] = int(nuevo_stock)
            administrador.editar_item(codigo, cambios, catalogo)
        elif opcion_admin == "3":
            codigo = input("Código del artículo a eliminar: ").strip()
            administrador.eliminar_item(codigo, catalogo)
        elif opcion_admin == "4":
            administrador.ver_reporte("items", catalogo, lista_usuarios)
        elif opcion_admin == "5":
            administrador.ver_reporte("usuarios", catalogo, lista_usuarios)
        elif opcion_admin == "6":
            print("Volviendo al menú principal.")
            break
        else:
            print("Opción inválida.")


if __name__ == "__main__":
    usuarios, catalogo_items, prestamos, servicio_stock = crear_datos_iniciales()
    menu_principal(usuarios, catalogo_items, prestamos, servicio_stock)
"""app = tk.Tk()
#Dimensiones de la pestaña
app.geometry("300x600")
app.config(background="black")
tk.Wm.wm_title(app, "Tienda de contenido audio visual")
tk.Button(
    app,
    text="Ingresar como usuario",
    background="White",
    command=menu_usuario,
).pack(
    fill=tk.BOTH,
    expand=True,
)
tk.Button(
    app,
    text="Ingresar como administrador",
    background="White",
    command=menu_admin,
).pack(
    fill=tk.BOTH,
    expand=True,
)
#etiquetas
tk.Label(
    app,
    text="etiqueta",
    bg="blue",
    justify="center",
).pack(
    fill=tk.BOTH,
    expand=True,
)
#tipo input
tk.Entry(
    bg="blue",
    justify="center",
).pack(
    fill=tk.BOTH,
    expand=True,
)
app.mainloop()"""
