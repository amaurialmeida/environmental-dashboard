# src/big_data_processor.py - Versão sem PySpark, usando Dask (leve e escalável)
import pandas as pd
import numpy as np
from dask import dataframe as dd
from dask.distributed import Client, LocalCluster
import warnings
warnings.filterwarnings('ignore')

class BigDataProcessor:
    """Simula processamento Big Data usando Dask (leve, sem necessidade de Java)."""
    
    def __init__(self, data_path):
        # Tenta criar um cluster Dask local leve
        try:
            self.cluster = LocalCluster(n_workers=2, threads_per_worker=2, memory_limit='2GB')
            self.client = Client(self.cluster)
            print(f"Dask dashboard disponível em: {self.client.dashboard_link}")
        except:
            print("Usando Dask em modo single-thread (sem cluster)")
            self.client = None
            
        # Lê dados com Dask (simula processamento distribuído)
        self.df_dask = dd.read_parquet(data_path)
        
    def aggregate_by_time(self, freq='monthly'):
        """Agrega métricas por período usando Dask (Big Data simulation)."""
        if freq == 'monthly':
            # Agrupa por ano e mês
            df_agg = self.df_dask.groupby(['year', 'month']).agg({
                'energy_produced_mwh': 'sum',
                'carbon_saved_tco2e': 'sum'
            }).compute()  # compute() executa o processamento distribuído
            
            df_agg = df_agg.reset_index()
            
        elif freq == 'yearly':
            df_agg = self.df_dask.groupby('year').agg({
                'energy_produced_mwh': 'sum',
                'carbon_saved_tco2e': 'sum'
            }).compute()
            df_agg = df_agg.reset_index()
            
        else:  # daily
            # Converte para string da data e agrupa
            self.df_dask['date_str'] = self.df_dask['date'].astype('str')
            df_agg = self.df_dask.groupby('date_str').agg({
                'energy_produced_mwh': 'sum',
                'carbon_saved_tco2e': 'sum'
            }).compute()
            df_agg = df_agg.reset_index()
            df_agg['date'] = pd.to_datetime(df_agg['date_str'])
            
        return df_agg
    
    def top_projects_by_impact(self, metric='carbon_saved_tco2e', top_n=5):
        """Retorna os projetos com maior impacto usando Dask."""
        top = self.df_dask.groupby('project_name')[metric].sum() \
            .nlargest(top_n) \
            .compute() \
            .reset_index()
        top.columns = ['project_name', f'total_{metric}']
        return top
    
    def generate_large_dataset(self, n_records=10_000_000):
        """Demonstra escalabilidade: gera dataset de 10M registros."""
        print(f"🔄 Gerando dataset Big Data com {n_records:,} registros...")
        
        # Cria particionamento para simular distribuição
        partitions = 10
        records_per_partition = n_records // partitions
        
        def generate_partition(partition_id):
            np.random.seed(partition_id)
            n = records_per_partition if partition_id < partitions - 1 else n_records - (records_per_partition * (partitions - 1))
            
            projects = ['Solar', 'Wind', 'Water', 'Biodiversity', 'ML_Climate']
            regions = ['Brazil', 'Chile', 'Argentina', 'Global']
            
            df_part = pd.DataFrame({
                'project_name': np.random.choice(projects, n),
                'project_type': np.random.choice(['solar', 'wind', 'water', 'biodiversity', 'climate_ml'], n),
                'region': np.random.choice(regions, n),
                'date': pd.date_range('2016-08-01', '2026-05-31', periods=n),
                'energy_produced_mwh': np.random.exponential(50, n),
                'carbon_saved_tco2e': np.random.exponential(30, n),
                'year': np.random.randint(2016, 2027, n),
                'month': np.random.randint(1, 13, n),
            })
            return df_part
        
        # Gera partições e combina
        partitions_list = [generate_partition(i) for i in range(partitions)]
        large_df = pd.concat(partitions_list, ignore_index=True)
        
        # Converte para Dask DataFrame
        dask_large = dd.from_pandas(large_df, npartitions=partitions)
        return dask_large
    
    def stop(self):
        """Encerra o cluster Dask."""
        if self.client:
            self.client.close()
        if self.cluster:
            self.cluster.close()