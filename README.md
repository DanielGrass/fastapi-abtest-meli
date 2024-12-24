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

  ---

  ## Cómo probar la API localmente
  Si deseas probar la API en tu entorno local:
  1. Asegúrate de tener Python y las dependencias instaladas (`fastapi`, `pandas`, `uvicorn`).
  2. Ejecuta el servidor:
  ```bash
  uvicorn main:app --reload
  ```
  3. Accede a la documentación interactiva en:
  ```
  http://127.0.0.1:8000/docs
  ```

  ---

  ## Despliegue en Heroku
  1. Usa `git` para versionar tu código.
  2. Crea un archivo `Procfile` con el siguiente contenido:
  ```
  web: uvicorn main:app --host=0.0.0.0 --port=${PORT}
  ```
  3. Haz deploy con:
  ```bash
  git push heroku main
  ```
  ## Documentación propia de la API (https://abtest-fastapi-662c944e83d2.herokuapp.com/docs)
  
              1. Dar click en Try out.
              2. Escribir el nombre del experimento (recuerda reemplazar \ por |).
              3. Escribir el dia a consultar.
              4. Dar click en Execute.
              5. Revisar responses.  