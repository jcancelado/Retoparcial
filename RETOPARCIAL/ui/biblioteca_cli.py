from presentation.biblioteca_vm import BibliotecaViewModel
from domain.libro import Libro
from domain.usuario import Usuario

# Lista de categorías válidas
CATEGORIAS_VALIDAS = [
    "Distopía",
    "Filosofía",
    "Política",
    "Historia",
    "Ciencia",
    "Novela",
    "Clásico"
]

class BibliotecaCLIView:
    """Vista CLI interactiva para la biblioteca."""

    def __init__(self, vm: BibliotecaViewModel):
        self.vm = vm
        self.vm.mensaje.subscribe(self._show_msg)
        self.vm.error.subscribe(self._show_err)

    def _show_msg(self, msg):
        if msg:
            print(f"[INFO] {msg}")

    def _show_err(self, err):
        if err:
            print(f"[ERROR] {err}")

    def _show_help(self):
        print("Comandos disponibles:")
        print(" - newbook <id> <titulo> <autor> <categorias>")
        print(f"   Categorías válidas: {', '.join(CATEGORIAS_VALIDAS)}")
        print(" - newuser <id> <nombre>")
        print(" - lend <id_usuario> <id_libro>")
        print(" - return <id_usuario> <id_libro>")
        print(" - save")
        print(" - load")
        print(" - list")
        print(" - help")
        print(" - exit")

    def demo(self):
        print("=== Biblioteca CLI ===")
        print("Escribe 'help' para ver los comandos disponibles.")

        while True:
            cmd = input("> ").strip().split()
            if not cmd:
                continue
            op = cmd[0].lower()

            if op == "exit":
                break

            elif op == "newbook" and len(cmd) >= 5:
                id_libro = cmd[1]
                autor = cmd[-2]
                categorias_input = cmd[-1].split(",")
                titulo = " ".join(cmd[2:-2])

                # Filtrar categorías válidas
                categorias = [cat for cat in categorias_input if cat in CATEGORIAS_VALIDAS]
                if not categorias:
                    print(f"[ERROR] Debes elegir al menos una categoría válida: {', '.join(CATEGORIAS_VALIDAS)}")
                    continue

                self.vm.agregar_libro(Libro(id_libro, titulo, autor, categorias=categorias))

            elif op == "newuser" and len(cmd) >= 3:
                id_usr = cmd[1]
                nombre = " ".join(cmd[2:])
                self.vm.registrar_usuario(Usuario(id_usr, nombre))

            elif op == "lend" and len(cmd) == 3:
                self.vm.prestar_libro(cmd[1], cmd[2])

            elif op == "return" and len(cmd) == 3:
                self.vm.devolver_libro(cmd[1], cmd[2])

            elif op == "save":
                self.vm.guardar()

            elif op == "load":
                self.vm.cargar()

            elif op == "list":
                print("Libros:")
                for libro in self.vm._biblioteca.listar_libros():
                    print(" -", libro)
                print("\nUsuarios:")
                for usuario in self.vm._biblioteca.listar_usuarios():
                    print(" -", usuario)

            elif op == "help":
                self._show_help()

            else:
                print("Comando no reconocido. Escribe 'help' para ver los comandos válidos.")
