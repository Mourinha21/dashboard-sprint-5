import streamlit as st
import pandas as pd
import plotly.express as px


# Armazenando os dataframes em variáveis

dados_europa = pd.read_csv(r'C:\Users\madki\dashboard-sprint-5\Europe.csv')
dados_india = pd.read_csv(r'C:\Users\madki\dashboard-sprint-5\India.csv')
dados_filipinas = pd.read_csv(
    r'C:\Users\madki\dashboard-sprint-5\Philippines.csv')
dados_eua = pd.read_csv(r'C:\Users\madki\dashboard-sprint-5\United_States.csv')

# Renomeando a coluna "Revenue growth" do dataframe dos dados dos EUA
dados_eua = dados_eua.rename(columns={'Revenue growth': 'Revenue growth (%)'})

# Alterando o tipo da coluna 'Profit(billions US$) de object para float'

dados_india['Profit(billions US$)'][30] = -0.4
dados_india['Profit(billions US$)'] = pd.to_numeric(
    dados_india['Profit(billions US$)'])

# Alterando os dados de um índice para conseguir converter a coluna no dataframe dos dados das Filipinas
dados_filipinas['Profits(USD millions)'][24] = '12'

# Alterando o tipo das colunas do dataframe das Filipinas

dados_filipinas['Revenue(USD millions)'] = (
    dados_filipinas['Revenue(USD millions)'].str.replace(",", ".").astype(float))
dados_filipinas['Profits(USD millions)'] = (
    dados_filipinas['Profits(USD millions)'].str.replace(",", ".").astype(float))
dados_filipinas['Employees'] = (
    dados_filipinas['Employees'].str.replace(",", "").astype(float))

# Ajustando e depois convertendo as colunas que não eram do tipo certo
dados_eua['Revenue (USD millions)'] = pd.to_numeric(
    dados_eua['Revenue (USD millions)'].str.replace(",", ".").astype(float))
dados_eua['Revenue growth (%)'] = pd.to_numeric(
    dados_eua['Revenue growth (%)'].str.replace("%", "").astype(float))
dados_eua['Employees'] = dados_eua['Employees'].str.replace(",", ".")
dados_eua['Employees'] = dados_eua['Employees'].str.replace(".", "")
dados_eua['Employees'] = pd.to_numeric(dados_eua['Employees'].astype(float))

# Agrupando dados da Europa por país
receita_pais_europeu = (
    dados_europa
    .groupby(['Headquarters'])[['Revenue(US$ billions)']]
    .mean().reset_index()
)

receita_pais_europeu.sort_values(
    by='Revenue(US$ billions)', axis=0, ascending=True, inplace=True)

# Ordenando os dados do dataframe da Índia para a criação do gráfico
dados_india.sort_values(by='Forbes 2000 rank', axis=0,
                        ascending=False, inplace=True)

# Atribuindo os dados ordenados do dataframe das Filipinas para a criação do gráfico
dados_ordenados_filipinas = dados_filipinas.sort_values(
    by='Employees', axis=0, ascending=True)

# Atribuindo os dados dos EUA em uma nova variável para a criação do gráfico
crescimento_industria_eua = (dados_eua.groupby(['Industry'])[
                             ['Revenue growth (%)']].sum().reset_index())
crescimento_industria_eua.sort_values(
    by='Revenue growth (%)', ascending=True, inplace=True)

hist_button_eu = st.button('Criar histograma')

if hist_button_eu:
    st.write(
        'Criando um histograma para o conjunto de dados da receita de países europeus')

    fig = px.histogram(dados_europa, x='Revenue(US$ billions)',
                       title='Contagem de receitas dos países europeus', color_discrete_sequence=['indianred'])

    st.plotly_chart(fig, use_container_width=True)

scatter_button_india = st.button('Criar gráfico de dispersão')

if scatter_button_india:
    st.write('Criando um gráfico de dispersão para o conjunto de dados da Índia')

    fig = px.scatter(dados_india, x='Forbes 2000 rank',
                     y='Assets(billions US$)',
                     trendline='expanding',
                     title='Patrimônio de empresas de acordo com o ranking da Forbes')

    st.plotly_chart(fig, use_container_width=True)

line_button_filipinas = st.button('Criar gráfico de linha')

if line_button_filipinas:
    st.write('Criando um gráfico de linha para o conjunto de dados das Filipinas')

    fig = px.scatter(dados_ordenados_filipinas, x='Employees',
                     y='Profits(USD millions)',
                     title='Lucro de empresas (por milhões de US$) pelo o número de funcionários (por mil)')

    st.plotly_chart(fig, use_container_width=True)

area_button_eua = st.button('Criar gráfico de área')

if area_button_eua:
    st.write('Criando um gráfico de área para o conjunto de dados dos EUA')

    fig = px.area(crescimento_industria_eua,
                  x='Industry',
                  y='Revenue growth (%)',
                  title='Crescimento de receita das empresas estadunidenses por indústria')

    st.plotly_chart(fig, use_container_width=True)
