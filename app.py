import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

from src.data_loader import load_data

TITULO = "Atletas das Olimpíadas 2024"

st.set_page_config(page_title=TITULO, layout="wide")

st.title(TITULO)

df = load_data()

# Variáveis quantitativas do estudo (mesma lista VARS_QUANT do notebook de EDA)
VARS_QUANT = ["height", "weight", "age"]

COR_DESTAQUE = "#2f6f8f"
CORES_GENERO = {"Female": "#e9a23b", "Male": COR_DESTAQUE}

# Sidebar: filtros (variáveis + intervalo + gênero)
with st.sidebar:
    st.header("Filtros")

    variaveis = st.multiselect(
        "Variáveis",
        options=VARS_QUANT,
        default=VARS_QUANT,
        help="Selecione as variáveis quantitativas que deseja analisar no dashboard.",
    )

    # Um slider de intervalo para cada variável selecionada
    intervalos = {}
    if variaveis:
        st.subheader("Intervalos")
    for var in variaveis:
        if pd.api.types.is_integer_dtype(df[var]):
            minimo, maximo, passo = int(df[var].min()), int(df[var].max()), 1
        else:
            minimo, maximo, passo = float(df[var].min()), float(df[var].max()), 0.1
        intervalos[var] = st.slider(
            var,
            min_value=minimo,
            max_value=maximo,
            value=(minimo, maximo),
            step=passo,
            key=f"intervalo_{var}",
        )

    separar_por_genero = st.toggle(
        "Distinguir por gênero",
        value=False,
        help="Colore a distribuição pelo gênero (Female ou Male).",
    )

# Mantém só os atletas dentro de todos os intervalos escolhidos
df_filtrado = df
for var, (inicio, fim) in intervalos.items():
    df_filtrado = df_filtrado[df_filtrado[var].between(inicio, fim)]

if df_filtrado.empty:
    st.warning("Nenhum atleta dentro dos intervalos escolhidos. Amplie os filtros.")
    st.stop()

# Distribuição (histograma), em largura total
with st.container(border=True):
    cabecalho, escolha = st.columns([3, 1])
    cabecalho.subheader("Distribuição")

    if not variaveis:
        st.info("Selecione pelo menos 1 variável nos filtros.")
    else:
        var_hist = escolha.selectbox("Variável", options=variaveis, label_visibility="collapsed")
        fig_hist = px.histogram(
            df_filtrado,
            x=var_hist,
            color="gender" if separar_por_genero else None,
            color_discrete_map=CORES_GENERO,
            barmode="overlay",
            opacity=0.8,
            labels={var_hist: var_hist, "count": "atletas"},
        )
        if not separar_por_genero:
            fig_hist.update_traces(marker_color=COR_DESTAQUE)
        fig_hist.update_layout(yaxis_title="atletas", margin=dict(t=10, b=10), height=380)
        st.plotly_chart(fig_hist, width="stretch")

# Correlação (heatmap) e leitura rápida (KPIs), lado a lado
col_correlacao, col_leitura = st.columns(2)

corr = None
with col_correlacao.container(border=True):
    st.subheader("Correlação")

    if len(variaveis) < 2:
        st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
    else:
        corr = df_filtrado[variaveis].corr(method="spearman")
        fig_corr = px.imshow(
            corr,
            text_auto=".2f",
            zmin=-1,
            zmax=1,
            color_continuous_scale="RdBu_r",
        )
        fig_corr.update_layout(margin=dict(t=10, b=10), height=300)
        st.plotly_chart(fig_corr, width="stretch")
        st.caption("Correlação de Spearman.")

with col_leitura.container(border=True):
    st.subheader("Leitura rápida")

    # Par de variáveis com a maior correlação (em módulo), fora da diagonal
    if corr is None:
        maior_correlacao = "—"
    else:
        pares = corr.where(np.triu(np.ones(corr.shape, dtype=bool), k=1)).stack()
        a, b = pares.abs().idxmax()
        valor = pares[(a, b)]
        maior_correlacao = f"{a} × {b} ({valor:.2f})"

    n_female = int((df_filtrado["gender"] == "Female").sum())
    n_male = int((df_filtrado["gender"] == "Male").sum())

    kpis = [
        ("Atletas", f"{len(df_filtrado)}"),
        ("Altura média", f"{df_filtrado['height'].mean():.0f} cm"),
        ("Peso médio", f"{df_filtrado['weight'].mean():.0f} kg"),
        ("Idade média", f"{df_filtrado['age'].mean():.0f} anos"),
        ("Maior correlação", maior_correlacao),
        ("Female / Male", f"{n_female} / {n_male}"),
    ]
    for linha in (kpis[:3], kpis[3:]):
        for coluna, (rotulo, valor) in zip(st.columns(3), linha):
            with coluna.container(border=True):
                st.caption(rotulo)
                st.markdown(f"**{valor}**")
