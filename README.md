# Proyecto: Motor de Búsqueda de Documentos Invertido

Este proyecto implementa un motor de búsqueda basado en un **índice invertido**, utilizando Python 3 y AWK. El sistema cumple con los requisitos de los **Puntos 1, 2, 3 y 4**.

---

## 1. Requisitos del Sistema

Asegúrate de tener instalados:

* **Python 3** (`python3`)
* **AWK** o **gawk**
* **make**

---

## 2. Construcción y Ejecución

El proyecto se ejecuta en un entorno Unix (WSL, Linux o macOS).

### Comando principal

```bash
make all
```

Construye todo el sistema en orden y lanza el buscador interactivo.

###  Tabla de Comandos `make`

| Comando            | Acción                                                    | Archivos Involucrados     | Requisitos        |
| ------------------ | --------------------------------------------------------- | ------------------------- | ----------------- |
| `make all`         | Ejecuta el proyecto completo en orden                     | Todos                     | Puntos 1, 2, 3, 4 |
| `make docs`        | Prepara documentos individuales desde el CSV              | `src/csv_to_txt.py`       | Preparación       |
| `make index`       | Construye el índice invertido bruto (`index/raw/`)        | `src/build_index.awk`     | Punto 1           |
| `make clean_index` | Elimina stopwords y genera índice limpio (`index/clean/`) | `src/stopword_remover.py` | Puntos 2 y 4      |
| `make search`      | Lanza el buscador interactivo                             | `src/buscador.py`         | Puntos 3 y 4      |
| `make clean`       | Elimina todos los archivos generados                      | Todos                     | Limpieza          |

---

##  Archivos Principales y su Funcionalidad

| Archivo                   | Funcionalidad                                                    | Requisitos           |
| ------------------------- | ---------------------------------------------------------------- | -------------------- |
| `src/csv_to_txt.py`       | Convierte el CSV fuente en documentos individuales               | Preparación de datos |
| `src/build_index.awk`     | Normaliza, tokeniza y construye el índice invertido bruto        | Punto 1              |
| `src/stopword_remover.py` | Elimina stopwords y genera índice limpio usando recursividad     | Puntos 2 y 4         |
| `src/buscador.py`         | Motor de búsqueda; resuelve consultas con intersección recursiva | Puntos 3 y 4         |

---

##  3. Ejemplos de Pruebas Clave

| Objetivo              | Consulta           | Explicación                                                         |
| --------------------- | ------------------ | ------------------------------------------------------------------- |
| Intersección simple   | `bummer upset`     | Busca documentos que contienen ambas palabras                       |
| Intersección múltiple | `whole body itchy` | Verifica intersecciones recursivas entre múltiples listas de posteo |
| Normalización         | `BUMMER`           | Confirma insensibilidad a mayúsculas/minúsculas                     |
| Término desconocido   | `zxyqw`            | Verifica el manejo de términos inexistentes                         |
| Salida                | `SALIR`            | Termina la ejecución del programa                                   |

---
