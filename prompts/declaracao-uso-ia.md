# Declaração de Uso de IA

**Nome:** Amanda Luz
**Data:** 27/10/2026 (Aula 22 — Streamlit, parte 2)

## Ferramenta

Claude Code (CLI da Anthropic), modelo Claude Sonnet 5.5 (`claude-sonnet-5-5`). A ferramenta leu os arquivos do repositório, editou o código diretamente e rodou o app em modo de teste (`streamlit.testing`, sem navegador). Eu abri o app no navegador e conferi o resultado visual.

## Prompt usado

Principais pedidos, na ordem em que aconteceram:

1. "preciso puxar novas informações de um repositório do git, mas não é o que eu estou sincronizada. Como devo fazer?" (indicando depois o repositório da professora)
2. "faça os ajustes para remover os conflitos. o que eu puxei que quero guardar são as informações. Quero que você deixe o que eu fiz do meu projeto. Isso que puxei foi do repositório da minha professora."
3. "vamos trabalhar na aula 22, parte 2. va me guiando para que eu possa entender o que esta sendo feito. Tudo está no roteiro no md"
4. "sim, aplique o cache e mantenha o Plotly"
5. "quero usar a matriz de correlação em formato triangular"
6. "quero deixar as barras menos retangulares"
7. "vamos para o passo 4, estruturar o dashboard 2" (escolhi a pergunta do dashboard, o público-alvo "comissão técnica" e aprovei as 6 métricas sugeridas)
8. "vamos deixar independente" (filtros do Dashboard 2 separados dos do Dashboard 1, em abas)
9. "vamos para o passo 6" (gráficos do Dashboard 2 em Altair)
10. "não gostei das cores que foram usadas para distinguir o gênero. use roxo para o feminino" e, depois, "não ficou muito interessante essa cor, pois tem pouco contraste com o azul"
11. "o gráfico de distribuição de idade não está fazendo sentido, eu verifiquei que alguns têm menos mulheres entre 26 e 28 anos, mas no gráfico parece que as mulheres têm mais que os homens, o que é equivocado"
12. "prepare o rascunho do uso de ia" (este documento)

## O que foi aceito, modificado ou rejeitado e por quê

- **Aceito:**
  - Resolução do conflito de merge mantendo a minha versão de `app.py` e `.streamlit/config.toml`; o material da professora (roteiro, README, pasta `entregas/`) entrou normalmente.
  - Cache com `@st.cache_data` no carregamento dos dados, no filtro por intervalos e na matriz de correlação.
  - Matriz de correlação só com o triângulo inferior (`np.tril`).
  - Barras do histograma do Dashboard 1 com cantos arredondados.
  - Estrutura em abas (`st.tabs`) com o Dashboard 1 em função própria e o Dashboard 2 com filtros próprios (país e gênero).
  - Os 6 KPIs do Dashboard 2 (nº de atletas, altura média, peso médio, idade mediana, IMC médio, amplitude de idade).
  - Gráficos do Dashboard 2 em Altair (barras de altura média por país clicáveis, dispersão altura × peso, distribuição de idade), com o clique nas barras filtrando KPIs e demais gráficos via `on_select`.
- **Modificado:**
  - A cor do gênero feminino: a IA usou laranja; pedi roxo; o primeiro roxo (`#8e44ad`) tinha pouco contraste com o azul, e foi trocado por um lilás mais claro (`#b57edc`).
  - O gráfico de distribuição de idade do Dashboard 2: a primeira versão empilhava as barras por gênero e passava a impressão errada (as mulheres pareciam ser mais numerosas). Eu percebi comparando com os dados; a correção foi usar barras lado a lado e faixas de idade calculadas no pandas, que conferi contra a contagem real.
  - A justificativa das métricas (`entregas/justificativa-metricas.md`) foi escrita pela IA como primeira versão. <!-- ajustar: descreva o que você revisou/reescreveu -->
- **Rejeitado:**
  - Migrar o Dashboard 1 de Plotly para Altair: a IA ofereceu a opção e eu decidi manter o Plotly nesse dashboard, usando Altair só no Dashboard 2, como pede o roteiro.
  - Resolver o conflito de merge aproveitando partes da versão da professora em `app.py`: preferi manter integralmente a minha.
  - O rascunho do layout do Dashboard 2 não foi gerado pela IA: ela só sugeriu um esquema em texto, e o desenho em `entregas/rascunho-dashboard2.png` é meu. <!-- confirmar quando o rascunho estiver pronto -->

<!-- Itens com comentário HTML acima são para você completar ou apagar antes de entregar. -->
