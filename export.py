import pandas as pd
import xlwings as xw

def exportar_datos(material, l_x, l_y, t, R_dict, f_c):
    """
    Exportación de datos a planilla principal
    Input:
        - material: str type object. Material name.
        - l_x: float type object. Wall width [m].
        - l_y: float type object. Wall height [m].
        - t: float type object. Wall thickness [mm].
        - R_dict: dict type object. Transmission Loss value per method:
            - R_sharp. List type object.
            - R_davy. List type object.
            - R_cremer. List type object.
            - R_iso. List type object.
        - f_c: float type object. 
    Output:
        - Excel file updated
        - Output message.
    """

    # Convertir el nombre del material en formato adecuado
    if " " in material:
        material_splited = material.rsplit(" ")
        material = "".join([i[0].capitalize() for i in material_splited])

    new_sheet_name = f"{material}_{l_x}_{l_y}_{t}"
    if len(new_sheet_name) > 31:
        new_sheet_name = new_sheet_name[:30]

    # Determinar el tamaño de las listas válidas en R_dict
    max_length = max(len(v) for v in R_dict.values() if v is not None)

    # Reemplazar listas None por listas vacías de tamaño max_length
    R_dict = {
        "cremer": R_dict["R_cremer"] if R_dict["R_cremer"] is not None else [None] * max_length,
        "sharp": R_dict["R_sharp"] if R_dict["R_sharp"] is not None else [None] * max_length,
        "davy": R_dict["R_davy"] if R_dict["R_davy"] is not None else [None] * max_length,
        "iso": R_dict["R_iso"] if R_dict["R_iso"] is not None else [None] * max_length
    }

    # Convertir el diccionario en un DataFrame
    df = pd.DataFrame.from_dict(R_dict, orient='index')

    with xw.App(visible=False) as app:
        wb = app.books.open("Planilla Resultados.xlsx")
        current_sheets_names = [sheet.name for sheet in wb.sheets]

        i = 0
        while new_sheet_name in current_sheets_names:
            i += 1
            new_sheet_name = new_sheet_name + f" ({i})"

        current_sheets = wb.sheets
        if current_sheets[0].name == "Plantilla":
            new_sheet = current_sheets[0]
            new_sheet.name = new_sheet_name
        else:
            new_sheet = current_sheets[0].copy(name=new_sheet_name)

        # Escribir los datos básicos en las celdas correspondientes
        new_sheet.range("B1").value = material
        new_sheet.range("B2").value = l_x
        new_sheet.range("B3").value = l_y
        new_sheet.range("B4").value = t

        # Escribir los datos de R_dict
        celda_R = "B7"
        new_sheet.range(celda_R).value = df.values.tolist()

        # Guardar el archivo
        wb.save()
        return f"Los datos fueron exportados correctamente en la hoja {new_sheet_name}"


def informe(file_path, material, l_x, l_y, t, R_dict):
    """
    Genera informe
    Input:
        - file_path
        - material: str type object. Material name.
        - l_x: float type object. Wall width [m].
        - l_y: float type object. Wall height [m].
        - t: float type object. Wall thickness [mm].
        - R_dict: dict type object. Transmission Loss value per method:
            - R_sharp. List type object.
            - R_davy. List type object.
            - R_cremer. List type object.
            - R_iso. List type object.
    """
    def gen_descripcion(metodo):
        descripcion = f"Predicción de índice de reducción sonora mediante método {metodo}. Pared de {material}, {l_x} m de largo, {l_y} m de alto y {t} mm de espesor"
        return descripcion

    # Determinar el tamaño de las listas válidas en R_dict
    max_length = max(len(v) for v in R_dict.values() if v is not None)

    # Reemplazar listas None por listas vacías de tamaño max_length
    R_dict = {
        "cremer": R_dict["R_cremer"] if R_dict["R_cremer"] is not None else [None] * max_length,
        "sharp": R_dict["R_sharp"] if R_dict["R_sharp"] is not None else [None] * max_length,
        "davy": R_dict["R_davy"] if R_dict["R_davy"] is not None else [None] * max_length,
        "iso": R_dict["R_iso"] if R_dict["R_iso"] is not None else [None] * max_length
    }

    hoja_metodo_informe = {
        "Cremer": "Informe Rw 1",
        "Sharp": "Informe Rw 2",
        "Davy": "Informe Rw 3",
        "ISO 12354-1": "Informe Rw 4"
    }

    # Convertir el diccionario en un DataFrame
    df = pd.DataFrame.from_dict(R_dict, orient='index')

    with xw.App(visible=False) as app:
        plantilla_path = "plantilla_informe.xlsx"
        wb = app.books.open(plantilla_path)

        # Guardar una copia de la plantilla en el file_path especificado
        wb.save(file_path)
        wb = app.books.open(file_path)  # Abrir la copia para trabajar en ella

        # Escribir los datos de R_dict
        celda_R = "C10"
        wb.sheets["Datos entrada"].range(celda_R).value = df.values.tolist()

        for metodo in hoja_metodo_informe.keys():
            descripcion = gen_descripcion(metodo)
            celda_desc = "C9"
            wb.sheets[hoja_metodo_informe[metodo]].range(celda_desc).value = descripcion

        # Guardar y cerrar la copia del archivo
        wb.save()
        return f"Los datos fueron exportados exitosamente en {file_path}"