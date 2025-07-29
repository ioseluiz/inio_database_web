import pandas as pd

# 1. Cargar el archivo CSV
try:
    df = pd.read_csv('Licitaciones.csv') # Reemplaza 'tu_archivo.csv' con el nombre de tu archivo
except FileNotFoundError:
    print("Error: El archivo no fue encontrado. Asegúrate de que 'tu_archivo.csv' esté en la misma carpeta o proporciona la ruta completa.")
    exit()

# 2. Identificar columnas con texto largo (ejemplo: todas las columnas de tipo 'object')
# Si sabes las columnas exactas, puedes especificarlas, por ejemplo:
# columnas_a_limpiar = ['descripcion', 'comentarios']
columnas_a_limpiar = df.select_dtypes(include=['object']).columns

# 3. Reemplazar saltos de línea en las columnas identificadas
for col in columnas_a_limpiar:
    # Reemplaza saltos de línea por un espacio. Puedes usar '' para eliminarlos por completo.
    df[col] = df[col].astype(str).str.replace(r'[\n\r]+', ' ', regex=True)

# 4. Guardar el archivo limpio
df.to_csv('tu_archivo_limpio.csv', index=False)
print("Archivo procesado y guardado como 'tu_archivo_limpio.csv'")