#"""
# Información del dataframe
from openpyxl import load_workbook
from pathlib import Path
import io
import pandas as pd

class info_modulo():
    def __init__(self, data):
        #einicialización
        self.data = data
        
    # Crear un dataframe para la df.info()
    def frame_info(self):
        buf = io.StringIO()
        self.info(buf=buf)
        s = buf.getvalue()
        lines = [line.split() for line in s.splitlines()[3:-2]]
        return pd.DataFrame(lines)

    # Desplegar los nulos
    def despliega_null(self):
        null_columns = self.columns[self.isnull().any()]
        df_2 = pd.DataFrame(columns= ['Nombre Variable', 'Cantidad de Nulos'])
        for col in null_columns:
            nueva_fila = { 'Nombre Variable': col, 'Cantidad de Nulos': self[col].isnull().sum()}
            df_2 = pd.concat([df_2, pd.DataFrame([nueva_fila])], ignore_index=True)
        return df_2

    def despliega_nan(self):
        obj_df = self.select_dtypes(include=['object'])
        null_columns = obj_df.columns[obj_df.isna().any()]
        obj_df2 = pd.DataFrame(columns= ['Nombre Variable', 'Cantidad de Nulos'])
        for col in null_columns:
            nueva_fila = { 'Nombre Variable': col, 'Cantidad de Nulos': obj_df[col].isna().sum()}
            obj_df2 = pd.concat([obj_df2, pd.DataFrame([nueva_fila])], ignore_index=True)
        return obj_df2

    # Crear archivo excel con distintas hojas para los datos
    def ingresar_archivo(self, ruta, hoja):
        df2 = pd.DataFrame(self)
        if Path(ruta).exists():
            writer = pd.ExcelWriter(ruta, mode="a", engine = 'openpyxl')
        else:
            writer = pd.ExcelWriter(ruta, mode="w", engine = 'openpyxl')
        df2.to_excel(writer, sheet_name=hoja, index=False)
        writer.close()

    # Desplegar por pantalla los datos
    def informacion_dataframe(self , crea_archivo = 'NO', ruta = ''):
      print(f"Tamaño: {self.data.shape}")
      print("\n")
      print(f"Variables nulos: ")
      print(info_modulo.despliega_null(self.data))
      print("\n")
      print(f"Variables NAN: ")
      print(info_modulo.despliega_nan(self.data))
      print("\n")    
      print(f"Informacion dataframe: ")
      print(self.data.info())
      print("\n")
      print(f"Datos: ")
      display(self.data.sample(10))
      if crea_archivo.upper() == 'SI':
        info_modulo.ingresar_archivo(self.data.shape, ruta, 'Tamaño')
        info_modulo.ingresar_archivo(info_modulo.despliega_null(self.data), ruta, 'Nulos')
        info_modulo.ingresar_archivo(info_modulo.despliega_nan(self.data), ruta, 'NAN')
        info_modulo.ingresar_archivo(info_modulo.frame_info(self.data), ruta, 'Información')
        info_modulo.ingresar_archivo(self.data.sample(10), ruta, 'Datos')
      else:
        print("\n")
        print(f"No se realiza creación de Archivo")
        