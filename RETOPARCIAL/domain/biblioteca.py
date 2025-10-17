from domain.libro import Libro
from domain.usuario import Usuario


class Biblioteca:
    """Modelo principal: maneja libros y usuarios."""

    def __init__(self, nombre: str):
        self.nombre = nombre
        self._libros = {}
        self._usuarios = {}

    # --- Gestión de libros ---
    def agregar_libro(self, libro: Libro):
        if libro.id_libro in self._libros:
            raise ValueError("Ya existe un libro con ese ID")
        self._libros[libro.id_libro] = libro

    def eliminar_libro(self, id_libro):
        if id_libro not in self._libros:
            raise ValueError("Libro no encontrado")
        del self._libros[id_libro]

    def listar_libros(self):
        return list(self._libros.values())

    # --- Gestión de usuarios ---
    def registrar_usuario(self, usuario: Usuario):
        if usuario.id_usuario in self._usuarios:
            raise ValueError("Ya existe un usuario con ese ID")
        self._usuarios[usuario.id_usuario] = usuario

    def listar_usuarios(self):
        return list(self._usuarios.values())

    # --- Préstamos ---
    def prestar_libro(self, id_libro, id_usuario):
        if id_libro not in self._libros:
            raise ValueError("Libro no encontrado")
        if id_usuario not in self._usuarios:
            raise ValueError("Usuario no encontrado")

        libro = self._libros[id_libro]
        usuario = self._usuarios[id_usuario]

        libro.prestar()
        usuario.prestar_libro(libro)

    def devolver_libro(self, id_libro, id_usuario):
        if id_libro not in self._libros or id_usuario not in self._usuarios:
            raise ValueError("Libro o usuario no encontrado")

        libro = self._libros[id_libro]
        usuario = self._usuarios[id_usuario]

        libro.devolver()
        usuario.devolver_libro(libro)

    # --- Firebase helpers ---
    def to_dict(self):
        return {
            "nombre": self.nombre,
            "libros": {lid: lib.to_dict() for lid, lib in self._libros.items()},
            "usuarios": {uid: usr.to_dict() for uid, usr in self._usuarios.items()},
        }

    @classmethod
    def from_dict(cls, data):
        bib = cls(data["nombre"])
        for lid, ldata in data.get("libros", {}).items():
            bib._libros[lid] = Libro.from_dict(ldata)
        for uid, udata in data.get("usuarios", {}).items():
            bib._usuarios[uid] = Usuario.from_dict(udata)
        return bib
