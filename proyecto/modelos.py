"""
modelos.py
Clases (objetos) del sistema: Servicio y Reserva.
"""


class Servicio:
    """Un servicio que se puede reservar (spa, restaurante, piscina...)."""

    def __init__(self, nombre, capacidad, disponible=True):
        self.nombre = nombre            # Nombre del servicio
        self.capacidad = capacidad      # Máximo de personas por reserva
        self.disponible = disponible    # True = se puede reservar, False = cerrado

    def __str__(self):
        estado = "disponible" if self.disponible else "NO disponible"
        return f"{self.nombre} (capacidad {self.capacidad}, {estado})"


class Reserva:
    """Una reserva hecha por un cliente."""

    def __init__(self, id_reserva, cliente, servicio, personas, fecha):
        self.id_reserva = id_reserva  # Número único de la reserva
        self.cliente = cliente        # Nombre del cliente
        self.servicio = servicio      # Objeto Servicio reservado
        self.personas = personas      # Cantidad de personas
        self.fecha = fecha            # Fecha de la reserva (tipo date)

    def __str__(self):
        return (f"Reserva #{self.id_reserva}: {self.cliente} - "
                f"{self.servicio.nombre} - {self.personas} persona(s) - {self.fecha}")
