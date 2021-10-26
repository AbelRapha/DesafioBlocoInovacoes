import pandas as pd
import streamlit as st
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import train_test_split
import joblib
import plotly.express as px

#Configurando páginas

st.set_page_config(page_title= "Dashboard Análise Dimas Construções",layout= "wide")

st.image("https://bloco.digital/wp-content/uploads/2020/07/cropped-blocohorizontal-e1596380063716-2.png", width=200)

def load_model(nome_arquivo):
    return joblib.load(nome_arquivo)

def calcula_retorno(valor_imovel, valor_aluguel):
    return  f'{valor_aluguel/valor_imovel * 100} %' 

#def calculo_rentabilidade(preco_aluguel, valor_venda):
 #   valor_aluguel = preco_aluguel
  #  venda = valor_venda
   # return (valor_aluguel/venda * 12)

botao_checkbox = st.sidebar.checkbox('Modelo Alugueis Zap')
botao_checkbox_tentativa_Extra_Trees = st.sidebar.checkbox('Modelo Planilha Bloco')

if botao_checkbox_tentativa_Extra_Trees:
    st.markdown(""" ### Projeto de Previsão de Aluguel em Florianópolis- Dados Planilha
        """)
    st.text("""Defina os parâmetros e preveja o valor ideal do aluguel do seu imóvel""")

    x_numericos = {'Condomínio':0, 'IPTU':0, 'Area.1':0, 'Preço/m²':0}   

    x_listas = {'ClassificacaoBairro': ['A', 'B', 'C'] , 'Bairro_':['Abraão', 'Agronômica',
       'Barreiros', 'Cachoeira do Bom Jesus', 'Cacupé',
       'Campeche', 'Capoeiras', 'Carvoeira',
       'Centro', 'Córrego Grande', 'Estreito',
       'Itacorubi', 'Jardim Atlântico', 'Jurerê',
       'Jurerê Internacional', 'Lagoa da Conceição',
       'Saco Grande', 'Saco dos Limões', 'Trindade']}

    dicionario = {}
    for item in x_listas:
        for valor in x_listas[item]:
            dicionario[f'{item}_{valor}'] = 0
        # Definindo parametros numericos
    for item in x_numericos:
        valor = st.sidebar.number_input(f'{item}', step=1.0, value=1.0, format = '%.1f')
        x_numericos[item] = valor

    #Definindo parâmetros categóricos
    for item in x_listas:
       valor = st.sidebar.selectbox(f'{item}', x_listas[item])
       dicionario[f'{item}_{valor}'] = 1

    botao = st.sidebar.button('Calcular o Valor')

    if botao:
        dicionario.update(x_numericos)
        valores_x = pd.DataFrame(dicionario, index=[0])
        modelo = load_model('Tentativa Extra Trees.joblib')
        preco = modelo.predict(valores_x)   
        if preco[0]:
            if preco[0] < 0:
                valor = -1 * preco[0]
                st.success(f"O valor a ser cobrado é de R$ {valor:.2f}")
            else:    
                st.success(f"O valor a ser cobrado é de R$ {preco[0]:.2f}")
           # preco_venda= st.number_input("Valor do imóvel", step=1000.0, value=1.0,format = '%.1f')
           # botao_calcular= st.button("Calcular rentabilidade")
           # if botao_calcular:
            #    rentabilidade = calculo_rentabilidade(float(preco[0]), preco_venda)
             #   st.success(f'A rentabilidade anual por meio do aluguel é de {rentabilidade:.0%}')
            st.button("Reiniciar Parâmetros")
if botao_checkbox:
    st.markdown(""" ### Projeto de Previsão de Aluguel em Florianópolis- Dados do Zap Imóveis
        """)
    st.text("""Defina os parâmetros e preveja o valor ideal do aluguel do seu imóvel""")
    dicionario = {}
    x_numericos = {'Vagas de Garagem':0, 'Total de Banheiros':0,
       'Total de Quartos':0, 'Area Total':0}
    # Definindo parametros numericos
    for item in x_numericos:
        valor = st.sidebar.number_input(f'{item}', step=1.0, value=0.0)
        x_numericos[item] = valor

    botao = st.sidebar.button('Calcular o Valor')

    if botao:
        dicionario.update(x_numericos)
        valores_x = pd.DataFrame(dicionario, index=[0])
        modelo = load_model('Zap Scraper Aluguel Extra Trees.joblib')
        preco = modelo.predict(valores_x)   
        if preco[0]:
            if preco[0] < 0:
                valor = -1 * preco[0]
                st.success(f"O valor a ser cobrado é de R$ {valor:.2f}")
                
            else:    
                st.success(f"O valor a ser cobrado é de R$ {preco[0]:.2f}")

           # preco_venda= st.number_input("Valor do imóvel", step=1000.0, value=1.0,format = '%.1f')
          #  botao_calcular=st.button("Calcular rentabilidade")
           # if botao_calcular:
            #    rentabilidade = calculo_rentabilidade(float(preco[0]), preco_venda)
             #   st.success(f'A rentabilidade anual por meio do aluguel é de {rentabilidade:.0%}')
            st.button("Reiniciar Parâmetros")
if botao_checkbox ==False and botao_checkbox_tentativa_Extra_Trees == False:
    st.title("Dashboard Análise Dimas Construções")

    @st.cache
    def dados_csv():
        df = pd.read_csv("Dados Bloco Convertido.csv")
        return df

    df = dados_csv()



    #------MultiSelect-------

    st.header("Selecione um filtro")
    bairro = st.multiselect( 
        "Selecione o Bairro",
        options=df["Bairro"].unique(),
        default=df["Bairro"].unique(),
    )

    df_selecao = df.query("Bairro == @bairro")

    grafico_alugueis_por_classe = (df_selecao[['Classificação Bairro', 'Aluguel.1']])
    grafico_alugueis_por_bairro = df_selecao[['Aluguel.1', 'Bairro']].groupby('Bairro').sum().sort_values(by='Aluguel.1', ascending=False)
    histograma = df_selecao[['Bairro', 'Aluguel.1', 'Classificação Bairro']]
    fig1 = px.histogram(
        grafico_alugueis_por_classe,
        x = 'Aluguel.1',
        y= 'Classificação Bairro',
        orientation= 'h',
        title= 'Gráfico Valor de aluguel por tipo de Bairro'
    )


    fig2 = px.histogram(
        histograma,
        x = 'Bairro',
        y = 'Aluguel.1',
        title= 'Gráfico Valor de Aluguel por Bairro'
    )

    left_column, right_column = st.columns(2)
    left_column.plotly_chart(fig1, use_container_width=True)

    right_column.plotly_chart(fig2, use_container_width=True)


    botao_dataset = st.checkbox("Mostrar Tabela")

    if botao_dataset:
        st.dataframe(df_selecao)

