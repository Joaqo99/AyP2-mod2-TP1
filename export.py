import pandas as pd
import xlwings as xw

def exportar_datos(material, l_x, l_y, t, R_dict, f_c):
    """
    Exportación de datos a planilla principal
    Input:
        - material: str type object. Material name.
        - l_x: float type object. Wall width [m].
        - l_y: float type object. Wall height [m].
        - t: float type object. Wall lenght [mm].
        - R_dict: dict type object. Transmission Loss value per method:
            - R_sharp. List type object.
            - R_davy. List type object.
            - R_cremer. List type object.
            - R_iso. List type object.
        - f_c: float type object. 
    """

    if " " in material:
        material_splited = material.rsplit(" ")
        material = ""
        for i in material_splited:
            material = material + i[0].capitalize()

    new_sheet_name = f"{material}_{l_x}_{l_y}_{t}"
    if len(new_sheet_name) > 31:
        new_sheet_name = new_sheet_name[:30]

    R_dict = {
        "cremer": R_dict["R_cremer"],
        "sharp": R_dict["R_sharp"],
        "davy": R_dict["R_davy"],
        "iso": R_dict["R_iso"]
    }

    # Convertir el diccionario en un DataFrame
    df = pd.DataFrame.from_dict(R_dict, orient='index')

    with xw.App(visible=False) as app:
        wb = app.books.open("TP1_GRUPO X.xlsx")
        # Obtener todas las hojas

        # Revisar que no haya un nombre de hoja igual:
        current_sheets_names = [sheet.name for sheet in wb.sheets]

        if new_sheet_name in current_sheets_names:
            return "Ya hay una hoja exportada sobre este ensayo"

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

        # Determinar la celda para empezar a escribir los datos de R_dict
        celda_R = "B7"
        new_sheet.range(celda_R).value = df.values.tolist()

        # Guardar el archivo
        wb.save()
        return f"Los datos fueron exportados correctamente en la hoja {new_sheet_name}"