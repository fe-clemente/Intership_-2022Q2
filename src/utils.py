# src/utils.py
import requests
import json
from datetime import datetime
import os

def fetch_selic_data(start_date: str, end_date: str) -> list:
    url = f"https://api.bcb.gov.br/dados/serie/bcdata.sgs.11/dados?formato=json&dataInicial={start_date}&dataFinal={end_date}"
    response = requests.get(url)
    data = response.json()
    for entry in data:
        entry['data'] = datetime.strptime(entry['data'], '%d/%m/%Y').date()
    return data

def save_data_to_file(data: list, filepath: str):
    # Garante que o diretório existe
    dir_name = os.path.dirname(filepath)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(filepath, 'w') as file:
        json.dump(data, file, default=str)

# Função de Teste
if __name__ == "__main__":
    data = fetch_selic_data('01/01/2000', '31/03/2022')
    save_data_to_file(data, 'data/selic_data.json')
    print("Dados da SELIC obtidos e salvos com sucesso!")
