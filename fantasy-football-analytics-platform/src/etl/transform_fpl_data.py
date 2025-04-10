from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, from_json, expr
import os

def create_spark_session():
    """
    Create and return a SparkSession.
    """
    spark = SparkSession.builder \
        .appName("FPL ETL Pipeline") \
        .getOrCreate()
    return spark

def extract_data(spark, input_path):
    """
    Extract data from a JSON file.
    """
    # Read JSON file into DataFrame
    df = spark.read.json(input_path, multiLine=True)
    return df

def transform_data(df):
    """
    Transform the raw data.
    For example, extract player information, compute metrics, or flatten nested structures.
    """
    # Beispiel: Angenommen, das JSON enthält ein Array namens 'elements' mit Spielerinformationen.
    # Wir extrahieren diese Spieler-Daten und wählen einige Spalten aus.
    if "elements" in df.columns:
        # Flatten the nested array 'elements'
        players_df = df.select(explode("elements").alias("player"))
        # Wähle spezifische Felder (passe diese an die Struktur der FPL-Daten an)
        players_df = players_df.select(
            col("player.id").alias("player_id"),
            col("player.first_name"),
            col("player.second_name"),
            col("player.element_type").alias("position"),
            col("player.now_cost").alias("cost"),
            col("player.total_points").alias("points")
        )
        # Füge eine Berechnung hinzu, z. B. Punkte pro Kosten
        players_df = players_df.withColumn("points_per_cost", col("points") / col("cost"))
        return players_df
    else:
        # Falls das JSON eine andere Struktur hat, passe die Transformation an.
        return df

def load_data(df, output_path):
    """
    Write the transformed DataFrame to an output file.
    We use Parquet as an example, but CSV or andere Formate sind auch möglich.
    """
    # Write DataFrame as Parquet file (kann aber auch als CSV geschrieben werden)
    df.write.mode("overwrite").parquet(output_path)
    print(f"Data loaded to: {output_path}")

def main():
    # Setup file paths (anpassen, falls dynamisch benötigt)
    input_path = os.path.join("data", "raw", "fpl_data_2025-04-10.json")
    output_path = os.path.join("data", "processed", "fpl_players.parquet")
    
    spark = create_spark_session()
    
    # Extract
    raw_df = extract_data(spark, input_path)
    print("Extraction complete.")
    
    # Transform
    transformed_df = transform_data(raw_df)
    print("Transformation complete.")
    
    # Load
    load_data(transformed_df, output_path)
    print("ETL pipeline completed.")

    spark.stop()

if __name__ == "__main__":
    main()
