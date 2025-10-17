from domain.biblioteca import Biblioteca
from data.firebase_service import FirebaseRealtimeService
from presentation.observable import Observable


class BibliotecaViewModel:
    """ViewModel para manejar la Biblioteca desde la UI o CLI."""

    def __init__(self, biblioteca: Biblioteca, storage: FirebaseRealtimeService | None = None):
        self._biblioteca = biblioteca
        self._storage = storage

        self.mensaje = Observable(None)
        self.error = Observable(None)

    def agregar_libro(self, libro):
        try:
            self._biblioteca.agregar_libro(libro)
            self.mensaje.value = f"Libro '{libro.titulo}' agregado"
        except Exception as e:
            self.error.value = str(e)

    def registrar_usuario(self, usuario):
        try:
            self._biblioteca.registrar_usuario(usuario)
            self.mensaje.value = f"Usuario '{usuario.nombre}' registrado"
        except Exception as e:
            self.error.value = str(e)

    def prestar_libro(self, id_libro, id_usuario):
        try:
            self._biblioteca.prestar_libro(id_libro, id_usuario)
            self.mensaje.value = f"Libro {id_libro} prestado a {id_usuario}"
        except Exception as e:
            self.error.value = str(e)

    def devolver_libro(self, id_libro, id_usuario):
        try:
            self._biblioteca.devolver_libro(id_libro, id_usuario)
            self.mensaje.value = f"Libro {id_libro} devuelto por {id_usuario}"
        except Exception as e:
            self.error.value = str(e)

    # --- Persistencia en Firebase ---
    def guardar(self):
        if not self._storage:
            self.error.value = "No hay conexión a Firebase"
            return
        try:
            self._storage.create("biblioteca", self._biblioteca.to_dict())
            self.mensaje.value = "Biblioteca guardada en Firebase"
        except Exception as e:
            self.error.value = str(e)

    def cargar(self):
        if not self._storage:
            self.error.value = "No hay conexión a Firebase"
            return
        try:
            data = self._storage.read("biblioteca")
            if not data:
                self.error.value = "No hay datos en Firebase"
                return
            self._biblioteca = Biblioteca.from_dict(data)
            self.mensaje.value = "Biblioteca cargada desde Firebase"
        except Exception as e:
            self.error.value = str(e)
