import pandas as pd
import xlwings as xw

def read_materials_table(path="TABLA MATERIALES TP1.xlsx"):
    """
    Reads materials database from excel file
    Input:
        - path: str. Filepath
    Output:
        - tabla_materiales: Dataframe.
    """
    tabla_materiales = pd.read_excel(path, skiprows=1, usecols="B:G")
    return tabla_materiales

def add_material(material_props):
    """
    Adds new material to database
    Input:
        - material_props: Dict type object. Material properties in dictionary type object. Format:
            - Name: str
            - Den: int. Density
            - YM: float. Young Modulus
            - LF: float. Loss Factor
            - PM: float. Poisson Modulus
    """
    tabla_materiales = read_materials_table()
    ids = tabla_materiales["Id."]
    last_index = ids.iloc[-1]

    new_mat_dict = {"Id.": int(last_index) + 1, 
               "Name": material_props["Name"],
               "Den": material_props["Den"],
               "YM": material_props["YM"],
               "LF": material_props["LF"],
               "PM": material_props["PM"],
               }
    new_mat_df = pd.DataFrame(new_mat_dict, index=[0])
    sheet_name = "Hoja1"

    with xw.App(visible=False) as app:
        wb = app.books.open("TABLA MATERIALES TP1.xlsx")
        cell = f"B{last_index + 3}"
        wb.sheets(sheet_name).range(cell).value = new_mat_df.values.tolist()

        wb.save()

    print("Material agregado")


def get_materials_list():
    materials_table = read_materials_table()
    materiales_serie = materials_table["Material"]
    lista_materiales = materiales_serie.values.tolist()
    return lista_materiales