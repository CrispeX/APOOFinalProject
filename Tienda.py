from datetime import date
from decimal import Decimal


class Usuario:
    def __init__(
        self,
        user_id: str,
        nombre: str,
        is_guest: bool = False,
        rol_seleccionado: str = "",
        historial_compras: List[str] = [],
        historial_prestamos: List[str] = [],
    ):
        self.user_id: str = user_id
        self.nombre: str = nombre
        self.is_guest: bool = is_guest
        self.rol_seleccionado: str = rol_seleccionado
        self.historial_compras: List[str] = historial_compras 
        self.historial_prestamos: List[str] = historial_prestamos

    def seleccionar_rol(self, rol: str):
        self.rol_seleccionado = rol
        print(f"El rol '{rol}' ha sido seleccionado para el usuario {self.nombre}.")

    def ver_historial(self):
        print(f"\nHistorial del usuario: {self.nombre}")
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

    def solicitar_prestamo(self, item_id: str):
        if self.rol_seleccionado != "Usuario":
            print("Para solicitar un prestamos debe tener el rol de usuario")
            return False
        if item_id in self.historial_prestamos:
            print("Ya este objeto a sido prestado")
            return False
        self.historial_prestamos.append(item_id)
        print(f"Solicitud de préstamo registrada: usuario={self.nombre}, item={item_id} el dia {date.today()}")
        return True

    def comprar(self, item_id: str):
        if self.rol_seleccionado != "Usuario":
            print("Para realizar una compra debe tener el rol de usuario")
            return False
        self.historial_compras.append(item_id)
        print(f"Solicitud de compra registrada: usuario={self.nombre}, item={item_id} el dia {date.today()}")
        return True


class Admin(Usuario):
    def __init__(
        self,
        user_id: str,
        nombre: str,
        is_guest: bool = False,
        rol_seleccionado: str = "",
        historial_compras: List[str] = None,
        historial_prestamos: List[str] = None,
    ):
        super().__init__(
            user_id=user_id,
            nombre=nombre,
            is_guest=is_guest,
            rol_seleccionado=rol_seleccionado,
            historial_compras=historial_compras,
            historial_prestamos=historial_prestamos,
        )

    def agregar_item(self, item: "Item"):
        pass

    def editar_item(self, item_id: str, cambios: Dict):
        pass

    def eliminar_item(self, item_id: str):
        pass

    def ver_reporte(self, tipo: str):
        pass


class Carrito:
    def _init_(self, carrito_id: str, items: Dict[str, int] = None, total: Decimal = Decimal("0.0")):
        self.carrito_id: str = carrito_id
        self.items: Dict[str, int] = items or {}  # itemID -> cantidad
        self.total: Decimal = total

    def agregar_item(self, item_id: str, cantidad: int):
        pass

    def remover_item(self, item_id: str):
        pass

    def calcular_total(self) -> Decimal:
        pass

    def checkout(self, usuario_id: str):
        pass


class Prestamo:
    def _init_(
        self,
        prestamo_id: str,
        item_ids: List[str] = None,
        user_id: str = None,
        fecha_inicio: date = None,
        fecha_devolucion: date = None,
        estado: str = "activo",
    ):
        self.prestamo_id: str = prestamo_id
        self.item_ids: List[str] = item_ids or []
        self.user_id: str = user_id
        self.fecha_inicio: date = fecha_inicio
        self.fecha_devolucion: date = fecha_devolucion
        self.estado: str = estado

    def renovar(self):
        pass

    def devolver(self):
        pass

    def calcular_multa(self) -> Decimal:
        pass


class ServicioStock:
    def _init_(self):
        self._repositorio = None

    def decrementar_por_compra(self, item_id: str, cantidad: int):
        pass

    def reservar_por_prestamo(self, item_id: str, cantidad: int):
        pass

    def restaurar_por_devolucion(self, item_id: str, cantidad: int):
        pass

    def verificar_disponibilidad(self, item_id: str) -> bool:
        pass


class Item:
    def _init_(
        self,
        id: str,
        titulo: str,
        stock: int,
        disponibilidad: List[str] = None,
        precio: Decimal = Decimal("0.0"),
    ):
        self.id: str = id
        self.titulo: str = titulo
        self.stock: int = stock
        self.disponibilidad: List[str] = disponibilidad
        self.precio: Decimal = precio

    def consultar_detalles(self):
        pass

    def actualizar_stock(self, delta: int):
        pass

    def cambiar_disponibilidad(self, tipo: str):
        pass

    def actualizar_precio(self, nuevo_precio: Decimal):
        pass

    def esta_disponible_para(self, tipo: str) -> bool:
        pass


    class Videojuego(Item):
        def _init_(
            self,
            id: str,
            titulo: str,
            consola_sistema: str,
            genero: str,
            stock: int,
            disponibilidad: List[str] = None,
            precio: Decimal = Decimal("0.0"),
        ):
            super()._init_(id=id, titulo=titulo, stock=stock, disponibilidad=disponibilidad, precio=precio)
            self.consola_sistema: str = consola_sistema
            self.genero: str = genero


class Disco(Item):
    def _init_(
        self,
        id: str,
        titulo: str,
        genero_musical: str,
        formato: str,
        stock: int,
        disponibilidad: List[str] = None,
        precio: Decimal = Decimal("0.0"),
    ):
        super()._init_(id=id, titulo=titulo, stock=stock, disponibilidad=disponibilidad, precio=precio)
        self.genero_musical: str = genero_musical
        self.formato: str = formato


class Consola(Item):
    def _init_(
        self,
        id: str,
        titulo: str,
        marca_modelo: str,
        estado: str,
        stock: int,
        disponibilidad: List[str] = None,
        precio: Decimal = Decimal("0.0"),
    ):
        super()._init_(id=id, titulo=titulo, stock=stock, disponibilidad=disponibilidad, precio=precio)
        self.marca_modelo: str = marca_modelo
        self.estado: str = estado


class Audiolibro(Item):
    def _init_(
        self,
        id: str,
        titulo: str,
        genero_literario: str,
        narrador: str,
        formato_digital: bool,
        stock: int,
        disponibilidad: List[str] = None,
        precio: Decimal = Decimal("0.0"),
    ):
        super()._init_(id=id, titulo=titulo, stock=stock, disponibilidad=disponibilidad, precio=precio)
        self.genero_literario: str = genero_literario
        self.narrador: str = narrador
        self.formato_digital: bool = formato_digital


class Pelicula(Item):
    def _init_(
        self,
        id: str,
        titulo: str,
        genero_cinematografico: str,
        formato: str,
        stock: int,
        disponibilidad: List[str] = None,
        precio: Decimal = Decimal("0.0"),
    ):
        super()._init_(id=id, titulo=titulo, stock=stock, disponibilidad=disponibilidad, precio=precio)
        self.genero_cinematografico: str = genero_cinematografico
        self.formato: str = formato
