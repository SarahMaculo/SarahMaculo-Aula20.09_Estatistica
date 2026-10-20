import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

# Obtendo e organizando os dados 

try:
    print('Obtendo dados . . .')
    ENDERECO_DADOS = 'https://www.ispdados.rj.gov.br/Arquivos/BaseDPEvolucaoMensalCisp.csv'

    df_ocorrencias = pd.read_csv(ENDERECO_DADOS, sep=';', encoding='iso-8859-1')
    # print(df_ocorrencias)

    df_estelionato_data = df_ocorrencias[['mes_ano', 'estelionato']]
    df_estelionato_data = df_estelionato_data.groupby('mes_ano', as_index=False)['estelionato'].sum()
    print(df_estelionato_data)

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

# Ordenando os dados
    
try:
    df_estelionato_data = df_estelionato_data.sort_values(
    by='estelionato',
    ascending=False
    )

    print(df_estelionato_data.head(10))
    print(df_estelionato_data.tail(10))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')

# Separando Média e Mediana
    
try:
    array_estelionato_data = np.array(df_estelionato_data['estelionato'])
    media_estelionato = np.mean(array_estelionato_data)
    mediana_estelionato = np.median(array_estelionato_data)
    distancia = abs(
    (media_estelionato - mediana_estelionato) / mediana_estelionato * 100
    )


except Exception as e:
    print(f'Erro ao obter os dados - {e}')


# # Determinando os quartis

try:
    q1 = np.quantile(array_estelionato_data, .25)
    q2 = np.quantile(array_estelionato_data, .50)
    q3 = np.quantile(array_estelionato_data, .75)

    max = np.max(array_estelionato_data)
    min = np.min(array_estelionato_data)

    amplitude = max - min
    print('\n M E N O R E S  E  M E N O R E S  Í N D I C E S')
    df_estelionato_menores = df_estelionato_data[df_estelionato_data['estelionato']<q1]
    df_estelionato_maiores = df_estelionato_data[df_estelionato_data['estelionato']>q3]


    print('\n M E N O R E S')
    print(f'{df_estelionato_menores.sort_values(by='estelionato', ascending=True)}')
    df_estelionato_menores.to_csv('menores.csv', index=False, sep=';')

    print('\n M A I O R E S')
    print(df_estelionato_maiores.sort_values(by='estelionato', ascending=False))

except Exception as e:
    print(f'Erro ao obter os dados - {e}')


interpretacao = (f'''
                 Devido aos valores que variam em aproximadamente 53/100 do seu valor central, a quantidade de estelionato entre os anos de 2003 - 2026 não possui um padrão; 
Ou seja, existem quantidades da atividade criminosa que variam ao longo do tempo.
Sabendo disso, 25/100 das menores ações somam um total de {q1} e 25/100 das maiores atividades são de {q3};
''')
print(interpretacao)

try:
    iqr = q3 - q1
    limite_sup = q3 + (1.5*iqr)
    limite_inf = q1 - (1.5*iqr)

    df_estelionato_outliers_maiores = (
        df_estelionato_data[df_estelionato_data['estelionato'] > limite_sup]
    )
    df_estelionato_outliers_menores = (
        df_estelionato_data[df_estelionato_data['estelionato']< limite_inf]
    )
    print('O U T L I E R S  S U P E R I O R E S')
    print(30*'=')
    if len(df_estelionato_outliers_maiores) == 0:
        print('Não há outliers.')
    else:
        print(df_estelionato_outliers_maiores)
        
    print('O U T L I E R S  I N F E R I O R E S')
    print(30*'=')

    if len(df_estelionato_outliers_menores) == 0:
        print('Não há outliers.')
    else:
        print(df_estelionato_outliers_menores)

except Exception as e:
    print(f'Erro ao calcular os outliers - {e}')

try:
    print('Informações sobre os casos de estelionato')
    plt.figure(figsize=(16, 10))
    plt.subplot(1,2,1)

    plt.boxplot(df_estelionato_data['estelionato'], orientation='horizontal', showfliers=False)
    plt.title('Distribuição dos dados')
    plt.xlabel('Estelionatos')

    plt.subplot(1,2,2)
    plt.text(0.1,0.95, f'Limite Inferior: {limite_inf}', fontsize=12) # -> coordenadas
    plt.text(0.1,0.90, f'Mínimo: {min}', fontsize=12)
    plt.text(0.1,0.85, f'Q1: {q1}', fontsize=12)
    plt.text(0.1,0.80, f'Q2: {q2}', fontsize=12)
    plt.text(0.1,0.75, f'Q3: {q3}', fontsize=12)
    plt.text(0.1,0.70, f'Limite Superior: {limite_sup}', fontsize=12)
    plt.text(0.1,0.65, f'Máximo: {max}', fontsize=12)

    plt.text(0.1,0.55, f'Mediana: {mediana_estelionato}', fontsize=12)
    plt.text(0.1,0.50, f'Média: {media_estelionato}', fontsize=12)
    plt.text(0.1,0.45, f'IQR: {iqr}', fontsize=12)
    plt.text(0.1,0.40, f'Amplitude Total: {amplitude}', fontsize=12)
    plt.text(0.1,0.35, f'Distância: {distancia}', fontsize=12)
    plt.axis('off') 

    plt.suptitle('Informações dos estelionatos')
    plt.show()

except Exception as e:
    print(f'Erro ao calcular os outliers - {e}')