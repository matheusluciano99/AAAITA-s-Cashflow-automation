import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

"""Automação do Fluxo de Caixa da Lojinha"""
"""Voa Urubuzão"""

# Configurações da autenticação com o Google Sheets
scopes = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']

# Substitua 'credentials.json' pelo nome do arquivo JSON de credenciais e a parte de scopes é necessária
credentials = Credentials.from_service_account_file('fc-2023-208ce7e2d751.json', scopes=scopes)

client = gspread.authorize(credentials)

# Abre a planilha pelo nome
planilha = client.open('FC 2023')  # Substitua 'Nome da Planilha' pelo nome da sua planilha do Google Sheets

# Abre a guia pelo nome
guia = planilha.worksheet('Resumo')  # Substitua 'Nome da Guia' pelo nome da guia que você quer trabalhar

# FC = Fluxo de Caixa
# Lendo o arquivo
FC = pd.read_csv('Cashflow.csv')  # Substitua o nome 'Nome do Arquivo' pelo nome do arquivo que você quer ler

# Trocando os pontos por nada e as virgulas por ponto
FC['VALOR'] = FC['VALOR'].apply(lambda x: float(str(x).replace('.', '').replace(',', '.')))

# Trocando o formato da data
FC['DATA'] = pd.to_datetime(FC['DATA'], dayfirst=True)

# Filtro de data
print("Digite a data no seguinte formato: Ano-Mes-Dia")
continua = True
# Loop para varios filtros
while continua:
    Lista_Val = []
    data_inf = input("Data inferior: ")
    data_inf = pd.to_datetime(data_inf)
    data_sup = input("Data superior: ")
    data_sup = pd.to_datetime(data_sup)
    FC_fil_por_data_e_valor = FC.query('DATA >= @data_inf and DATA <= @data_sup and VALOR > 0') 

    # Passando valores filtrados por data para lista
    Lista_Val = Lista_Val + FC_fil_por_data_e_valor['VALOR'].tolist()

    Resultado_Final = sum(Lista_Val)
    print(Resultado_Final)
    celula = input("Coloque a celula que voce quer alterar: ")
    guia.update(celula, [[Resultado_Final]])
    resposta = input("Deseja realizar mais filtros? (s/n) ")
    if resposta == 'n':
        continua = False

print("VOA URUBUZAO!!!")