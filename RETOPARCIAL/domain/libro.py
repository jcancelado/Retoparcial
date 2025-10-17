class Libro:
    """Modelo de dominio: representa un libro en la biblioteca."""

    def __init__(self, id_libro: str, titulo: str, autor: str, disponible: bool = True, categorias: list[str] = None):
        self.id_libro = id_libro
        self.titulo = titulo
        self.autor = autor
        self.disponible = disponible
        self.categorias = categorias if categorias is not None else []  # Lista de categorías

    def prestar(self):
        if not self.disponible:
            raise ValueError("El libro no está disponible")
        self.disponible = False

    def devolver(self):
        self.disponible = True

    def to_dict(self):
        return {
            "id_libro": self.id_libro,
            "titulo": self.titulo,
            "autor": self.autor,
            "disponible": self.disponible,
            "categorias": self.categorias
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            data["id_libro"],
            data["titulo"],
            data["autor"],
            data.get("disponible", True),
            data.get("categorias", [])
        )

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        cats = ", ".join(self.categorias) if self.categorias else "Sin categoría"
        return f"{self.titulo} ({self.autor}) - {estado} - Categorías: {cats}"
