# Sistema de reservas con manejo de excepciones

Proyecto de la Fase 4 - Prácticas simuladas (Programación 213023, UNAD).

## ¿Qué hace?
Un sistema sencillo para reservar servicios (Spa, Restaurante, Piscina). Está pensado para
**no detenerse nunca** ante errores: cada problema se atrapa, se explica con un mensaje claro
y se anota en un archivo de logs.

## Archivos
| Archivo | Para qué sirve |
|---|---|
| `excepciones.py` | Excepciones personalizadas (errores con nombre propio) |
| `registro_logs.py` | Configuración del archivo de logs (`logs/sistema.log`) |
| `modelos.py` | Clases `Servicio` y `Reserva` |
| `gestor_reservas.py` | Lógica: crear, cancelar y guardar reservas (try/except/else/finally y encadenamiento) |
| `simulaciones.py` | Programa principal: 16 simulaciones válidas e inválidas |

## Cómo ejecutarlo
```bash
python simulaciones.py
```
Después revise el archivo `logs/sistema.log`.

## Conceptos aplicados
- Excepciones personalizadas (`ErrorReservas` y sus hijas)
- `try / except`, `try / except / else`, `try / finally`
- Encadenamiento de excepciones (`raise ... from ...`)
- Logging a archivo (INFO y ERROR)

## Autor
Juan Esteban Briceño - Programación 213023, UNAD.
