import altair as alt
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
CORES_GENERO = {"Female": "#b57edc", "Male": COR_DESTAQUE}


@st.cache_data
def filtrar_por_intervalos(dados, intervalos):
    """Mantém só os atletas dentro de todos os intervalos escolhidos."""
    filtrado = dados
    for var, (inicio, fim) in intervalos.items():
        filtrado = filtrado[filtrado[var].between(inicio, fim)]
    return filtrado


@st.cache_data
def calcular_correlacao(dados, variaveis):
    """Matriz de correlação de Spearman entre as variáveis escolhidas."""
    return dados[variaveis].corr(method="spearman")


@st.cache_data
def contagem_por_faixa_etaria(dados, largura=2):
    """Nº de atletas por faixa de idade (ex.: "26–27") e gênero, e a ordem das faixas."""
    inicio, fim = int(dados["age"].min()), int(dados["age"].max())
    limites = list(range(inicio, fim + largura + 1, largura))
    rotulos = [f"{a}–{a + largura - 1}" for a in limites[:-1]]
    faixa = pd.cut(dados["age"], bins=limites, labels=rotulos, right=False)
    contagem = (
        dados.assign(faixa=faixa.astype(str))
        .groupby(["faixa", "gender"])
        .size()
        .reset_index(name="atletas")
    )
    return contagem, rotulos


@st.cache_data
def medias_por_pais(dados):
    """Altura média e nº de atletas de cada país (base das barras do Dashboard 2)."""
    return (
        dados.groupby("country")
        .agg(altura_media=("height", "mean"), atletas=("code", "count"))
        .reset_index()
    )


