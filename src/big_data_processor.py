from pyspark.sql import SparkSession
from pyspark.sql.functions import sum as spark_sum, col, year, month
import pandas as pd

class BigDataProcessor:
    """Simula processamento em escala usando PySpark."""
    
    def __init__(self, data_path):
        self.spark = SparkSession.builder \
            .appName("EnvironmentalDashboard") \
            .config("spark.sql.execution.arrow.pyspark.enabled", "true") \
            .getOrCreate()
        
        # Lê dados (pode ser CSV, Parquet, ou conectar-se a um bucket S3)
        self.df_spark = self.spark.read.parquet(data_path)
        
    def aggregate_by_time(self, freq='monthly'):
        """Agrega métricas por período."""
        if freq == 'monthly':
            df_agg = self.df_spark.groupBy('year', 'month') \
                .agg(spark_sum('energy_produced_mwh').alias('total_energy_mwh'),
                     spark_sum('carbon_saved_tco2e').alias('total_carbon_tco2e'))
        elif freq == 'yearly':
            df_agg = self.df_spark.groupBy('year') \
                .agg(spark_sum('energy_produced_mwh').alias('total_energy_mwh'),
                     spark_sum('carbon_saved_tco2e').alias('total_carbon_tco2e'))
        else:  # daily
            df_agg = self.df_spark.groupBy('date') \
                .agg(spark_sum('energy_produced_mwh').alias('total_energy_mwh'),
                     spark_sum('carbon_saved_tco2e').alias('total_carbon_tco2e'))
        
        return df_agg.toPandas()
    
    def top_projects_by_impact(self, metric='carbon_saved_tco2e', top_n=5):
        """Retorna os projetos com maior impacto."""
        top = self.df_spark.groupBy('project_name') \
            .agg(spark_sum(metric).alias(f'total_{metric}')) \
            .orderBy(f'total_{metric}', ascending=False) \
            .limit(top_n) \
            .toPandas()
        return top
    
    def stop(self):
        self.spark.stop()