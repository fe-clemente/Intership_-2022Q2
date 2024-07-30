import json
import pandas as pd


def load_selic_data(filepath):
    try:
        with open(filepath, 'r') as file:
            data = json.load(file)
        return pd.DataFrame(data)
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {filepath}")
        return pd.DataFrame()
    except json.JSONDecodeError:
        print("Erro ao decodificar JSON.")
        return pd.DataFrame()


def perform_calculations(df, initial_capital):
    if not df.empty:
        df['data'] = pd.to_datetime(df['data'])
        df = df.set_index('data')
        df = df.sort_index()
        df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
        df['Calculated Value'] = initial_capital
        df['Calculated Value'] = df['valor'].apply(lambda x: initial_capital * (1 + x))

        for i in range(1, len(df)):
            df['Calculated Value'].iloc[i] = df['Calculated Value'].iloc[i - 1] * (1 + df['valor'].iloc[i])

        df['Difference'] = df['Calculated Value'] - initial_capital

    return df


def main_calculation_function():
    data = load_selic_data('data/selic_data.json')
    initial_capital = 1000
    result = perform_calculations(data, initial_capital)
    print(result.head())
    print(f"Último valor calculado: {result['Calculated Value'].iloc[-1]}")


if __name__ == "__main__":
    main_calculation_function()
