# presentation/observable.py
from typing import Callable, List, Any


class Observable:
    """
    Observable minimalista para patrón MVVM.

    Permite suscribirse a cambios de valor.
    Cada vez que se actualiza `value`, se notifican los suscriptores.
    """

    def __init__(self, value: Any = None):
        self._value = value
        self._subs: List[Callable[[Any], None]] = []

    def subscribe(self, callback: Callable[[Any], None]) -> None:
        """Suscribe una función que será llamada al cambiar el valor."""
        self._subs.append(callback)
        # Notifica inmediatamente el valor actual (útil para inicializar vistas)
        if self._value is not None:
            callback(self._value)

    @property
    def value(self) -> Any:
        return self._value

    @value.setter
    def value(self, new_value: Any) -> None:
        self._value = new_value
        for callback in list(self._subs):
            callback(new_value)
