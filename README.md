# Taller Reloj

Reloj **analógico** con tres manecillas (hora, minuto y segundo) hecho en Python
para la materia de Estructura de Datos. Cada esfera del reloj (segundos, minutos
y horas) es una **lista circular doblemente enlazada**, y la interfaz gráfica está
hecha solo con Tkinter (sin HTML, CSS ni librerías de terceros).

## Cómo ejecutarlo

```bash
python main.py
```

Requisitos: Python 3.9 o superior con Tkinter (viene incluido en Python para
Windows y macOS; en Ubuntu/Debian: `sudo apt install python3-tk`).

Pruebas unitarias:

```bash
python -m unittest discover -s tests -t .
```

## Funcionalidad adicional: alarmas

En el panel derecho se elige la hora con flechas ▲ ▼ (las horas y los minutos son
dos listas circulares dobles, así que al pasar de 23 a 0 o de 59 a 0 el valor da
la vuelta), se agrega la alarma y se ve en la lista. Cuando llega la hora el reloj
suena, el borde parpadea y aparece el botón **DISMISS**. Las alarmas se repiten
todos los días.

## Estructura del proyecto

| Archivo | Responsabilidad |
| --- | --- |
| `clock/circular_doubly_linked_list.py` | Lista circular doble con cursor (`advance`, `rewind`, `move_to`). |
| `clock/clock_time.py` | Modelo de tiempo: tres listas circulares, acarreo segundos → minutos → horas y cálculo de ángulos. |
| `clock/alarm.py` | `Alarm`, `AlarmTimeSelector` (dos listas circulares) y `AlarmManager`. |
| `clock/clock_view.py` | Dibujo de la esfera y las tres manecillas en un `Canvas`. |
| `clock/alarm_panel.py` | Panel lateral de alarmas. |
| `clock/widgets.py` | Botones planos reutilizables. |
| `clock/theme.py` | Paleta de colores. |
| `clock/app.py` | Controlador: conecta modelos y vistas y ejecuta la animación. |
| `main.py` | Punto de entrada. |

## Cómo funciona

- `ClockTime.tick()` avanza la lista de segundos; cuando esta completa una vuelta
  (`advance()` devuelve `True` al volver a la cabeza) avanza la de minutos, y esta
  a su vez la de horas.
- En cada cuadro la app lee la hora del sistema y llama a `synchronize`, que hace
  `tick()` cuando pasó exactamente un segundo (así el acarreo lo hacen las listas)
  o reinicia las listas si hubo un salto mayor.
- Los ángulos de las manecillas salen de la posición de cada lista; la manecilla de
  segundos barre de forma continua usando la fracción del segundo actual.

Módulos estándar usados: `tkinter` (interfaz), `time` (hora del sistema) y `math`
(seno y coseno para rotar las manecillas).
