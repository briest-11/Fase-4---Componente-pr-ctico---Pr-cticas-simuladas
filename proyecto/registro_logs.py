"""
registro_logs.py
Configuración del archivo de LOGS (el "diario" del sistema).

Un log es un archivo donde el programa va anotando lo que pasa: qué se hizo
bien (INFO) y qué falló (ERROR), con fecha y hora. Sirve para revisar después
qué ocurrió, aunque el usuario no haya visto la pantalla.
"""
import logging  # Módulo estándar de Python para manejar logs
import os       # Para crear la carpeta donde se guarda el log

CARPETA_LOGS = "logs"                                # Carpeta del archivo de logs
ARCHIVO_LOG = os.path.join(CARPETA_LOGS, "sistema.log")  # Ruta completa del archivo


def obtener_logger(nombre="reservas"):
    """Devuelve un logger listo para usar (escribe en archivo y en pantalla)."""
    os.makedirs(CARPETA_LOGS, exist_ok=True)  # Crea la carpeta si no existe
    logger = logging.getLogger(nombre)        # Pide el logger con ese nombre

    # Si ya fue configurado antes, lo devolvemos tal cual (evita líneas repetidas)
    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)  # Registrar desde el nivel INFO hacia arriba

    # Formato de cada línea: fecha - nivel - mensaje
    formato = logging.Formatter("%(asctime)s | %(levelname)-8s | %(message)s")

    # Destino 1: el archivo de logs (guardado permanente)
    archivo = logging.FileHandler(ARCHIVO_LOG, encoding="utf-8")
    archivo.setFormatter(formato)
    logger.addHandler(archivo)

    # Destino 2: la pantalla (para ver lo que pasa mientras se ejecuta)
    pantalla = logging.StreamHandler()
    pantalla.setFormatter(formato)
    logger.addHandler(pantalla)

    return logger
