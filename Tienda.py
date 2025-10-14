from datetime import date
from decimal import Decimal


class Usuario:
    def __init__(
        self,
        user_id: str,
        nombre: str,
        is_guest: bool = False,
        rol_seleccionado: str = "",
        historial_compras: List[str] = None,
        historial_prestamos: List[str] = None,
    ):
        self.user_id: str = user_id
        self.nombre: str = nombre
        self.is_guest: bool = is_guest
        self.rol_seleccionado: str = rol_seleccionado
        self.historial_compras: List[str] = historial_compras or []
        self.historial_prestamos: List[str] = historial_prestamos or []

    def seleccionar_rol(self, rol: str):
        pass

    def ver_historial(self):
        pass

    def solicitar_prestamo(self, item_id: str):
        pass

    def comprar(self, item_id: str):
        pass


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
