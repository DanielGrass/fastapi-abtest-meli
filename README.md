# Aplicación FastAPI ABTest - MELI

Este proyecto es una aplicación FastAPI diseñada para analizar los resultados de pruebas A/B almacenados en una tabla Delta en AWS S3. La aplicación proporciona un endpoint API para recuperar los resultados de experimentos en una fecha específica.


## Descripción de la API

### Endpoint: Obtener Resultados de un Experimento

- **URL**: `/experiment/{experiment_name}/result`
- **Método**: `GET`
- **Parámetro de Consulta**:
  - `day` (requerido): La fecha en formato `YYYY-MM-DD` para la cual se desean obtener los resultados del experimento.

- **Respuesta**:
  - `200 OK`:
    ```json
    {
      "results": {
        "exp_name": "experiment_name",
        "day": "YYYY-MM-DD",
        "number_of_participants": NNN,
        "winner": "variant_id",
        "variants": [
          {
            "id": 1,
            "number_of_purchases": 100
          },
          {
            "id": 2,
            "number_of_purchases": 101
          }
        ]
      }
    }
    ```
  - `404 Not Found`: Si no se encuentran datos para el experimento y día especificados.
  - `500 Internal Server Error`: Para cualquier error inesperado.

**Nota**: Al especificar el `experiment_name` en la URL, reemplaza cualquier carácter `/` con `|` para evitar problemas en la ruta de la URL.
