"""
gestor_reservas.py
Lógica principal: crear, cancelar y guardar reservas.
Aquí se usa el manejo de excepciones: raise, try/except/else/finally
y ENCADENAMIENTO de excepciones ("raise ... from ...").
"""
import json                              # Para guardar las reservas en un archivo
from datetime import datetime, date      # Para trabajar con fechas

from excepciones import (
    DatosInvalidosError, ServicioNoExisteError, ServicioNoDisponibleError,
    ReservaInvalidaError, ReservaNoEncontradaError, ErrorGuardadoError,
)
from modelos import Servicio, Reserva
from registro_logs import obtener_logger

logger = obtener_logger()  # Logger compartido para anotar eventos y errores


class GestorReservas:
    """Administra los servicios disponibles y las reservas hechas."""

    def __init__(self):
        self.servicios = {}      # Catálogo: nombre -> Servicio
        self.reservas = {}       # Reservas: id -> Reserva
        self.siguiente_id = 1    # Contador para numerar las reservas

    # ------------------------------------------------------------------
    def agregar_servicio(self, servicio):
        """Agrega un servicio al catálogo."""
        self.servicios[servicio.nombre] = servicio
        logger.info(f"Servicio agregado: {servicio}")

    # ------------------------------------------------------------------
    def _convertir_fecha(self, texto_fecha):
        """Convierte un texto 'AAAA-MM-DD' en fecha. Si está mal escrito, lanza nuestro error."""
        try:
            # strptime lanza ValueError si el texto no es una fecha válida
            return datetime.strptime(texto_fecha, "%Y-%m-%d").date()
        except (ValueError, TypeError) as error:
            # ENCADENAMIENTO: "from error" conserva el error original como causa
            raise DatosInvalidosError(
                f"La fecha '{texto_fecha}' no es válida. Use el formato AAAA-MM-DD."
            ) from error

    # ------------------------------------------------------------------
    def _validar_personas(self, personas):
        """Verifica que 'personas' sea un entero positivo."""
        try:
            # int() lanza ValueError (texto) o TypeError (None) si no puede convertir
            cantidad = int(personas)
        except (ValueError, TypeError) as error:
            raise DatosInvalidosError(
                f"La cantidad de personas '{personas}' no es un número."
            ) from error  # Encadenamos el error original
        if cantidad <= 0:
            raise DatosInvalidosError("La cantidad de personas debe ser mayor que cero.")
        return cantidad

    # ------------------------------------------------------------------
    def crear_reserva(self, cliente, nombre_servicio, personas, texto_fecha):
        """Crea una reserva validando todas las reglas. Devuelve la Reserva creada."""
        # 1. Validar el nombre del cliente
        if not isinstance(cliente, str) or not cliente.strip():
            raise DatosInvalidosError("El nombre del cliente no puede estar vacío.")

        # 2. Validar cantidad de personas y fecha (pueden lanzar DatosInvalidosError)
        cantidad = self._validar_personas(personas)
        fecha = self._convertir_fecha(texto_fecha)

        # 3. Buscar el servicio en el catálogo
        try:
            servicio = self.servicios[nombre_servicio]  # KeyError si no existe
        except KeyError as error:
            raise ServicioNoExisteError(
                f"El servicio '{nombre_servicio}' no existe en el catálogo."
            ) from error  # Encadenamiento

        # 4. Reglas de negocio
        if not servicio.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{servicio.nombre}' no está disponible.")
        if fecha < date.today():
            raise ReservaInvalidaError(f"La fecha {fecha} ya pasó; no se puede reservar.")
        if cantidad > servicio.capacidad:
            raise ReservaInvalidaError(
                f"{cantidad} personas superan la capacidad de {servicio.capacidad} del servicio."
            )
        for existente in self.reservas.values():  # Revisar que no esté duplicada
            if (existente.cliente == cliente and existente.servicio is servicio
                    and existente.fecha == fecha):
                raise ReservaInvalidaError("Ya existe una reserva igual para ese cliente, servicio y fecha.")

        # 5. Todo correcto: crear y guardar la reserva
        reserva = Reserva(self.siguiente_id, cliente, servicio, cantidad, fecha)
        self.reservas[reserva.id_reserva] = reserva
        self.siguiente_id += 1
        logger.info(f"Reserva creada -> {reserva}")
        return reserva

    # ------------------------------------------------------------------
    def cancelar_reserva(self, id_reserva):
        """Cancela una reserva por su número."""
        try:
            reserva = self.reservas.pop(id_reserva)  # KeyError si no existe
        except KeyError as error:
            raise ReservaNoEncontradaError(
                f"No existe la reserva #{id_reserva}."
            ) from error  # Encadenamiento
        logger.info(f"Reserva cancelada -> {reserva}")
        return reserva

    # ------------------------------------------------------------------
    def guardar_reservas(self, ruta):
        """Guarda las reservas en un archivo JSON. Usa try/except/else/finally."""
        archivo = None  # Se define antes para poder cerrarlo en 'finally'
        try:
            archivo = open(ruta, "w", encoding="utf-8")  # Puede fallar (ruta mala)
            datos = [
                {"id": r.id_reserva, "cliente": r.cliente, "servicio": r.servicio.nombre,
                 "personas": r.personas, "fecha": str(r.fecha)}
                for r in self.reservas.values()
            ]
            json.dump(datos, archivo, ensure_ascii=False, indent=2)  # Escribe el JSON
        except OSError as error:
            # Error del sistema de archivos -> lo convertimos en nuestro error (encadenado)
            raise ErrorGuardadoError(f"No se pudo guardar en '{ruta}'.") from error
        else:
            # Solo se ejecuta si NO hubo ningún error
            logger.info(f"Reservas guardadas correctamente en '{ruta}'.")
        finally:
            # Se ejecuta SIEMPRE: cerramos el archivo si llegó a abrirse
            if archivo is not None:
                archivo.close()
            logger.info("Intento de guardado finalizado.")
