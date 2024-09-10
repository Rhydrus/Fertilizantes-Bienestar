import os
import pandas as pd


mexico_shp_path = "data/Mexico"
fertilizantes_path = "data"


def MapSHP(mexico_shp_path):  # Directorio principal
    dict_shp = {}
    for folder in os.listdir(mexico_shp_path):
        folder_path = os.path.join(mexico_shp_path, folder)
        if os.path.isdir(folder_path):  # Verifica si es una carpeta
            for archivo in os.listdir(folder_path):
                if archivo.endswith(
                    ".shp"
                ):  # Verifica si el archivo tiene la extensión .shp
                    dict_shp[folder] = os.path.join(folder_path, archivo)
                    break  # Si solo hay un archivo .shp por carpeta, puedes usar break
    return dict_shp


def Beneficiarios(year=2020):

    if year == 2021:
        df = pd.read_excel(
            "data\\raw\\listado_beneficiarios_fertilizantes_2021.xlsx",
            engine="openpyxl",
        )
    elif year == 2022:
        df = pd.read_excel(
            "data\\raw\\listado_beneficiarios_fertilizantes_2022.xlsx",
            engine="openpyxl",
        )
    elif year == 2023:
        df = pd.read_excel(
            "data\\raw\\listado_beneficiarios_fertilizantes_2023.xlsx",
            engine="openpyxl",
        )
    else:
        df = pd.read_excel(
            "data\\raw\\listado_beneficiarios_fertilizantes_2020.xlsx",
            engine="openpyxl",
        )

    return df


def obtener_rutas_shp():  # Directorio principal
    diccionario_shp = {}
    for carpeta in os.listdir(mexico_shp_path):
        ruta_carpeta = os.path.join(mexico_shp_path, carpeta)
        if os.path.isdir(ruta_carpeta):  # Verifica si es una carpeta
            for archivo in os.listdir(ruta_carpeta):
                if archivo.endswith(
                    ".shp"
                ):  # Verifica si el archivo tiene la extensión .shp
                    diccionario_shp[carpeta] = os.path.join(ruta_carpeta, archivo)
                    break  # Si solo hay un archivo .shp por carpeta, puedes usar break
    return diccionario_shp
