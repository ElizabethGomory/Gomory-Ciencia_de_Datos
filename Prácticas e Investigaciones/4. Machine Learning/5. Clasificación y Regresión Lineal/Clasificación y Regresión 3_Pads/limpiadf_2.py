# Cambiar a datos numéricos y imputar valores faltantes
from sklearn.impute import KNNImputer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder
import pandas as pd

class limpiar_datos():
    def __init__(self, data):
        #einicialización
        self.data = data
        
    def transforma_a_numero(self, categorical_data_cols):
        pre_columns = categorical_data_cols
        for c in pre_columns:
            unicos = pd.DataFrame(self[c].unique())
            if (unicos.isnull().sum().any()):
              i = 0
              for i in range(len(unicos)):
                if unicos.iloc[i].notnull().all():
                  self[c] = self[c].replace(unicos.iloc[i][0], i , regex=True)
            else:
              encoder = LabelEncoder()
              self[c] = encoder.fit_transform(self[c].astype("str"))
        return self

    def imputar_eliminar_valores(self, porcnull_aceptable = 35, indicacion = 'NO'):
        categorical_data_cols  = [column for column in self.data.columns if self.data[column].dtypes == 'O']
        if categorical_data_cols != []:
          self.data = limpiar_datos.transforma_a_numero(self.data, categorical_data_cols)
        else:
          print("El dataset no cuenta con columnas categóricas")
        x_columns = self.data.columns[self.data.isnull().any()]
        if not x_columns.empty:
            for col in x_columns:
                if ( ((self.data[col].isnull().sum() * 100)/self.data.shape[0]) >= porcnull_aceptable ):
                    self.data.drop(col, axis=1, inplace=True)
                else:
                    if (indicacion.upper() == 'BORRACOL'):
                        self.data.drop(col, axis=1, inplace=True)
                    elif (indicacion.upper() == 'BORRAFILA'):
                        self.data.dropna(subset=col, how = 'any', axis=0, inplace=True)
                    elif indicacion.upper() == 'METKNN':
                        imputer = KNNImputer(n_neighbors=5, weights="uniform")
                        self.data[col] = imputer.fit_transform(self.data[col].values.reshape(-1, 1))
                    elif indicacion.upper() == 'METMEDIA':
                        model = SimpleImputer(strategy='mean')
                        self.data[col]  = model.fit_transform(self.data[col].values.reshape(-1, 1))
                    elif indicacion.upper() == 'METMODA':
                        model = SimpleImputer(strategy='most_frequent')
                        self.data[col]  = model.fit_transform(self.data[col].values.reshape(-1, 1))
                    else:
                        print("No se solicita imputar valores")
        else:
            print("No existen datos nulos que imputar")
        return self.data