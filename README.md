# Proyecto: AB Testing - MELI Challenge by Daniel Grass
# Backend: FastAPI
## Diciembre 2024
![Logo](https://http2.mlstatic.com/frontend-assets/ml-web-navigation/ui-navigation/6.6.73/mercadolibre/logo_large_25years@2x.png?width=300)

## Descripción General
Esta API permite obtener resultados de experimentos A/B. Contiene información sobre experimentos, incluyendo el número de usuarios, variantes y compras realizadas.

La API está implementada con **FastAPI** y está desplegada en Heroku para acceso público.

## Nota Importante
En el parámetro `experiment_name`, es necesario reemplazar los caracteres `\` por `|` antes de realizar la solicitud.

## Repositorio del Proyecto
El código fuente de esta API está disponible en el siguiente repositorio de GitHub:
[fastapi-abtest-meli](https://github.com/DanielGrass/fastapi-abtest-meli)

## Estructura de la API
### Endpoint: `/experiment/{experiment_name}/result`
Este endpoint permite consultar los resultados de un experimento en una fecha específica.

#### Parámetros:
1. **experiment_name (str)**: Nombre del experimento.  
2. **day (str)**: Fecha en formato `YYYY-MM-DD`. Este parámetro es obligatorio.

#### Respuesta Exitosa (200):
Si el experimento y la fecha existen en los datos, la API devuelve:
- **exp_name**: Nombre del experimento.
- **day**: Fecha del experimento.
- **number_of_participants**: Número total de participantes en el experimento.
- **winner**: Variante ganadora basada en el mayor número de compras.
- **variants**: Lista de variantes con el número de compras realizadas.

#### Respuesta de Error (404):
Si el experimento o la fecha no existen, se devuelve un mensaje indicando que no se encontraron datos.

---

## Ejemplo de Uso
### URL Base
La API está desplegada en Heroku en la siguiente URL:
```
https://abtest-fastapi-662c944e83d2.herokuapp.com
```

### Ejemplo 1: Resultado satisfactorio
**URL**:
```
https://abtest-fastapi-662c944e83d2.herokuapp.com/experiment/qadb|sa-on-vip/result?day=2021-08-01
```

**Respuesta**:
```json
{
    "results": {
        "exp_name": "qadb|sa-on-vip",
        "day": "2021-08-01",
        "number_of_participants": 3500,
        "winner": 1,
        "variants": [
            {
                "id": 1,
                "number_of_purchases": 1500
            },
            {
                "id": 2,
                "number_of_purchases": 1200
            },
            {
                "id": 3,
                "number_of_purchases": 800
            }
        ]
    }
}
```

### Ejemplo 2: Fecha sin resultados
**URL**:
```
https://abtest-fastapi-662c944e83d2.herokuapp.com/experiment/qadb|sa-on-vip/result?day=2024-08-01
```

**Respuesta**:
```json
{
    "detail": "No data found for experiment 'qadb|sa-on-vip' on day '2024-08-01'"
}
```
## Requisitos de Instalación

Para ejecutar este proyecto, asegúrate de tener instalados los siguientes software:

- [Python 3.9](https://www.python.org/downloads/)
- [pip](https://pip.pypa.io/en/stable/installation/)

### Instalación

1. Clona el repositorio:

   ```bash
   git clone https://github.com/DanielGrass/AB-MELI.git
   cd AB-MELI

2. Crea y activa un entorno virtual:

- En Windows:

    ```bash
    python -m venv venv
    .\venv\Scripts\activate

- En macOS/Linux:

    ```bash    
    python3 -m venv venv
    source venv/bin/activate

3. Instala las dependencias:
    ```bash    
    pip install -r requirements.txt

4. Ejecuta la aplicación:
    ```bash    
    uvicorn main:app --reload

5. Accede a la documentación interactiva en:
    ```
    http://127.0.0.1:8000/docs
---

## Documentación swagger de la API (https://abtest-fastapi-662c944e83d2.herokuapp.com/docs)
          1. Dar click en Try out.
          2. Escribir el nombre del experimento (recuerda reemplazar \ por |).
          3. Escribir el dia a consultar.
          4. Dar click en Execute.
          5. Revisar responses.  