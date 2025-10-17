# Proyecto: Modificadores de acceso en Python (POO) – Cuenta bancaria + MVVM (intro)

Este proyecto muestra, con un ejemplo simple de creación y uso de una cuenta bancaria, cómo se modelan los “modificadores de acceso” en Python usando convenciones y name mangling, además de un flujo de uso desde `main()`.

Archivos principales (versión original):
- `persona.py`: clase `Persona` con atributos público, protegido (convención) y privado (name mangling), además de una `property` con validación.
- `cuenta_bancaria.py`: clase `CuentaBancaria` con atributos público, protegido, privado y métodos para operar (depósito, retiro, transferencia).
- `oficina.py`: clase `OficinaBancaria` que orquesta apertura de cuentas y transferencias entre cuentas.
- `main.py`: función `main()` que ejecuta una demostración práctica de accesos y errores controlados.

---

## Nueva demo con arquitectura MVVM (intro en 3 paquetes)

Se añadió una variante mínima de MVVM para separar responsabilidades:

- `domain/`: modelo de dominio puro.
- `presentation/`: ViewModel con estado observable y comandos.
- `ui/`: vista CLI que se suscribe al ViewModel.
- `app/main.py`: punto de entrada que compone dominio → ViewModel → vista.

Estructura:

```
domain/
  __init__.py
  account.py
presentation/
  __init__.py
  observable.py
  account_vm.py
ui/
  __init__.py
  account_cli.py
app/
  main.py
```

### Cómo ejecutar la demo MVVM

```bash
python -m app.main
```

Comandos dentro de la CLI:

- `d <monto>`: depositar.
- `r <monto> <pin>`: retirar (PIN inicial: `1234`).
- `q`: salir.

## Cómo ejecutar

```bash
python main.py
```

Verás salidas que demuestran accesos permitidos, advertencias de acceso “protegido”, errores por acceso a privados y validaciones.

## Modificadores de acceso en Python (convenciones y name mangling)

Python no tiene modificadores de acceso “estrictos” como `public`, `protected` o `private` del mundo Java/C#. En su lugar, se usan convenciones de nombres y un mecanismo de name mangling para indicar la intención de encapsulación.

- **Público** (sin guiones bajos):
  - Ejemplo: `Persona.nombre`, `CuentaBancaria.numero_cuenta`
  - Acceso libre desde cualquier lugar.

- **Protegido** (un guion bajo `_` al inicio):
  - Ejemplo: `Persona._dni`, `CuentaBancaria._saldo`, `OficinaBancaria._cuentas`
  - Convención: “esto es para uso interno de la clase o subclases”. Python no bloquea el acceso, pero es una señal para no usarlo desde fuera.

- **Privado** (dos guiones bajos `__` al inicio):
  - Ejemplo: `Persona.__edad`, `CuentaBancaria.__pin`, `OficinaBancaria.__fondos_reserva`
  - Activa el name mangling: internamente Python renombra el atributo a `_<Clase>__<nombre>`. Por eso, `obj.__pin` falla, pero `obj._CuentaBancaria__pin` funciona (aunque no es recomendado). Sirve para evitar colisiones de nombres y reforzar la encapsulación.

- **Properties para controlar acceso a privados**:
  - `Persona` expone `edad` como `@property` para leer y `@edad.setter` para validar el valor antes de asignar al atributo privado `__edad`.

### Ejemplos en este proyecto

- `persona.py`:
  - Público: `nombre`
  - Protegido: `_dni`
  - Privado: `__edad` (acceso a través de la property `edad`)

- `cuenta_bancaria.py`:
  - Público: `numero_cuenta`, `saldo` (property de solo lectura), `depositar`, `retirar`, `transferir_a`, `consultar_saldo`, `cambiar_pin`
  - Protegido: `_saldo`, `_validar_monto`, `_requerir_pin`, `_validar_pin_formato`
  - Privado: `__pin`, `__establecer_pin_inicial`

- `oficina.py`:
  - Público: `abrir_cuenta`, `obtener_cuenta`, `transferir`, `total_depositado`
  - Protegido: `_cuentas`, `_resumen_interno`
  - Privado: `__fondos_reserva`

## ¿Por qué a veces se ve una flecha `-> tipo` en métodos?

