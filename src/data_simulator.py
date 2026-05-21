import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_impact_dataset():
    """Gera um dataset sintético mas realista do impacto de cada projeto."""
    
    # 1. Definição dos projetos baseada no seu portfolio
    projects = [
        {"name": "Usina Solar Noroeste Paulista", "type": "solar", "start": "2019-01-01", "capacity_mw": 1.07, "region": "SP, Brasil"},
        {"name": "Síndrome do Colapso das Abelhas", "type": "biodiversity", "start": "2016-08-01", "end": "2022-12-31", "region": "MG, SP, PR"},
        {"name": "Observatório do Rio Santa Rita", "type": "water", "start": "2017-03-01", "region": "Fernandópolis, SP"},
        {"name": "Potencial Eólico — Patagônia", "type": "wind", "start": "2025-03-01", "region": "Chile & Argentina"},
        {"name": "Qualidade da Água — Patagônia", "type": "water", "start": "2019-01-01", "end": "2024-12-31", "region": "Chile & Argentina"},
        {"name": "Monitoramento Sísmico — Patagônia", "type": "geology", "start": "2025-03-01", "region": "Chile & Argentina"},
        {"name": "Impacto Espécies Invasoras — Puerto Williams", "type": "biodiversity", "start": "2024-01-01", "region": "Chile"},
        {"name": "Abelhas sem Ferrão no Brasil", "type": "biodiversity", "start": "2023-01-01", "region": "Brasil"},
        {"name": "Previsão Impacto El Niño 2026", "type": "climate_ml", "start": "2025-06-01", "region": "Global"},
        {"name": "Carro Elétrico vs Combustão", "type": "mobility", "start": "2025-10-01", "region": "Brasil-Patagônia"},
    ]
    
    records = []
    start_global = datetime(2016, 8, 1)
    end_global = datetime(2026, 5, 31)
    
    for project in projects:
        # Define período de dados do projeto
        p_start = datetime.strptime(project.get('start', '2016-08-01'), '%Y-%m-%d')
        p_end = datetime.strptime(project.get('end', '2026-05-31'), '%Y-%m-%d')
        p_end = min(p_end, end_global)
        
        # Gera registros mensais para cada projeto
        current_date = max(p_start, start_global)
        while current_date <= p_end:
            # Lógica de impacto baseada no tipo de projeto
            if project['type'] == 'solar':
                # Energia solar: variação sazonal e por capacidade
                monthly_energy_mwh = project['capacity_mw'] * 24 * 30 * random.uniform(0.15, 0.25)
                carbon_saved_tco2 = monthly_energy_mwh * 0.084  # Fator médio Brasil
                
            elif project['type'] == 'wind':
                # Eólico na Patagônia: fator de capacidade alto (~40%)
                monthly_energy_mwh = 3.0 * 24 * 30 * random.uniform(0.35, 0.45)  # assume 3MW nominal
                carbon_saved_tco2 = monthly_energy_mwh * 0.084
                
            elif project['type'] == 'biodiversity':
                # Projetos de conservação: carbono por área preservada/restaurada
                monthly_energy_mwh = 0
                carbon_saved_tco2 = random.uniform(10, 50)  # tCO2e por mês
                
            elif project['type'] == 'water':
                # Projetos hídricos: ganhos indiretos menores
                monthly_energy_mwh = random.uniform(0, 5)
                carbon_saved_tco2 = random.uniform(5, 20)
                
            elif project['type'] == 'climate_ml':
                # Modelo de ML: impacto via otimizações
                monthly_energy_mwh = random.uniform(10, 30)
                carbon_saved_tco2 = random.uniform(15, 40)
                
            else:
                monthly_energy_mwh = random.uniform(0, 2)
                carbon_saved_tco2 = random.uniform(0, 10)
            
            # Adiciona ruído e tendência de melhoria ao longo do tempo
            time_factor = 1 + (current_date - start_global).days / (365*10)  # 10% melhoria por década
            monthly_energy_mwh *= time_factor * random.uniform(0.9, 1.1)
            carbon_saved_tco2 *= time_factor * random.uniform(0.9, 1.1)
            
            records.append({
                'project_name': project['name'],
                'project_type': project['type'],
                'region': project['region'],
                'date': current_date,
                'energy_produced_mwh': max(0, monthly_energy_mwh),
                'carbon_saved_tco2e': max(0, carbon_saved_tco2),
                'year': current_date.year,
                'month': current_date.month,
            })
            current_date += timedelta(days=30)  # aprox. mensal
    
    df = pd.DataFrame(records)
    return df

if __name__ == "__main__":
    df = generate_impact_dataset()
    print(f"Dataset gerado: {df.shape[0]} registros")
    print(df.head())
    # Salva como parquet (ótimo para Big Data)
    df.to_parquet('../data/processed/portfolio_impact_data.parquet', index=False)