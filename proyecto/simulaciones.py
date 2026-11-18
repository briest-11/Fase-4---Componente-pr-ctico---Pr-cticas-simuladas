"""
simulaciones.py
Programa principal: ejecuta 16 simulaciones (válidas e inválidas) del sistema.
La aplicación NUNCA se detiene: cada error se atrapa, se anota en el log y
el programa sigue con la siguiente simulación.
"""
from datetime import date, timedelta

from excepciones import ErrorReservas
from gestor_reservas import GestorReservas
from modelos import Servicio
from registro_logs import obtener_logger, ARCHIVO_LOG

logger = obtener_logger()
resultados = {"exitosas": 0, "con_error_controlado": 0, "error_inesperado": 0}


def ejecutar(numero, descripcion, accion):
    """Ejecuta una simulación protegida con try/except/else/finally."""
    logger.info(f"--- Simulación {numero}: {descripcion} ---")
    try:
        accion()  # Ejecuta la operación a probar
    except ErrorReservas as error:
        # Error previsto (nuestras excepciones personalizadas)
        resultados["con_error_controlado"] += 1
        logger.error(f"Simulación {numero} -> {type(error).__name__}: {error}")
        if error.__cause__ is not None:  # Si hubo encadenamiento, anotamos la causa original
            logger.error(f"   Causa original: {type(error.__cause__).__name__}: {error.__cause__}")
    except Exception as error:
        # Red de seguridad: cualquier error que no esperábamos
        resultados["error_inesperado"] += 1
        logger.error(f"Simulación {numero} -> ERROR INESPERADO {type(error).__name__}: {error}")
    else:
        # Solo si no hubo errores
        resultados["exitosas"] += 1
        logger.info(f"Simulación {numero} -> completada con éxito")
    finally:
        # Siempre se ejecuta
        logger.info(f"--- Fin de la simulación {numero} ---")


def main():
    gestor = GestorReservas()
    # Catálogo de servicios (la Piscina está en mantenimiento a propósito)
    gestor.agregar_servicio(Servicio("Spa", capacidad=4))
    gestor.agregar_servicio(Servicio("Restaurante", capacidad=10))
    gestor.agregar_servicio(Servicio("Piscina", capacidad=20, disponible=False))

    # Fechas calculadas a partir de hoy para que las pruebas siempre funcionen
    manana = str(date.today() + timedelta(days=1))
    pasado = str(date.today() + timedelta(days=2))
    ayer = str(date.today() - timedelta(days=1))

    # ---- Simulaciones VÁLIDAS ----
    ejecutar(1, "Reserva válida en el Spa", lambda: gestor.crear_reserva("Ana Pérez", "Spa", 2, manana))
    ejecutar(2, "Reserva válida en el Restaurante", lambda: gestor.crear_reserva("Luis Gómez", "Restaurante", 6, pasado))
    ejecutar(3, "Cancelar una reserva existente", lambda: gestor.cancelar_reserva(2))
    ejecutar(4, "Guardar reservas en un archivo", lambda: gestor.guardar_reservas("reservas.json"))

    # ---- Simulaciones INVÁLIDAS ----
    ejecutar(5, "Cliente con nombre vacío", lambda: gestor.crear_reserva("   ", "Spa", 2, manana))
    ejecutar(6, "Cantidad de personas escrita con letras", lambda: gestor.crear_reserva("Ana", "Spa", "dos", manana))
    ejecutar(7, "Cantidad de personas negativa", lambda: gestor.crear_reserva("Ana", "Spa", -3, manana))
    ejecutar(8, "Fecha mal escrita", lambda: gestor.crear_reserva("Ana", "Spa", 2, "32/13/2026"))
    ejecutar(9, "Fecha que ya pasó", lambda: gestor.crear_reserva("Ana", "Spa", 2, ayer))
    ejecutar(10, "Servicio que no existe", lambda: gestor.crear_reserva("Ana", "Gimnasio", 2, manana))
    ejecutar(11, "Servicio no disponible (Piscina)", lambda: gestor.crear_reserva("Ana", "Piscina", 2, manana))
    ejecutar(12, "Más personas que la capacidad", lambda: gestor.crear_reserva("Ana", "Spa", 9, manana))
    ejecutar(13, "Reserva duplicada", lambda: gestor.crear_reserva("Ana Pérez", "Spa", 2, manana))
    ejecutar(14, "Cancelar una reserva que no existe", lambda: gestor.cancelar_reserva(99))
    ejecutar(15, "Guardar en una ruta inválida", lambda: gestor.guardar_reservas("/carpeta/que/no/existe/reservas.json"))
    ejecutar(16, "Dato nulo (None) como personas", lambda: gestor.crear_reserva("Ana", "Spa", None, manana))

    # ---- Resumen final ----
    logger.info(f"RESUMEN: {resultados}")
    print(f"\nListo. Revise el archivo de logs: {ARCHIVO_LOG}")


if __name__ == "__main__":
    main()