En Python moderno se pueden anotar tipos en funciones y métodos con “type hints”. La flecha `->` indica el tipo de retorno de una función. Por ejemplo:

```python
def sumar(a: int, b: int) -> int:
    return a + b
```

- `a: int` y `b: int` anotan los parámetros.
- `-> int` indica que la función retorna un `int`.

Estas anotaciones son opcionales: documentan, ayudan a herramientas de análisis y mejoran la legibilidad, pero no cambian la ejecución (Python no valida tipos estrictamente en runtime por defecto). En este proyecto retiramos esas anotaciones para alinearnos con tu curso actual, pero es común encontrarlas en código profesional.

## Flujo de la demo original (`main.py`)

`main()` ejecuta tres demostraciones:
1. Persona: acceso a `nombre` (público), lectura/validación de `edad` (privado mediante property), acceso al protegido `_dni`, error por leer `__edad` directamente y ejemplo de name mangling.
2. CuentaBancaria: depósito, retiro con PIN correcto, intento con PIN incorrecto, consulta de saldo; muestra diferencia entre protegido `_saldo` y privado `__pin`.
3. OficinaBancaria: apertura de cuentas, transferencia, total depositado, uso de método “protegido” `_resumen_interno` y fallo al leer `__fondos_reserva`.

## Buenas prácticas

- Evita usar fuera de su clase atributos/métodos con `_` o `__`.
- Expón operaciones con métodos públicos y usa `properties` cuando necesites validación.
- Recuerda: el name mangling refuerza encapsulación, pero no es un mecanismo de seguridad.

- doc
- https://www.geeksforgeeks.org/python/name-mangling-in-python/

---

## Integración: Firebase Realtime Database (CRUD básico)

Esta rama añade una integración mínima con Firebase RTDB, respetando la separación MVVM:

- `data/firebase_service.py`: servicio de datos con operaciones CRUD (`create/read/update/delete/list`).
- `domain/account.py`: agrega `to_dict()` y `from_dict()` para serialización.
- `presentation/account_vm.py`: expone comandos `guardar`, `cargar`, `eliminar`, `listar` usando el servicio.
- `ui/account_cli.py`: añade comandos CLI para CRUD.

### Requisitos

Instala dependencias:

```bash
pip install -r requirements.txt
```

Variables de entorno necesarias:

- `FIREBASE_DB_URL`: URL de tu RTDB (por ejemplo `https://<project-id>-default-rtdb.firebaseio.com`).
- `FIREBASE_CREDENTIALS_JSON`: Ruta al JSON de credenciales de servicio o el contenido JSON literal.

En PowerShell:

```powershell
$env:FIREBASE_DB_URL = "https://<tu-project>-default-rtdb.firebaseio.com"
$env:FIREBASE_CREDENTIALS_JSON = "D:\ruta\a\serviceAccount.json"
```

También puedes pegar el contenido JSON directamente:

```powershell
$env:FIREBASE_CREDENTIALS_JSON = '{"type":"service_account", ... }'
```

### Uso desde la CLI

Ejecuta la app habitual:

```bash
python -m app.main
```

Comandos adicionales:

- `new <num> <titular> <pin>`: crea una cuenta local en memoria.
- `save`: guarda/crea en RTDB usando `num` como clave.
- `load <num>`: carga desde RTDB y sustituye la cuenta activa.
- `del <num>`: elimina la entrada en RTDB.
- `list`: lista todas las cuentas almacenadas bajo `accounts/`.

Notas:

- El PIN no se persiste en RTDB (solo `numero_cuenta`, `titular`, `saldo`). Al cargar, el PIN queda como `"0000"` por defecto; puedes cambiarlo con `cambiar_pin`.
- El servicio usa la ruta base `accounts/` en RTDB; puedes cambiarla instanciando `FirebaseRealtimeService(base_path="otra/ruta")`.

### Inyección del servicio

Para habilitar Firebase en tiempo de ejecución, crea el servicio y pásalo al ViewModel en `app/main.py`:

```python
from data.firebase_service import FirebaseRealtimeService
storage = FirebaseRealtimeService(base_path="accounts")
vm = CuentaViewModel(cuenta, storage)
```
