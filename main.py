from fastapi import FastAPI, HTTPException, Query
from pyspark.sql import SparkSession
from pyspark.sql.functions import col, regexp_replace
from mangum import Mangum

# Inicializar FastAPI
app = FastAPI()

# Configuración de Spark
spark = SparkSession.builder \
    .appName("DeltaTableTest") \
    .config("spark.jars.packages", "io.delta:delta-core_2.12:2.4.0,org.apache.hadoop:hadoop-aws:3.3.4") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "com.amazonaws.auth.DefaultAWSCredentialsProviderChain") \
    .config("spark.python.worker.reuse", "true") \
    .getOrCreate()

# Ruta al Delta Table Gold (S3)
gold_table_path = "s3a://abtest-meli/delta-table-gold-aggregate/"
gold_df = spark.read.format("delta").load(gold_table_path)

# Ajustar los nombres en gold_df reemplazando / por |
gold_df = gold_df.withColumn("experiment_name", regexp_replace(col("experiment_name"), "/", "|"))

@app.get("/experiment/{experiment_name}/result")
async def get_results(experiment_name: str, day: str = Query(..., description="The day in YYYY-MM-DD format")):
    try:
        # Filtrar por experimento y día
        exp_data = gold_df.filter(
            (col("experiment_name") == experiment_name) & (col("day") == day)
        )

        if exp_data.count() == 0:
            raise HTTPException(status_code=404, detail=f"No data found for experiment '{experiment_name}' on day '{day}'")

        # Calcular resultados
        total_participants = exp_data.agg({"users": "sum"}).collect()[0][0]
        variant_data = exp_data.groupBy("variant_id").sum("purchases").collect()

        winner = max(variant_data, key=lambda x: x["sum(purchases)"])["variant_id"]

        variants = [{"id": row["variant_id"], "number_of_purchases": row["sum(purchases)"]} for row in variant_data]

        return {
            "results": {
                "exp_name": experiment_name,
                "day": day,
                "number_of_participants": total_participants,
                "winner": winner,
                "variants": variants
            }
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Integración con AWS Lambda usando Mangum
handler = Mangum(app)
