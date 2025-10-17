from domain.biblioteca import Biblioteca
from presentation.biblioteca_vm import BibliotecaViewModel
from ui.biblioteca_cli import BibliotecaCLIView
from data.firebase_service import FirebaseRealtimeService


def main():
    service = FirebaseRealtimeService(base_path="bibliotecas")
    biblioteca = Biblioteca("Biblioteca Central")
    vm = BibliotecaViewModel(biblioteca, storage=service)
    vista = BibliotecaCLIView(vm)
    vista.demo()


if __name__ == "__main__":
    main()
