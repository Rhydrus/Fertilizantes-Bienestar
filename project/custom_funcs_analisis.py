import numpy as np
import pandas as pd  # type: ignore
import matplotlib.pyplot as plt
import seaborn as sns


def calcular_minmax(dataset):
    montos = {
        "min": dataset["MONTO FEDERAL"].min(),
        "mean": dataset["MONTO FEDERAL"].mean(),
        "max": dataset["MONTO FEDERAL"].max(),
        "total": round(dataset["MONTO FEDERAL"].sum(), 2),
    }

    return montos


def plot_minmax(*montos_dicts, labels=None):
    """
    Genera un gráfico de barras comparativo para los valores mínimos, medios, máximos y totales de varios diccionarios.

    :param montos_dicts: Diccionarios con estadísticas (min, mean, max, total) obtenidos de calcular_minmax.
    :param labels: Lista opcional de etiquetas (e.g., años) para cada diccionario.
    """
    if labels is None:
        labels = [f"Data {i+1}" for i in range(len(montos_dicts))]

    min_values = [montos["min"] for montos in montos_dicts]
    mean_values = [montos["mean"] for montos in montos_dicts]
    max_values = [montos["max"] for montos in montos_dicts]
    total_values = [montos["total"] for montos in montos_dicts]

    # Crear un DataFrame con los estadísticos para cada etiqueta
    df_stats = pd.DataFrame(
        {
            "Label": labels,
            "Min": min_values,
            "Mean": mean_values,
            "Max": max_values,
            "Total": total_values,
        }
    )

    # Ancho de las barras
    bar_width = 0.3

    # Posiciones para las barras en el eje x
    r1 = np.arange(len(labels))
    r2 = [x + bar_width for x in r1]
    r3 = [x + bar_width for x in r2]

    pastel_colors = sns.color_palette("pastel", 3)

    # Crear las barras
    plt.bar(
        r1,
        min_values,
        color=pastel_colors[0],
        width=bar_width,
        edgecolor=pastel_colors[0],
        label="Min",
    )

    pastel_colors = sns.color_palette("pastel", 3)

    plt.bar(
        r2,
        mean_values,
        color=pastel_colors[1],
        width=bar_width,
        edgecolor=pastel_colors[1],
        label="Mean",
    )

    plt.bar(
        r3,
        max_values,
        color=pastel_colors[2],
        width=bar_width,
        edgecolor=pastel_colors[2],
        label="Max",
    )

    # Añadir etiquetas y título
    plt.xlabel("Categoría", fontweight="bold")
    plt.ylabel("Monto Federal (millones)", fontweight="bold")
    plt.xticks([r + bar_width for r in range(len(labels))], labels)
    plt.title("Montos Federales (Min, Mean, Max, Total) por Categoría")

    # Añadir leyenda
    plt.legend()

    # Mostrar el gráfico
    plt.show()

    return df_stats


def plot_totals(*montos_dicts, labels=None):
    """
    Genera un gráfico de barras que muestra los totales de montos federales por categoría (por ejemplo, año).

    :param montos_dicts: Diccionarios con estadísticas (min, mean, max, total) obtenidos de calcular_minmax.
    :param labels: Lista opcional de etiquetas (e.g., años) para cada diccionario.
    """
    if labels is None:
        labels = [f"Data {i+1}" for i in range(len(montos_dicts))]

    # Crear los datos de los totales por cada categoría
    totals = [montos["total"] for montos in montos_dicts]

    # Definir colores para cada barra
    pastel_colors = sns.color_palette("pastel", len(montos_dicts))

    # Crear el gráfico de barras
    plt.figure(figsize=(15, 8))
    bars = plt.bar(labels, totals, color=pastel_colors)

    # Añadir etiquetas y título
    plt.xlabel("Categoría", fontweight="bold")
    plt.ylabel("Total de Montos Federales", fontweight="bold")
    plt.title("Aumento del Total de Montos Federales por Categoría")

    # Añadir etiquetas con el monto total sobre cada barra, formateadas como moneda
    for bar, label, total in zip(bars, labels, totals):
        height = bar.get_height()
        formatted_total = "{:,}".format(total)
        plt.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            f" ${formatted_total}",
            ha="center",
            va="bottom",
            fontsize=9,
            color="black",
        )

    # Mostrar el gráfico
    plt.grid(axis="y", linestyle="--")
    plt.show()


def Entidades(dataset, columna):
    Estados = set(dataset[columna])
    Estados = list(Estados)

    return Estados


