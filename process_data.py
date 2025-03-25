import pandas as pd
import io
import os
import json
from datetime import datetime

def process_table(df, region, producto, tipo, year):
    """
    Procesa una tabla HTML, la divide en datos de mayoristas y minoristas,
    y añade los metadatos correspondientes.
    
    Args:
        table_element: Elemento de tabla web obtenido con Selenium
        region: Nombre de la región
        producto: Nombre del producto
        tipo: Subtipo del producto
        
    Returns:
        tuple: (df_mayoristas, df_minoristas) DataFrames procesados
    """
    # Eliminar las filas de encabezado originales
    df = df.iloc[4:].reset_index(drop=True)
    # Definir nombres de columnas
    df.columns = ['FECHA', 'UNIDAD DE MEDIDA', 'EQUIVALENTE (KG/LT)', 
                 'PRECIO MINIMO', 'PRECIO PROMEDIO', 'PRECIO MAXIMO', 
                 'UNIDAD DE MEDIDA.1', 'EQUIVALENTE (KG/LT).1', 
                 'PRECIO MINIMO.1', 'PRECIO PROMEDIO.1', 'PRECIO MAXIMO.1']
    
    # Definir columnas para cada tipo de DataFrame
    columnas_mayoristas = ['FECHA', 'UNIDAD DE MEDIDA', 'EQUIVALENTE (KG/LT)', 
                          'PRECIO MINIMO', 'PRECIO PROMEDIO', 'PRECIO MAXIMO']
    
    columnas_minoristas = ['FECHA', 'UNIDAD DE MEDIDA.1', 'EQUIVALENTE (KG/LT).1', 
                          'PRECIO MINIMO.1', 'PRECIO PROMEDIO.1', 'PRECIO MAXIMO.1']
    
    # Crear DataFrames separados
    df_mayoristas = df[columnas_mayoristas].copy()
    df_minoristas = df[columnas_minoristas].copy()
    
    # Renombrar columnas en DataFrame de minoristas
    df_minoristas.columns = ['FECHA', 'UNIDAD DE MEDIDA', 'EQUIVALENTE (KG/LT)', 
                            'PRECIO MINIMO', 'PRECIO PROMEDIO', 'PRECIO MAXIMO']
    
    # Agregar metadatos
    df_mayoristas['AÑO'] = year
    df_mayoristas['REGION'] = region
    df_mayoristas['PRODUCTO'] = producto
    df_mayoristas['TIPO'] = tipo
    df_mayoristas['VARIABLE'] = 'Mayorista'
    
    df_minoristas['AÑO'] = year
    df_minoristas['REGION'] = region
    df_minoristas['PRODUCTO'] = producto
    df_minoristas['TIPO'] = tipo
    df_minoristas['VARIABLE'] = 'Minorista'
    
    # Reordenar columnas
    orden_columnas = ['AÑO', 'FECHA', 'REGION', 'PRODUCTO', 'TIPO', 'VARIABLE', 
                     'UNIDAD DE MEDIDA', 'EQUIVALENTE (KG/LT)', 
                     'PRECIO MINIMO', 'PRECIO PROMEDIO', 'PRECIO MAXIMO']
    
    df_mayoristas = df_mayoristas[orden_columnas]
    df_minoristas = df_minoristas[orden_columnas]
    
    # Convertir tipos de datos
    # Fecha a datetime
    df_mayoristas['FECHA'] = pd.to_datetime(df_mayoristas['FECHA'], format='%d/%m/%Y', errors='coerce').dt.date
    df_minoristas['FECHA'] = pd.to_datetime(df_minoristas['FECHA'], format='%d/%m/%Y', errors='coerce').dt.date
    
    # Valores numéricos a float
    columnas_numericas = ['EQUIVALENTE (KG/LT)', 'PRECIO MINIMO', 'PRECIO PROMEDIO', 'PRECIO MAXIMO']
    for col in columnas_numericas:
        df_mayoristas[col] = df_mayoristas[col].str.replace(',', '.').astype(float, errors='ignore')
        df_minoristas[col] = df_minoristas[col].str.replace(',', '.').astype(float, errors='ignore')
    
    return df_mayoristas, df_minoristas

