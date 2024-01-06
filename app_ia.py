import streamlit as st
import yfinance as yf
from prophet import Prophet
from prophet.plot import plot_plotly
from plotly import graph_objs as go
from datetime import date


st.title("Aplicação de Análise Preditiva Feito por André Augusto Eleutério")

lista_tickers = ["PETR4.SA", "ABEV3.SA", "MGLU3.SA",
                  "BBAS3.SA", "GOOG", "APPL", "MSFT"]

tickers = {
    "PETR4.SA": "Petrobras",
    "ABEV3.SA": "Ambev",
    "MGLU3.SA": "Magazine Luiza",
    "BBAS3.SA": "Banco do Brasil",
    "GOOG": "Google",
    "AAPL": "Apple",
    "MSFT": "Microsoft"
}

def carregar_dados(ticker, dt_inicial, dt_final):
    df = yf.Ticker(ticker).history(start=dt_inicial.strftime("%Y-%m-%d"), 
                                end= dt_final.strftime("%Y-%m-%d"))
    return df
 
def prever_dados(df, periodo):
    df.reset_index(inplace=True)
    df = df.loc[:, ['Date', 'Close']]
    df['Date'] = df['Date'].dt.tz_localize(None)
    df.rename(columns= {"Date": "ds", "Close": "y"}, inplace= True)

    modelo = Prophet()
    modelo.fit(df)

    datas_futuras = modelo.make_future_dataframe(periods=int(periodo) * 30)
    previsoes = modelo.predict(datas_futuras)
    return modelo, previsoes

st.image("logo.jpg")

with st.sidebar:
    st.header("Menu")
    ticker = st.selectbox ("Selecione a Carteira:" , lista_tickers)
    dt_inicial = st.date_input("Data Inicial", value=date(2022, 1, 1))
    dt_final = st.date_input ("Data Final")
    meses = st.number_input("Meses de Previsão", 1, 24, value=6)

dados = carregar_dados(ticker, dt_inicial, dt_final)

if dados.shape [0] != 0:
    st.header (f"Dados da ação - {tickers[ticker]}")
    st.dataframe(dados)

    st.subheader("Variação do Período")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=dados.index, y= dados['Close'], name= "Open"))
    st.plotly_chart(fig)

    st.header(f"Previsão dos prôximos {meses} meses!")
    modelo, previsoes = prever_dados(dados, meses)
    fig = plot_plotly(modelo, previsoes)
    st.plotly_chart(fig)
    


else:
    st.warning("Nenhum dado encontrado no período selecionado!")
