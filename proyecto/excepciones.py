"""
excepciones.py
Excepciones PERSONALIZADAS del sistema de reservas.

Una excepción personalizada es un error con nombre propio. Así, cuando algo
falla, el mensaje explica exactamente qué pasó (por ejemplo "el servicio no
está disponible") en lugar de un error genérico de Python.
"""


class ErrorReservas(Exception):
    """Error base: todos los errores de este sistema heredan de esta clase."""
    pass  # No necesita nada más; sirve para agrupar todos los errores propios


class DatosInvalidosError(ErrorReservas):
    """Se lanza cuando los datos escritos son incorrectos (vacíos, texto en vez de número, fecha mal escrita)."""
    pass


class ServicioNoExisteError(ErrorReservas):
    """Se lanza cuando se pide un servicio que no está en el catálogo."""
    pass


class ServicioNoDisponibleError(ErrorReservas):
    """Se lanza cuando el servicio existe pero está cerrado o en mantenimiento."""
    pass


class ReservaInvalidaError(ErrorReservas):
    """Se lanza cuando la reserva rompe una regla (fecha pasada, demasiadas personas, duplicada)."""
    pass


class ReservaNoEncontradaError(ErrorReservas):
    """Se lanza cuando se quiere cancelar una reserva que no existe."""
    pass


class ErrorGuardadoError(ErrorReservas):
    """Se lanza cuando no se puede guardar el archivo con las reservas."""
    pass
