import json
import os
from typing import Any, Dict, Optional
from dotenv import load_dotenv  # 👈 Para leer variables del archivo .env

try:
    import firebase_admin
    from firebase_admin import credentials, db
except ImportError:
    firebase_admin = None  # type: ignore
    credentials = None  # type: ignore
    db = None  # type: ignore


class FirebaseRealtimeService:
    """
    Servicio de acceso a Firebase Realtime Database (RTDB).

    Usa variables de entorno:
      - FIREBASE_CREDENTIALS_JSON: ruta al archivo de credenciales o JSON embebido.
      - FIREBASE_DB_URL: URL del RTDB (https://<project-id>-default-rtdb.firebaseio.com)

    Permite operaciones CRUD sobre una colección base (por defecto: 'accounts').
    """

    def __init__(self, base_path: str = "accounts"):
        # ✅ Carga el archivo .env antes de usar las variables
        load_dotenv()
        self.base_path = base_path.strip("/")
        self._ensure_sdk_initialized()

    # ---------------------------------------------------------------------
    # 🔧 Inicialización del SDK de Firebase
    # ---------------------------------------------------------------------
    def _ensure_sdk_initialized(self) -> None:
        if firebase_admin is None:
            raise RuntimeError(
                "El paquete 'firebase-admin' no está instalado. Instálalo con:\n"
                "   pip install firebase-admin"
            )

        # Evita inicializar más de una vez
        if not firebase_admin._apps:  # type: ignore[attr-defined]
            creds_source = os.getenv("FIREBASE_CREDENTIALS_JSON")
            db_url = os.getenv("FIREBASE_DB_URL")

            # 🔍 Debug opcional (puedes comentar estas líneas si no las necesitas)
            # print("FIREBASE_DB_URL:", db_url)
            # print("FIREBASE_CREDENTIALS_JSON:", creds_source)

            if not db_url:
                raise RuntimeError("Falta la variable de entorno FIREBASE_DB_URL")

            if not creds_source:
                raise RuntimeError("Falta la variable de entorno FIREBASE_CREDENTIALS_JSON")

            # Si la variable apunta a un archivo local
            if os.path.isfile(creds_source):
                cred = credentials.Certificate(creds_source)
            else:
                # Si contiene JSON embebido
                try:
                    creds_dict = json.loads(creds_source)
                    cred = credentials.Certificate(creds_dict)
                except json.JSONDecodeError as exc:
                    raise RuntimeError(
                        "FIREBASE_CREDENTIALS_JSON inválido: no es ruta válida ni JSON correcto"
                    ) from exc

            firebase_admin.initialize_app(cred, {"databaseURL": db_url})

    # ---------------------------------------------------------------------
    # 📁 Referencia a la colección o nodo base
    # ---------------------------------------------------------------------
    def _ref(self, key: Optional[str] = None):
        path = self.base_path if key is None else f"{self.base_path}/{key}"
        return db.reference(path)

    # ---------------------------------------------------------------------
    # 🧩 Operaciones CRUD
    # ---------------------------------------------------------------------
    def create(self, key: str, data: Dict[str, Any]) -> None:
        """Crea o reemplaza un registro en Firebase."""
        if not key:
            raise ValueError("La clave (key) es requerida para crear datos.")
        self._ref(key).set(data)

    def read(self, key: str) -> Optional[Dict[str, Any]]:
        """Lee un registro por su clave."""
        if not key:
            raise ValueError("La clave (key) es requerida para leer datos.")
        value = self._ref(key).get()
        if value is None:
            return None
        if not isinstance(value, dict):
            raise ValueError(f"Formato inesperado en {key}: se esperaba un dict.")
        return value

    def update(self, key: str, partial_data: Dict[str, Any]) -> None:
        """Actualiza parcialmente un registro."""
        if not key:
            raise ValueError("La clave (key) es requerida para actualizar datos.")
        if not isinstance(partial_data, dict):
            raise TypeError("partial_data debe ser un diccionario.")
        self._ref(key).update(partial_data)

    def delete(self, key: str) -> None:
        """Elimina un registro por su clave."""
        if not key:
            raise ValueError("La clave (key) es requerida para eliminar datos.")
        self._ref(key).delete()

    def list_all(self) -> Dict[str, Dict[str, Any]]:
        """Lista todos los registros del nodo base."""
        value = self._ref().get()
        if value is None:
            return {}
        if not isinstance(value, dict):
            raise ValueError("Formato inesperado: se esperaba un dict con elementos.")
        # Solo retornamos items tipo dict (por seguridad)
        return {k: v for k, v in value.items() if isinstance(v, dict)}
