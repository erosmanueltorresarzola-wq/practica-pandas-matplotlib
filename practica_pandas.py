"""
Tecnológico Nacional de México · Instituto Tecnológico de Ciudad Madero
Departamento de Sistemas y Computación
Ingeniería en Sistemas Computacionales

Asignatura: Tópicos Avanzados de Programación
Docente: Dr. Alejandro Estrada Padilla
Práctica de Laboratorio: Análisis y visualización de calificaciones con Pandas y Matplotlib

Alumno: Eros Manuel Torres Arzola
"""

import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Asegurar codificación utf-8 en la consola
if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass


def main():
    print("=" * 70)
    print("PRÁCTICA DE LABORATORIO: PANDAS Y MATPLOTLIB")
    print("Tópicos Avanzados de Programación - ITCM")
    print("=" * 70)

    # -------------------------------------------------------------------------
    # EJERCICIO 1: Carga y revisión
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EJERCICIO 1: CARGA Y REVISIÓN DEL DATASET")
    print("=" * 70)

    # Cargar calificaciones_isc.csv en un DataFrame llamado df
    csv_path = "calificaciones_isc.csv"
    if not os.path.exists(csv_path):
        raise FileNotFoundError(f"No se encontró el archivo '{csv_path}' en la ruta actual.")

    df = pd.read_csv(csv_path)

    # 1. Primeras 5 filas
    print("\n--- Primeras 5 filas (df.head()) ---")
    print(df.head())

    # 2. Número de filas y de columnas
    filas, columnas = df.shape
    print(f"\n--- Dimensiones del DataFrame (df.shape) ---")
    print(f"Número de filas: {filas}")
    print(f"Número de columnas: {columnas}")

    # 3. Tipo de dato de cada columna
    print("\n--- Tipos de datos por columna (df.dtypes) ---")
    print(df.dtypes)

    # 4. Resumen estadístico de calificacion y de asistencias
    print("\n--- Resumen estadístico de calificacion y asistencias (df.describe()) ---")
    print(df[["calificacion", "asistencias"]].describe())

    # Comentario requerido por el Ejercicio 1:
    # ¿Por qué el archivo tiene 288 registros y no 24?
    # El archivo contiene 288 registros porque hay 24 alumnos en total,
    # y cada alumno está evaluado en 4 materias distintas (Programación, Bases de datos,
    # Redes y Matemáticas discretas), donde cada materia tiene 3 unidades evaluadas.
    # Por lo tanto: 24 alumnos × 4 materias × 3 unidades = 288 registros.

    # -------------------------------------------------------------------------
    # EJERCICIO 2: Filtros
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EJERCICIO 2: FILTROS (SIN MODIFICAR df)")
    print("=" * 70)

    # Filtro 1: Solo el grupo A
    filtro_grupo_a = df[df["grupo"] == "A"]
    conteo_grupo_a = len(filtro_grupo_a)
    print(f"- Registros pertenecientes unicamente al Grupo A: {conteo_grupo_a}")

    # Filtro 2: Unidades con calificacion menor a 70
    filtro_menor_70 = df[df["calificacion"] < 70]
    conteo_menor_70 = len(filtro_menor_70)
    print(f"- Unidades con calificacion menor a 70 (reprobatorias): {conteo_menor_70}")

    # Filtro 3: Bases de datos, del grupo B, con calificacion de al menos 80
    filtro_bd_b_80 = df[
        (df["materia"] == "Bases de datos") & 
        (df["grupo"] == "B") & 
        (df["calificacion"] >= 80)
    ]
    conteo_bd_b_80 = len(filtro_bd_b_80)
    print(f"- Bases de datos, del Grupo B, con calificacion >= 80: {conteo_bd_b_80}")

    # -------------------------------------------------------------------------
    # EJERCICIO 3: Columna calculada
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EJERCICIO 3: COLUMNA CALCULADA (situacion)")
    print("=" * 70)

    # Crear columna situacion con np.where (vectorizado sin ciclos)
    # Valor "Aprobado" si calificacion >= 70, de lo contrario "Reprobado"
    df["situacion"] = np.where(df["calificacion"] >= 70, "Aprobado", "Reprobado")
    print("Columna 'situacion' agregada exitosamente.")
    print("\n--- Muestra de las primeras 8 filas con la columna 'situacion' ---")
    print(df[["matricula", "nombre", "materia", "unidad", "calificacion", "situacion"]].head(8))

    # -------------------------------------------------------------------------
    # EJERCICIO 4: Resúmenes
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EJERCICIO 4: RESÚMENES ESTADÍSTICOS Y EXPORTACIÓN CSV")
    print("=" * 70)

    # 1. Promedio de calificación por materia
    print("\n1. Promedio de calificación por materia:")
    promedio_por_materia = df.groupby("materia")["calificacion"].mean().round(2)
    print(promedio_por_materia.to_string())

    # 2. Promedio por grupo y materia
    print("\n2. Promedio de calificación por grupo y materia:")
    promedio_grupo_materia = df.groupby(["grupo", "materia"])["calificacion"].mean().round(2)
    print(promedio_grupo_materia.to_string())

    # 3. Promedio general de cada alumno, ordenado de mayor a menor
    print("\n3. Promedio general de cada alumno (ordenado de mayor a menor):")
    promedios_alumnos = (
        df.groupby(["matricula", "nombre"])["calificacion"]
        .mean()
        .round(2)
        .reset_index()
        .rename(columns={"calificacion": "promedio"})
        .sort_values(by="promedio", ascending=False)
    )
    print(promedios_alumnos.to_string(index=False))

    # 4. Promedio general por unidad, con todas las materias juntas
    print("\n4. Promedio general por unidad (todas las materias):")
    promedio_por_unidad = df.groupby("unidad")["calificacion"].mean().round(2)
    print(promedio_por_unidad.to_string())

    # 5. Cuántas unidades salieron aprobadas y cuántas reprobadas
    print("\n5. Conteo de unidades aprobadas y reprobadas:")
    conteo_situacion = df["situacion"].value_counts()
    print(conteo_situacion.to_string())

    # Exportar promedio por alumno a promedios_alumnos.csv sin índice
    archivo_exportacion = "promedios_alumnos.csv"
    promedios_alumnos.to_csv(archivo_exportacion, index=False)
    print(f"\nArchivo exportado exitosamente a: '{archivo_exportacion}'")

    # -------------------------------------------------------------------------
    # EJERCICIO 5: Gráficas con Matplotlib
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EJERCICIO 5: GENERACIÓN DE GRÁFICAS")
    print("=" * 70)

    # Configuración de estilo visual general
    plt.rcParams["font.sans-serif"] = "DejaVu Sans"
    plt.rcParams["axes.edgecolor"] = "#333333"
    plt.rcParams["axes.linewidth"] = 0.8

    # --- Gráfica 1: Barras del promedio por materia ---
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    materias = promedio_por_materia.index.tolist()
    valores_materia = promedio_por_materia.values.tolist()
    colores_barras = ["#2b5c8f", "#d95f02", "#7570b3", "#1b9e77"]

    barras = ax1.bar(materias, valores_materia, color=colores_barras, width=0.55, edgecolor="#222222", zorder=3)
    ax1.set_ylim(0, 100)
    ax1.set_title("Promedio de Calificación por Materia", fontsize=14, fontweight="bold", pad=12)
    ax1.set_xlabel("Materia", fontsize=11, fontweight="bold")
    ax1.set_ylabel("Calificación Promedio (0 - 100)", fontsize=11, fontweight="bold")
    ax1.grid(axis="y", linestyle="--", alpha=0.6, zorder=0)

    # Agregar etiquetas con el valor numérico en cada barra
    for barra in barras:
        altura = barra.get_height()
        ax1.annotate(f"{altura:.2f}",
                     xy=(barra.get_x() + barra.get_width() / 2, altura),
                     xytext=(0, 4),
                     textcoords="offset points",
                     ha="center", va="bottom", fontsize=10, fontweight="bold")

    # Línea de referencia aprobatoria (70)
    ax1.axhline(70, color="#d9534f", linestyle=":", linewidth=1.5, label="Mínimo aprobatorio (70)")
    ax1.legend(loc="upper right")

    plt.tight_layout()
    # Guardar ANTES de mostrar (requisito crítico del PDF)
    plt.savefig("promedio_materias.png", dpi=300)
    print("[OK] Grafica 1 guardada: promedio_materias.png")
    plt.close(fig1)

    # --- Gráfica 2: Histograma de todas las calificaciones ---
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    n, bins, parches = ax2.hist(df["calificacion"], bins=10, color="#3470a3", edgecolor="white", alpha=0.85, zorder=3)
    
    # Línea vertical en el 70
    ax2.axvline(70, color="#e74c3c", linestyle="--", linewidth=2, label="Límite aprobatorio (70)")

    ax2.set_title("Distribución de Todas las Calificaciones Registradas", fontsize=14, fontweight="bold", pad=12)
    ax2.set_xlabel("Calificación Obtenida", fontsize=11, fontweight="bold")
    ax2.set_ylabel("Frecuencia (Número de registros)", fontsize=11, fontweight="bold")
    ax2.grid(axis="y", linestyle="--", alpha=0.6, zorder=0)
    ax2.legend(loc="upper right")

    plt.tight_layout()
    # Guardar ANTES de mostrar
    plt.savefig("histograma.png", dpi=300)
    print("[OK] Grafica 2 guardada: histograma.png")
    plt.close(fig2)

    # --- Gráfica 3: Líneas del promedio por unidad (una línea por materia) ---
    fig3, ax3 = plt.subplots(figsize=(9, 5.5))
    promedio_materia_unidad = df.groupby(["unidad", "materia"])["calificacion"].mean().unstack()

    marcadores = ["o", "s", "^", "D"]
    colores_lineas = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728"]

    for idx, col in enumerate(promedio_materia_unidad.columns):
        ax3.plot(promedio_materia_unidad.index, promedio_materia_unidad[col],
                 marker=marcadores[idx % len(marcadores)],
                 color=colores_lineas[idx % len(colores_lineas)],
                 linewidth=2.2, markersize=7, label=col, zorder=3)
        # Añadir valor en cada punto
        for u in promedio_materia_unidad.index:
            val = promedio_materia_unidad.loc[u, col]
            ax3.annotate(f"{val:.1f}", (u, val), textcoords="offset points", xytext=(0, 7),
                         ha="center", fontsize=8.5)

    ax3.set_title("Tendencia del Promedio por Unidad según Materia", fontsize=14, fontweight="bold", pad=12)
    ax3.set_xlabel("Unidad de Evaluación", fontsize=11, fontweight="bold")
    ax3.set_ylabel("Calificación Promedio", fontsize=11, fontweight="bold")
    ax3.set_xticks([1, 2, 3])
    ax3.set_xticklabels(["Unidad 1", "Unidad 2", "Unidad 3"])
    ax3.grid(True, linestyle="--", alpha=0.6, zorder=0)
    ax3.axhline(70, color="gray", linestyle=":", linewidth=1, label="Aprobatorio (70)")
    ax3.legend(title="Materias", loc="best")

    plt.tight_layout()
    # Guardar ANTES de mostrar
    plt.savefig("tendencia_unidades.png", dpi=300)
    print("[OK] Grafica 3 guardada: tendencia_unidades.png")
    plt.close(fig3)

    # -------------------------------------------------------------------------
    # EJERCICIO 6: Lectura de resultados e interpretación
    # -------------------------------------------------------------------------
    print("\n" + "=" * 70)
    print("EJERCICIO 6: INTERPRETACIÓN Y LECTURA DE RESULTADOS")
    print("=" * 70)
    interpretacion = """
RESPUESTAS A LAS PREGUNTAS DEL EJERCICIO 6:

1. ¿Qué materia quedó con el promedio más bajo?
   -> La materia con el promedio más bajo fue "Matemáticas discretas" con una calificación
      promedio de 66.08 (siendo la única materia por debajo del umbral aprobatorio de 70).
      En contraste, "Redes" obtuvo el promedio más alto con 76.03, seguida de "Bases de datos"
      con 73.85 y "Programación" con 72.97.

2. ¿El promedio general de la unidad 3 es menor que el de las unidades 1 y 2?
   -> Sí, efectivamente. El promedio de la Unidad 3 es de 69.79, el cual es menor que el de la
      Unidad 1 (73.75) y que el de la Unidad 2 (73.16). En la gráfica de tendencias se observa
      una caída general del rendimiento académico hacia la Unidad 3 en materias como
      Programación y Matemáticas discretas.

3. ¿Cuántos alumnos quedan bajo 70 en su promedio general?
   -> Quedan exactamente 7 alumnos (de un total de 24) con un promedio general inferior a 70:
      - Ana López: 69.92
      - Iván Ramírez: 69.92
      - Fernanda Rodríguez: 69.50
      - Diana Hernández: 69.08
      - Gabriel Sánchez: 67.92
      - Víctor Ramos: 66.17
      - Kevin Gómez: 64.08
"""
    print(interpretacion)
    print("=" * 70)
    print("PROCESO COMPLETADO EXITOSAMENTE")
    print("=" * 70)


if __name__ == "__main__":
    main()
