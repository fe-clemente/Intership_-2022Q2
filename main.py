import pandas as pd
import numpy as np
from datetime import timedelta, datetime


# Função para calcular o valor futuro com juros compostos
def calcular_juros_compostos(capital_inicial, taxa_juros, periodo):
    return capital_inicial * (1 + taxa_juros) ** periodo


# Função para calcular o lucro total
def calcular_lucro(df, capital_inicial, start_date, end_date, frequency):
    df_periodo = df[(df.index >= start_date) & (df.index <= end_date)]

    if frequency == 'dia':
        periodos = len(df_periodo)
        taxa_juros = df_periodo['SELIC'].mean() / 100
    elif frequency == 'mês':
        df_resampled = df_periodo.resample('ME').mean()
        periodos = len(df_resampled)
        taxa_juros = df_resampled['SELIC'].mean() / 100
    elif frequency == 'ano':
        df_resampled = df_periodo.resample('A').mean()
        periodos = len(df_resampled)
        taxa_juros = df_resampled['SELIC'].mean() / 100
    else:
        raise ValueError("Frequência inválida. Use 'dia', 'mês' ou 'ano'.")

    lucro_total = calcular_juros_compostos(capital_inicial, taxa_juros, periodos)
    return lucro_total


# Função para encontrar o período mais lucrativo
def periodo_mais_lucrativo(df, capital_inicial, periodo_dias, start_date, end_date):
    max_lucro = -float('inf')
    melhor_inicio = None
    melhor_fim = None

    datas = pd.date_range(start=start_date, end=end_date - pd.Timedelta(days=periodo_dias))

    for start in datas:
        end = start + pd.Timedelta(days=periodo_dias)
        lucro = calcular_lucro(df, capital_inicial, start, end, 'dia')
        if lucro > max_lucro:
            max_lucro = lucro
            melhor_inicio = start
            melhor_fim = end

    return melhor_inicio, melhor_fim, max_lucro


# Função para calcular e imprimir o lucro mensal
def lucro_mensal(df, capital_inicial, start_date, end_date):
    df_periodo = df[(df.index >= start_date) & (df.index <= end_date)]
    df_mensal = df_periodo.resample('ME').mean()

    print(f"Lucro mês a mês de {start_date.strftime('%Y-%m-%d')} a {end_date.strftime('%Y-%m-%d')}:")

    lucros_mensais = []
    for date, row in df_mensal.iterrows():
        taxa_juros = row['SELIC'] / 100
        lucro = calcular_juros_compostos(capital_inicial, taxa_juros, 1) - capital_inicial
        lucros_mensais.append((date.strftime('%m/%Y'), lucro))
        print(f"{date.strftime('%m/%Y')} R$ {lucro:,.2f}")

    return pd.DataFrame(lucros_mensais, columns=['Data', 'Lucro'])


# Função para formatar o lucro total
def formatar_lucro_total(lucro_total):
    lucro_str = f"{lucro_total:,.2f}"
    partes = lucro_str.split(',')
    partes_formatadas = [f"R$ {parte.strip()}" for parte in partes]
    return ' '.join(partes_formatadas)


# Função principal
def main():
    # Gerar dados simulados
    dates = pd.date_range(start='2000-01-01', end='2022-03-31', freq='D')
    np.random.seed(0)  # Para reprodutibilidade
    selic_rates = np.random.uniform(low=3.0, high=15.0, size=len(dates))  # Taxas SELIC simuladas

    df = pd.DataFrame({'SELIC': selic_rates}, index=dates)

    capital_inicial = 1500
    periodo_dias = 500
    start_date = pd.to_datetime('2000-01-01')
    end_date = pd.to_datetime('2022-03-31')

    inicio, fim, lucro = periodo_mais_lucrativo(df, capital_inicial, periodo_dias, start_date, end_date)

    print("O período mais lucrativo de 500 dias corridos desde 2000-01-01 até 2022-03-31 foi:")
    print(f"Início: {inicio.strftime('%Y-%m-%d')}")
    print(f"Término: {fim.strftime('%Y-%m-%d')}")

    lucro_total = calcular_lucro(df, capital_inicial, inicio, fim, 'dia')
    lucro_total_formatado = formatar_lucro_total(lucro_total)
    print(f"Se eu tivesse investido R$ {capital_inicial} do início de 2000 até março de 2022, teria um lucro de:")
    print(f"{lucro_total_formatado}")

    df_lucro_mensal = lucro_mensal(df, capital_inicial, inicio, fim)

    lucro_total_mensal = df_lucro_mensal['Lucro'].sum()
    lucro_total_mensal_formatado = formatar_lucro_total(lucro_total_mensal)
    print(f"\nSoma dos lucros mensais: {lucro_total_mensal_formatado}")


if __name__ == "__main__":
    main()
