import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore
from sklearn.preprocessing import LabelEncoder

from tabulate import tabulate  # type: ignore


def Producto(dataset, producto_col):
    estados_productos = {}
    estados = dataset["ENTIDAD"].unique()  # Obtener los estados únicos

    for estado in estados:
        productos = dataset.loc[dataset["ENTIDAD"] == estado, producto_col].unique()
        estados_productos[estado] = productos

    return estados_productos


def print_dataframe_info(df, year):
    print(f"Beneficiarios {year}\n")
    df.info()
    print("\n" + "-" * 50 + "\n")


def print_summary(df, year):
    description = df.describe()
    description_list = description.reset_index().values.tolist()
    columns = list(description.columns)
    columns.insert(0, "Attribute")  # Agregar el nombre de la fila de índice
    print(f"\nBeneficiarios {year}")
    print(tabulate(description_list, headers=columns, tablefmt="grid"))
    # sesgo y curtosis
    numeric_columns = df.select_dtypes(include=["number"])
    sesgo = numeric_columns.skew()
    curtosis = numeric_columns.kurt()
    print(f"Sesgo (Skewness) de Beneficiarios {year}:")
    print(sesgo)
    print(f"\nCurtosis de Beneficiarios {year}:")
    print(curtosis)


def count_values_in_categorical_columns(df: pd.DataFrame, categorical_cols) -> dict:
    """
    Cuenta las instancias de cada valor en todas las columnas categóricas de un DataFrame.

    Parameters:
    - df: DataFrame en el que se encuentran las columnas categóricas.

    Returns:
    - dict: Diccionario con los nombres de las columnas como claves y otros diccionarios como valores.
            Los diccionarios internos tienen los valores únicos de las columnas como claves y las frecuencias como valores.
    """

    # Crear un diccionario para almacenar los conteos
    all_counts = {}

    # Iterar sobre cada columna categórica
    for col in categorical_cols:
        # Contar las instancias de cada valor en la columna
        value_counts = df[col].value_counts()
        # Convertir la Serie de conteos a un diccionario
        count_dict = value_counts.to_dict()
        # Agregar al diccionario general
        all_counts[col] = count_dict

    return all_counts


def print_describe(dataframe, year):
    # Obtener el resumen de las columnas categóricas
    categorical_description = dataframe.select_dtypes(include="object").describe()

    # Convertir el DataFrame a una lista de listas para tabulate
    categorical_description_list = categorical_description.reset_index().values.tolist()

    # Obtener los nombres de las columnas para tabulate
    columns = list(categorical_description.columns)
    columns.insert(0, "Attribute")  # Agregar el nombre de la fila de índice

    # Imprimir la tabla usando tabulate
    print(f"\nBeneficiarios {year}")
    print(tabulate(categorical_description_list, headers=columns, tablefmt="grid"))

    return


def distribucion_plot(df, year):
    # Configuración de la figura y los subplots
    fig, axs = plt.subplots(1, 3, figsize=(30, 8))

    # Histograma del Monto Federal
    sns.histplot(df["MONTO FEDERAL"], bins=30, kde=True, ax=axs[0])
    axs[0].set_title(f"Distribución del Monto Federal {year}")
    axs[0].set_xlabel("Monto Federal (MXN)")
    axs[0].set_ylabel("Frecuencia")

    # Boxplot del Monto Federal
    sns.boxplot(x=df["MONTO FEDERAL"], ax=axs[1])
    axs[1].set_title(f"Boxplot del Monto Federal {year}")
    axs[1].set_xlabel("Monto Federal (MXN)")

    # Gráfico de Barras de Beneficiarios por Entidad
    sns.countplot(
        y="ENTIDAD", data=df, order=df["ENTIDAD"].value_counts().index, ax=axs[2]
    )
    axs[2].set_title(f"Distribución de Beneficiarios por Entidad {year}")
    axs[2].set_xlabel("Número de Beneficiarios")
    axs[2].set_ylabel("Entidad")

    # Ajuste para que no se solapen los subplots
    plt.tight_layout()

    plt.show()


def label_encode(df):
    categorical_columns = df.select_dtypes(include=["object"]).columns
    label_encoders = {}

    for column in categorical_columns:
        le = LabelEncoder()
        df[column] = le.fit_transform(df[column])
        label_encoders[column] = le

    # Verifica los resultados
    return df


def correlacion(df, year):
    correlation_matrix = df.corr()
    plt.figure(figsize=(10, 8))
    sns.heatmap(
        correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5
    )
    plt.title(f"Matriz de Correlación de las Variables Numéricas {year}")
    plt.show()


def bivariado(df, year):
    fig, axs = plt.subplots(1, 2, figsize=(30, 8))

    # Boxplot
    sns.boxplot(x="ENTIDAD", y="MONTO FEDERAL", data=df, ax=axs[0])
    axs[0].tick_params(axis="x", rotation=90)  # Rotar etiquetas del eje x
    axs[0].set_title(f"Distribución del Monto Federal por Entidad {year}")
    axs[0].set_xlabel("Entidad")
    axs[0].set_ylabel("Monto Federal (MXN)")

    # Gráfico de barras apilado
    contingency_table = pd.crosstab(df["ENTIDAD"], df["ESTRATIFICACIÓN"])
    contingency_table.plot(kind="bar", stacked=True, ax=axs[1])
    axs[1].set_title(f"Relación entre Entidad y Otra Variable Categórica {year}")
    axs[1].set_xlabel("Entidad")
    axs[1].set_ylabel("Frecuencia")

    # Ajustar diseño
    plt.tight_layout()

    # Mostrar gráficos
    plt.show()
