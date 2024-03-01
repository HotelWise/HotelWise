from google.colab import drive
import pandas as pd

drive.mount('/content/drive')

ruta_hoteles= '/content/drive/MyDrive/Datasets_PF/hotelesv2.parquet'
ruta_reviews= '/content/drive/MyDrive/Datasets_PF/all-reviews.parquet'

df1= pd.read_parquet(ruta_hoteles)
df2= pd.read_parquet(ruta_reviews)

palabras_a_buscar = ['wifi', 'gym', 'restaurant', 'piscina', 'laundry', 'kindergarten', 'pool', 'parking lot',
                     'massage', 'casino', 'resort', 'fitness', 'tennis', 'taxi', 'Swimming', 'food', 'parking', 'central heating', 'central heat', 'spa']
columnas = ['descrption', 'category', 'facilities', 'text']


def merge_dataframes(df1, df2):
    # Columnas a eliminar en el primer DataFrame
    columnas_a_eliminar_df1 = ['latitude', 'longitude', 'avg_rating', 'num_of_reviews', 'url', 'County', 'City', 'State', 'Country']
    df1 = df1.drop(columns=columnas_a_eliminar_df1)
    
    # Columnas a eliminar en el segundo DataFrame
    columnas_a_eliminar_df2 = ['review_id', 'trash', 'user_id', 'name', 'time', 'rating', 'facilities', 'url']
    df2 = df2.drop(columns=columnas_a_eliminar_df2)
    
    # Realizar la fusión (join) de los DataFrames
    df3 = df1.merge(df2, on='gmap_id', how='left')
    
    # Rellenar los valores nulos con cadenas vacías
    df3.fillna('', inplace=True)
    
    return df3


def buscar_palabras_clave(df, palabras_a_buscar=None, columnas=None):

    # Solicitar al usuario las palabras clave si no se proporcionaron
    if not palabras_a_buscar:
        palabras_a_buscar = input("Ingresa las palabras clave separadas por coma: ").split(',')

    # Crear una nueva columna llamada 'amenidades' y guardar las palabras clave como lista
    df['amenidades'] = df[columnas].apply(lambda row: [word for word in palabras_a_buscar if any(word.lower() in str(cell).lower() for cell in row)], axis=1)

    # Reemplazar las listas vacías por celdas vacías
    df['amenidades'] = df['amenidades'].apply(lambda x: '' if len(x) == 0 else ', '.join(x))

    return df
  

df3 = merge_dataframes(df1, df2)
df = buscar_palabras_clave(df3, palabras_a_buscar, columnas)

final_guardar = '/content/drive/MyDrive/Datasets_PF/amenidades.csv'
df.to_csv(final_guardar, index=False)