def dashboard_1(df):
    # Filtros do Dashboard 1 ficam na sidebar (variáveis + intervalo + gênero)
    with st.sidebar:
        st.header("Filtros do Dashboard 1")

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

    df_filtrado = filtrar_por_intervalos(df, intervalos)

    # return (e não st.stop()) para não interromper a aba do Dashboard 2
    if df_filtrado.empty:
        st.warning("Nenhum atleta dentro dos intervalos escolhidos. Amplie os filtros.")
        return

    # Distribuição (histograma), em largura total
    with st.container(border=True):
        cabecalho, escolha = st.columns([3, 1])
        cabecalho.subheader("Distribuição")

        if not variaveis:
            st.info("Selecione pelo menos 1 variável nos filtros.")
        else:
            var_hist = escolha.selectbox(
                "Variável", options=variaveis, label_visibility="collapsed"
            )
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
            # Barras com cantos arredondados e um pequeno espaço entre elas
            fig_hist.update_traces(marker_cornerradius=6)
            fig_hist.update_layout(
                yaxis_title="atletas", margin=dict(t=10, b=10), height=380, bargap=0.08
            )
            st.plotly_chart(fig_hist, width="stretch")

    # Correlação (heatmap) e leitura rápida (KPIs), lado a lado
    col_correlacao, col_leitura = st.columns(2)

    corr = None
    with col_correlacao.container(border=True):
        st.subheader("Correlação")

        if len(variaveis) < 2:
            st.warning("Selecione pelo menos 2 variáveis para calcular a correlação.")
        else:
            corr = calcular_correlacao(df_filtrado, variaveis)
            # Só o triângulo inferior (com a diagonal): o superior repetiria os mesmos valores
            corr_triangular = corr.where(np.tril(np.ones(corr.shape, dtype=bool)))
            fig_corr = px.imshow(
                corr_triangular,
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


def dashboard_2(df):
    st.subheader("Como as seleções de rugby se comparam em perfil físico e idade?")

    # Filtros do Dashboard 2 ficam no topo da aba, independentes dos do Dashboard 1
    col_pais, col_genero = st.columns([3, 1])
    paises = col_pais.multiselect(
        "Países",
        options=sorted(df["country"].unique()),
        default=[],
        placeholder="Todos os países",
        help="Escolha as seleções a comparar. Vazio = todas.",
        key="d2_paises",
    )
    genero = col_genero.radio(
        "Gênero",
        options=["Todos", "Female", "Male"],
        horizontal=True,
        key="d2_genero",
    )

    df2 = df
    if paises:
        df2 = df2[df2["country"].isin(paises)]
    if genero != "Todos":
        df2 = df2[df2["gender"] == genero]

    if df2.empty:
        st.warning("Nenhum atleta com os filtros escolhidos. Amplie a seleção.")
        return

    # Espaço dos KPIs reservado aqui (topo da página) e preenchido só no fim,
    # depois de saber quais países foram clicados nas barras
    area_kpis = st.container()

    col_barras, col_dispersao = st.columns(2)

    with col_barras.container(border=True):
        st.subheader("Altura média por país")

        # O clique numa barra seleciona o país; vem para o Python via on_select
        clique = alt.selection_point(name="pais", fields=["country"])
        barras = (
            alt.Chart(medias_por_pais(df2))
            .mark_bar(cornerRadiusEnd=6, color=COR_DESTAQUE)
            .encode(
                y=alt.Y("country:N", sort="-x", title=None),
                x=alt.X("altura_media:Q", title="altura média (cm)"),
                opacity=alt.condition(clique, alt.value(1), alt.value(0.35)),
                tooltip=[
                    alt.Tooltip("country:N", title="país"),
                    alt.Tooltip("altura_media:Q", title="altura média (cm)", format=".1f"),
                    alt.Tooltip("atletas:Q", title="atletas"),
                ],
            )
            .add_params(clique)
            .properties(height=alt.Step(22))
        )
        evento = st.altair_chart(barras, key="barras_pais", on_select="rerun", width="stretch")
        st.caption("Clique numa barra para filtrar o restante do dashboard (shift para vários).")

    # Países clicados; sem clique, todos os que passaram pelos filtros
    paises_clicados = [item["country"] for item in evento.selection.get("pais", [])]
    df_sel = df2[df2["country"].isin(paises_clicados)] if paises_clicados else df2
    if df_sel.empty:  # clique antigo num país que saiu dos filtros
        df_sel = df2

    cor_genero = alt.Color(
        "gender:N",
        title="gênero",
        scale=alt.Scale(domain=list(CORES_GENERO), range=list(CORES_GENERO.values())),
    )

    with col_dispersao.container(border=True):
        st.subheader("Altura × peso")
        dispersao = (
            alt.Chart(df_sel)
            .mark_circle(size=60, opacity=0.7)
            .encode(
                x=alt.X("height:Q", title="altura (cm)", scale=alt.Scale(zero=False)),
                y=alt.Y("weight:Q", title="peso (kg)", scale=alt.Scale(zero=False)),
                color=cor_genero,
                tooltip=[
                    alt.Tooltip("name:N", title="atleta"),
                    alt.Tooltip("country:N", title="país"),
                    alt.Tooltip("height:Q", title="altura (cm)"),
                    alt.Tooltip("weight:Q", title="peso (kg)"),
                    alt.Tooltip("age:Q", title="idade"),
                ],
            )
            .properties(height=380)
        )
        st.altair_chart(dispersao, width="stretch")

    with st.container(border=True):
        st.subheader("Distribuição de idade")
        # Barras lado a lado (xOffset): empilhadas, a altura total pareceria ser a de um só gênero
        faixas, ordem_faixas = contagem_por_faixa_etaria(df_sel)
        histograma = (
            alt.Chart(faixas)
            .mark_bar(cornerRadiusTopLeft=6, cornerRadiusTopRight=6)
            .encode(
                x=alt.X("faixa:O", sort=ordem_faixas, title="idade (anos)", axis=alt.Axis(labelAngle=0)),
                xOffset="gender:N",
                y=alt.Y("atletas:Q", title="atletas"),
                color=cor_genero,
                tooltip=[
                    alt.Tooltip("faixa:O", title="idade"),
                    alt.Tooltip("gender:N", title="gênero"),
                    alt.Tooltip("atletas:Q", title="atletas"),
                ],
            )
            .properties(height=260)
        )
        st.altair_chart(histograma, width="stretch")

    # KPIs calculados sobre os atletas selecionados (df_sel)
    imc = df_sel["weight"] / (df_sel["height"] / 100) ** 2  # peso (kg) / altura (m)²
    amplitude_idade = int(df_sel["age"].max() - df_sel["age"].min())

    with area_kpis:
        if paises_clicados:
            st.caption("Mostrando: " + ", ".join(paises_clicados))
        kpis = st.columns(6)
        kpis[0].metric("Atletas", f"{len(df_sel)}")
        kpis[1].metric("Altura média", f"{df_sel['height'].mean():.1f} cm")
        kpis[2].metric("Peso médio", f"{df_sel['weight'].mean():.1f} kg")
        kpis[3].metric("Idade mediana", f"{df_sel['age'].median():.0f} anos")
        kpis[4].metric("IMC médio", f"{imc.mean():.1f}")
        kpis[5].metric("Amplitude de idade", f"{amplitude_idade} anos")


aba1, aba2 = st.tabs(["Dashboard 1", "Dashboard 2"])

with aba1:
    dashboard_1(df)

with aba2:
    dashboard_2(df)
