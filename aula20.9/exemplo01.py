import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# Obtendo dados 

try:
    print('Obtendo dados . . .')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    #utf-8, iso-8859-1, cp1252 (decodificador de caracteres - cada arquivo tem o seu)
    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrência)

    #delimitando os dados
    df_roubo_veiculo = df_ocorrencias[['munic', 'roubo_veiculo']]
    # print(df_roubo_veiculo.tail(30))

    # ### PREPARANDO DADOS

    #  totalizando os roubos por cidade (variável qualitativa 'munic' e variável quantitativa 'roubo_veiculo')
    df_roubo_veiculo = df_roubo_veiculo.groupby('munic', as_index=False)['roubo_veiculo'].sum()


    # Classificando os dados / Ordenando
    df_roubo_veiculo = df_roubo_veiculo.sort_values(
        by='roubo_veiculo',
        ascending=False
    )
    print(df_roubo_veiculo.head(10))
    print(df_roubo_veiculo.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

# try:
#     print(f'\nObtendo informações a cerca dos roubos dos veículos . . .')

array_roubo_veiculo = np.array(df_roubo_veiculo['roubo_veiculo']) 
media_roubo_veiculo = np.mean(array_roubo_veiculo)
mediana_roubo_veiculo = np.median(array_roubo_veiculo)
distancia = abs(
    (media_roubo_veiculo - mediana_roubo_veiculo) / mediana_roubo_veiculo * 100
    )


# except Exception as e:
    # print(f'Obtendo Medidas - {e}')

try:
    q1 = np.quantile(array_roubo_veiculo, .25)
    q2 = np.quantile(array_roubo_veiculo, .50)
    q3 = np.quantile(array_roubo_veiculo, .75)
    


    df_roubo_veiculos_menores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']<q1]
    df_roubo_veiculos_maiores = df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']>q3]

    print('TAXAS DE ROUBO MAIORES E MENORES')

    print('\n M E N O R E S')
    print(f'{df_roubo_veiculos_menores.sort_values(by='roubo_veiculo', ascending=True)}')
    df_roubo_veiculos_menores.to_csv('menores.csv', index=False, sep=';')

    print('\n M A I O R E S')
    print(df_roubo_veiculos_maiores.sort_values(by='roubo_veiculo', ascending=False))
    df_roubo_veiculos_maiores.to_csv('maiores.csv', index=False, sep=';')
    
except Exception as e:
    print(f'Erro ao analisar a distribuição - {e}')


# Medidas de Posição e Dispersão
    
try:
    print('\nCalculando a Amplitude Total')
    # AMPLITUDE TOTAL = menor valor - MAIOR VALOR

    max = np.max(array_roubo_veiculo)
    min = np.min(array_roubo_veiculo)
    amplitude = max - min
except Exception as e:
    print(f'Erro ao analisar a distribuição - {e}')
#Achando Outliers;
    
try:
    # Amplitudo dos dados mais centrais
    iqr = q3 - q1
    
    # Calculando os limites
    # S U P E R I O R
    limite_sup = q3 + (1.5*iqr)

    # I N F E R I O R 
    limite_inf = q1 - (1.5*iqr)

    # print(f'\n Limite Superior: {limite_sup}')
    # print(f'\n Limite Inferior: {limite_inf}')

    # Filtrando os outliers
    df_roubo_veiculos_outliers_menores =(
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']<limite_inf]
    )
    df_roubo_veiculos_outliers_maiores = (
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']>limite_sup]
        )

    print(f'\nMunicípios com outliers inferiores')
    print(30 * '=')
    if len(df_roubo_veiculos_outliers_menores) == 0:
        print('Não há outliers inferiores.')
    else:
        print(df_roubo_veiculos_outliers_menores)

        df_roubo_veiculos_outliers_menores =(
        df_roubo_veiculo[df_roubo_veiculo['roubo_veiculo']<limite_inf]
    )
    print(f'\nMunicípios com outliers superiores')
    print(30 * '=')
    if len(df_roubo_veiculos_outliers_maiores) == 0:
        print('Não há outliers superiores.')
    else:
        print(df_roubo_veiculos_outliers_maiores)
except Exception as e:
    print(f'Erro ao calcular os outliers - {e}')

try:
    print('\nMOSTRANDO VALORES')
    print()
    print(f'Mínimo: {min}')
    print(f'\nMáximo: {max}')
    print(f'\nLimite inf: {limite_inf}')
    print(f'''\n
    Q1: {q1} 
    Q2: {q2} 
    Q3: {q3}
    ''')
    print(f'\nLimite sup: {limite_sup}')
    
    print()
    print('\nMedidas de Tendência Central')
    print()
    print(f'Média : {media_roubo_veiculo}')
    print()
    print(f'Mediana : {mediana_roubo_veiculo}')
    print()
    print(f'Distância Média - Mediana : {distancia:.2f}%')

    print(f'\nAmplitude Total: {amplitude}')
    print(f'\nIQR: {iqr}')

except Exception as e:
    print(f'Erro ao calcular os outliers - {e}')


# Plotando gráfico
# try:
#     print('Plotando BoxPlot')
#     # pip install matplotlib -> library pra visualização de dados

#     # BoxPlot -> gráfico
#     # showfliers=False -> Retira outliers
#     plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation="horizontal", showmeans=True)
#     plt.show()

# except Exception as e:
#     print(f'Erro ao calcular os outliers - {e}')

# Plotando gráfico
try:
    print('Informações de Roubos de Veículos')
    # pip install matplotlib -> library pra visualização de dados
    plt.figure(figsize=(16, 10))

    # Posição 1 Boxplot
    plt.subplot(1,2,1)
    # BoxPlot -> gráfico
    # showfliers=False -> Retira outliers
    plt.boxplot(df_roubo_veiculo['roubo_veiculo'], orientation="horizontal", showmeans=True)
    plt.title('Distribuição dos dados')
    plt.xlabel('Roubo de Veículos')
    # plt.ylabel('Municípios')

    plt.subplot(1,2,2)
    plt.text(0.1,0.95, f'Limite Inferior: {limite_inf}', fontsize=12) # -> coordenadas
    plt.text(0.1,0.90, f'Mínimo: {min}', fontsize=12)
    plt.text(0.1,0.85, f'Q1: {q1}', fontsize=12)
    plt.text(0.1,0.80, f'Q2: {q2}', fontsize=12)
    plt.text(0.1,0.75, f'Q3: {q3}', fontsize=12)
    plt.text(0.1,0.70, f'Limite Superior: {limite_sup}', fontsize=12)
    plt.text(0.1,0.65, f'Máximo: {max}', fontsize=12)

    plt.text(0.1,0.55, f'Mediana: {mediana_roubo_veiculo}', fontsize=12)
    plt.text(0.1,0.50, f'Média: {media_roubo_veiculo}', fontsize=12)
    plt.text(0.1,0.45, f'IQR: {iqr}', fontsize=12)
    plt.text(0.1,0.40, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.1,0.35, f'Distância: {distancia}', fontsize=12)
    plt.axis('off') 

    plt.suptitle('Informações dos roubos de veículos')

    
    plt.show()

except Exception as e:
    print(f'Erro ao calcular os outliers - {e}')