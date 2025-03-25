# Scraper SISAP - Monitoreo de Precios Agrícolas 🥔

[![Licencia MIDAGRI](https://img.shields.io/badge/Licencia-MIDAGRI-blue)](https://www.gob.pe/midagri)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-yellowgreen)
![Bibliotecas](https://img.shields.io/badge/Selenium%20%7C%20Pandas%20%7C%20Openpyxl-orange)

**Herramienta colaborativa para investigadores PUCP**  
Extracción y análisis de datos oficiales de precios agrícolas del Ministerio de Desarrollo Agrario y Riego del Perú (MIDAGRI).

<img src="image.png" width="700" alt="Ejemplo reporte SISAP">

## 📚 Descripción
Sistema automatizado que recolecta datos del [SISAP](http://sistemas.midagri.gob.pe/sisap/portal2/ciudades/) para análisis académico, con capacidad para:

- Procesar datos desde 2015 hasta 2025
- Cubrir 24 regiones del territorio nacional
- Monitorear 50+ variedades de productos
- Generar reportes diarios de mercados mayoristas/minoristas

**Fuente oficial:**  
`Mercados mayoristas y minoristas a nivel nacional - MINAGRI-DGESEP-DEIA-Área de Comercio`

## 🛠️ Tecnologías Clave
| Componente | Función |
|------------|---------|
| **Selenium** | Automatización de navegación web |
| **Pandas** | Procesamiento de datos tabulares |
| **Openpyxl** | Generación de archivos Excel |
| **FileLock** | Gestión segura de registros |

## 🗂️ Estructura del Proyecto
```bash
scraper-sisap/
├── main.ipynb            # Notebook principal de ejecución
├── process_data.py       # Módulo de procesamiento
└── outputs/              # Datos generados
   ├── precios_mayoristas_2023.xlsx
   ├── precios_minoristas_2023.xlsx
   └── registro_procesados.json

## 
💻 Instalación
 1. Requisitos previos:

```bash
pip install selenium pandas openpyxl filelock
```

 2. Ejecución básica:
```python
from scraper import run_scraper

run_scraper(
    years=[2023],
    regions=['Lima'],
    download_folder='datos_pucp',
    check_processed=True
)
```

## 📊 Estructura de Datos
**Archivos Excel generados**

 Contienen información detallada organizada por:

AÑO | FECHA       | REGION | PRODUCTO | TIPO       | VARIABLE   | UNIDAD MEDIDA | PRECIO MIN | PRECIO PROM | PRECIO MAX
---|---|---|---|---|---|---|---|---|---|
2023 | 2023-05-01 | Lima   | Papa     | Papa Amarilla   | Mayorista  | Saco          | 105.00     | 106.50      | 108.00


### 📄 Registro JSON

```json
{
  "2023": {
    "Lima": {
      "Papa": {
        "Papa Amarilla": {
          "procesado": true,
          "ultima_actualizacion": "2023-08-21 14:30:00"
        }
      }
    }
  }
}
```

## 🤝 Colaboración PUCP

**Proyecto desarrollado para la Facultad de Ciencias Sociales con objetivos de:**

- Analizar fluctuaciones de precios históricos
    
- Identificar patrones de distribución regional
    
- Generar modelos predictivos para pequeños agricultores
    
- Apoyar investigaciones sobre seguridad alimentaria



**Próximas etapas:**

- Integración con API MIDAGRI

- Sistema de alertas tempranas

- Visualizaciones interactivas

## 📜 Créditos y Contacto

Ministerio de Desarrollo Agrario y Riego (MIDAGRI)
Sistema de Información de Abastecimiento de Productos (SISAP)
Versión 2.0 - Información útil y oportuna

© Copyright 2010 - Todos los derechos reservados
Desarrollado por la Unidad de Tecnología de la Información

Contacto Oficial:
* Av. La Universidad Nº 200. La Molina - (511) 613-5800
* Jr. Yauyos Nº 258. Lima - (511) 315-5060 / (511)315-5090
  
[⬆️ Volver al inicio](#scraper-sisap---monitoreo-de-precios-agrícolas-)
