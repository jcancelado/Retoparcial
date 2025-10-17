class Usuario:
    """Modelo de dominio: representa un usuario de la biblioteca."""

    def __init__(self, id_usuario: str, nombre: str):
        self.id_usuario = id_usuario
        self.nombre = nombre
        self._libros_prestados = []

    @property
    def libros_prestados(self):
        return list(self._libros_prestados)

    def prestar_libro(self, libro):
        if libro in self._libros_prestados:
            raise ValueError("El usuario ya tiene este libro prestado")
        self._libros_prestados.append(libro)

    def devolver_libro(self, libro):
        if libro not in self._libros_prestados:
            raise ValueError("El usuario no tiene este libro prestado")
        self._libros_prestados.remove(libro)

    def to_dict(self):
        return {
            "id_usuario": self.id_usuario,
            "nombre": self.nombre,
            "libros_prestados": [libro.id_libro for libro in self._libros_prestados],
        }

    @classmethod
    def from_dict(cls, data):
        user = cls(data["id_usuario"], data["nombre"])
        # los libros se pueden vincular luego en Biblioteca
        return user

    def __str__(self):
        return f"{self.nombre} ({len(self._libros_prestados)} libros prestados)"
