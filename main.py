from fastapi import FastAPI, HTTPException, Query
import pandas as pd

# Inicializar FastAPI
app = FastAPI()


# Cargar el archivo CSV en un DataFrame de pandas
data = pd.read_csv("data/df_aggregated.csv")

# Reemplazar '/' por '|' en la columna "experiment_name"
data["experiment_name"] = data["experiment_name"].str.replace("/", "|", regex=False)
@app.get("/experiment/{experiment_name}/result")
async def get_results(
    experiment_name: str, day: str = Query(..., description="The day in YYYY-MM-DD format")
):
    """
    Endpoint para obtener los resultados de un experimento en una fecha específica.
    """
    try:
        # Filtrar por experimento y día
        filtered_data = data[(data["experiment_name"] == experiment_name) & (data["day"] == day)]

        # Verificar si el experimento y día existen
        if filtered_data.empty:
            raise HTTPException(
                status_code=404,
                detail=f"No data found for experiment '{experiment_name}' on day '{day}'",
            )

        # Calcular resultados
        total_participants = filtered_data["users"].sum()
        variant_data = (
            filtered_data.groupby("variant_id")["purchases"].sum().reset_index()
        )

        # Determinar ganador
        winner = variant_data.loc[variant_data["purchases"].idxmax(), "variant_id"]

        # Crear la salida
        variants = [
            {
                "id": int(row["variant_id"]),
                "number_of_purchases": int(row["purchases"]),
            }
            for _, row in variant_data.iterrows()
        ]

        return {
            "results": {
                "exp_name": experiment_name,
                "day": day,
                "number_of_participants": int(total_participants),
                "winner": int(winner),
                "variants": variants,
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Integración con AWS Lambda usando Mangum
handler = Mangum(app)