def save_data(df_mayoristas, df_minoristas, year, region, producto, tipo, directorio='datos'):
    """
    Guarda los datos en archivos Excel, creándolos si no existen o
    agregando los datos si ya existen.
    
    Args:
        df_mayoristas: DataFrame con datos de precios mayoristas
        df_minoristas: DataFrame con datos de precios minoristas
        producto: Nombre del producto
        tipo: Subtipo del producto
        directorio: Directorio donde se guardarán los archivos
        
    Returns:
        None
    """
    # Crear directorio si no existe
    if not os.path.exists(directorio):
        os.makedirs(directorio)
    
    # Definir rutas de archivos
    archivo_mayoristas = os.path.join(directorio, f'precios_mayoristas_{year}.xlsx')
    archivo_minoristas = os.path.join(directorio, f'precios_minoristas_{year}.xlsx')
    
    # Guardar datos de mayoristas
    if os.path.exists(archivo_mayoristas):
        # Si el archivo existe, leer y concatenar con nuevos datos
        df_existing = pd.read_excel(archivo_mayoristas)
        df_combined = pd.concat([df_existing, df_mayoristas], ignore_index=True)
        # Eliminar duplicados basados en año, fecha, región, producto, tipo y variable
        df_combined = df_combined.drop_duplicates(
            subset=['AÑO', 'FECHA', 'REGION', 'PRODUCTO', 'TIPO', 'VARIABLE'],
            keep='last'
        )
        df_combined.to_excel(archivo_mayoristas, index=False)
    else:
        # Si no existe, crear nuevo archivo
        df_mayoristas.to_excel(archivo_mayoristas, index=False)
    
    # Guardar datos de minoristas
    if os.path.exists(archivo_minoristas):
        # Si el archivo existe, leer y concatenar con nuevos datos
        df_existing = pd.read_excel(archivo_minoristas)
        df_combined = pd.concat([df_existing, df_minoristas], ignore_index=True)
        # Eliminar duplicados basados en año, fecha, región, producto, tipo y variable
        df_combined = df_combined.drop_duplicates(
            subset=['AÑO', 'FECHA', 'REGION', 'PRODUCTO', 'TIPO', 'VARIABLE'],
            keep='last'
        )
        df_combined.to_excel(archivo_minoristas, index=False)
    else:
        # Si no existe, crear nuevo archivo
        df_minoristas.to_excel(archivo_minoristas, index=False)
    
    # Actualizar registro de productos procesados
    update_register(year, region, producto, tipo, directorio)
    
    return


def update_register(year, region, producto, tipo, directorio='datos'):
    """
    Actualiza el registro JSON de productos y subproductos procesados.
    La jerarquía será: año -> región -> producto -> tipo.
    """
    archivo_registro = os.path.join(directorio, 'registro_procesados.json')
    
    # Inicializar o cargar el registro existente
    if os.path.exists(archivo_registro):
        with open(archivo_registro, 'r', encoding='utf-8') as f:
            registro = json.load(f)
    else:
        registro = {}
    
    year_str = str(year)  # Convertir el año a string para usarlo como clave
    
    # Crear estructura jerárquica: año -> región -> producto -> tipo
    if year_str not in registro:
        registro[year_str] = {}
    
    if region not in registro[year_str]:
        registro[year_str][region] = {}
    
    if producto not in registro[year_str][region]:
        registro[year_str][region][producto] = {}
        
    # Registrar tipo con timestamp en formato YYYY-MM-DD HH:MM:SS
    registro[year_str][region][producto][tipo] = {
        'procesado': True,
        'ultima_actualizacion': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    
    # Guardar registro actualizado
    with open(archivo_registro, 'w', encoding='utf-8') as f:
        json.dump(registro, f, ensure_ascii=False, indent=4)
    
    return

def check_process(year, region, producto, tipo, directorio='datos'):
    """
    Verifica si un producto y tipo ya han sido procesados para un año y región específicos.
    
    Args:
        year: Año de los datos
        region: Región de los datos
        producto: Nombre del producto
        tipo: Subtipo del producto
        directorio: Directorio donde se guarda el registro
        
    Returns:
        bool: True si ya fue procesado, False en caso contrario
    """
    archivo_registro = os.path.join(directorio, 'registro_procesados.json')
    
    # Si no existe el archivo de registro, no se ha procesado nada
    if not os.path.exists(archivo_registro):
        return False
    
    # Cargar registro
    with open(archivo_registro, 'r', encoding='utf-8') as f:
        registro = json.load(f)
    
    year_str = str(year)  # Convertir el año a string para usarlo como clave
    
    # Verificar si el año, región, producto y tipo están registrados
    if (year_str in registro and 
        region in registro[year_str] and 
        producto in registro[year_str][region] and 
        tipo in registro[year_str][region][producto]):
        
        return registro[year_str][region][producto][tipo]['procesado']
    
    return False
# def ejemplo_uso():
#     """
#     Ejemplo de cómo usar las funciones en un scraper real.
#     Este código es solo para ilustración.
#     """
#     year = 2025  # Año actual o el que corresponda

#     # En un scraper real, esto sería parte de un bucle que itera sobre regiones, productos y tipos
#     for region in lista_regiones:
#         for producto in lista_productos:
#             for tipo in tipos_de_producto:
#                 # Verificar si ya se procesó
#                 if verificar_procesado(year, region, producto, tipo):
#                     print(f"Saltando {year} - {region} - {producto} - {tipo} (ya procesado)")
#                     continue
                    
#                 # Código para navegar a la página y obtener la tabla
#                 # ...
                
#                 # Procesar la tabla
#                 df_mayoristas, df_minoristas = procesar_tabla(
#                     table_element, 
#                     region=region, 
#                     producto=producto,
#                     tipo=tipo
#                 )
                
#                 # Guardar los datos y actualizar registro
#                 guardar_datos(df_mayoristas, df_minoristas, producto, tipo)
                
#                 # Actualizar el registro para marcar como procesado
#                 update_register(year, region, producto, tipo)
                
#                 print(f"Procesado: {year} - {region} - {producto} - {tipo}")

if __name__ == "__main__":
    # Este código se ejecuta solo si se corre el script directamente
    print("Módulo de procesamiento de datos cargado.")
    # Puedes agregar código de prueba aquí si lo deseas