def Monto(dataset, grupo, region, Reverse):
    estados_total = {}
    for regiones in region:
        total = round(
            (dataset.loc[dataset[grupo] == regiones, "MONTO FEDERAL"].sum()), 2
        )
        estados_total[regiones] = total / 1000000

    # formato de mayor a menor
    estados_total = dict(
        sorted(estados_total.items(), key=lambda item: item[1], reverse=Reverse)
    )
    return estados_total


def Entidades_beneficiarios(dataset, figsize):
    Estados = Entidades(dataset=dataset, columna="ENTIDAD")
    Estados_Montos = Monto(
        dataset=dataset, grupo="ENTIDAD", region=Estados, Reverse=True
    )
    # Crear un dataframe con los estados y sus montos
    df_estados_montos = pd.DataFrame(
        data={
            "Estado": list(Estados_Montos.keys()),
            "Monto": list(Estados_Montos.values()),
        }
    )

    plt.figure(figsize=figsize)
    ax = plt.gca()  # Obtener el eje actual
    pastel_colors = sns.color_palette("pastel", len(Estados_Montos))
    # Gráfico de barras verticales para Estados ordenados
    bars = ax.bar(Estados_Montos.keys(), Estados_Montos.values(), color=pastel_colors)
    ax.set_title("Montos Federales por Estado(millones)")
    ax.set_ylabel("Total (MXN)")

    # Añadir los montos correspondientes en las barras
    for bar in bars:
        height = bar.get_height()  # Obtener la altura de la barra (monto)
        label = f"{height:,.2f}"  # Formatear el monto con comas y 2 decimales
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height,
            label,
            ha="center",
            va="bottom",
            color="black",
        )

    # Ajustar el espacio para evitar la superposición
    plt.tight_layout()

    # Mostrar el gráfico
    plt.show()
    return df_estados_montos


def Estados_rename(data):
    for i in range(len(data)):  # Recorre el índice de cada elemento
        # Reemplazar nombres de estados
        if data[i] == "México":
            data[i] = "MÃ©xico"  # Corrige el nombre de México
        elif data[i] == "Michoacán De Ocampo":
            data[i] = "MichoacÃ¡n de Ocampo"
        elif data[i] == "Ciudad De México":
            data[i] = "Ciudad de MÃ©xico"

    return data


def Mapa_Entidades(dataframe, shp):

    # Asumiendo que 'Entidad' es una lista obtenida de una función o DataFrame
    Entidad = Entidades(dataset=dataframe, columna="ENTIDAD")
    Entidad = [entidad.title() for entidad in Entidad]
    Entidad = Estados_rename(data=Entidad)
    print(f"Tittle: {Entidad}")

    # Crear un DataFrame con los estados beneficiarios
    beneficiarios_df = pd.DataFrame(
        {
            "NOM_ENT": Entidad,
            "Beneficiario": [1] * len(Entidad),  # 1 si es beneficiario, 0 si no lo es
        }
    )
    # Unir con el shapefile
    merged = shp.merge(beneficiarios_df, on="NOM_ENT", how="left")
    # Reemplazar NaN con 0 (no beneficiarios)
    merged["Beneficiario"] = merged["Beneficiario"].fillna(0)
    # Colorear los estados beneficiarios
    fig, ax = plt.subplots(1, 1, figsize=(15, 8))
    merged.plot(column="Beneficiario", cmap="OrRd", legend=True, ax=ax)
    ax.set_title("Estados Beneficiarios del Programa")
    plt.show()


def cosechas(dataframe):

    # Sumar la cantidad de veces que cada producto fue cosechado por estado
    producto_por_estado = (
        dataframe.groupby(["ENTIDAD", "PRODUCTO"])
        .size()
        .reset_index(name="CANTIDAD_CULTIVOS")
    )

    # Pivotar la tabla para tener los productos como columnas
    producto_pivot = producto_por_estado.pivot(
        index="ENTIDAD", columns="PRODUCTO", values="CANTIDAD_CULTIVOS"
    ).fillna(0)

    # Configuración del tamaño del gráfico
    plt.figure(figsize=(14, 8))

    # Crear el gráfico de barras apiladas
    producto_pivot.plot(kind="bar", stacked=True, colormap="tab20b", figsize=(14, 8))

    # Configuración de la gráfica
    plt.title("Cantidad de Veces que Cada Producto fue Cosechado por Estado")
    plt.xlabel("Estado")
    plt.ylabel("Cantidad de Veces Cosechado")
    plt.xticks(rotation=90)
    plt.legend(title="Producto Cultivado", bbox_to_anchor=(1.05, 1), loc="upper left")
    plt.tight_layout()

    # Mostrar gráfico
    plt.show()
    # Mostrar el resultado
    print(producto_por_estado)

    return producto_por_estado
