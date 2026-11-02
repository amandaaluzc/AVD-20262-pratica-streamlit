# Atletas das Olimpíadas 2024: Rugby Sevens

Trabalho desenvolvido para a disciplina **Análise e Visualização de Dados (AVD)** da CESAR School, período 2026.2 (Aulas 21, 22 e 23 — Streamlit), por **Amanda Luz**.

**App publicado:** <https://avd-20262-pratica-app-amandaaluzc.streamlit.app/>

## Sobre o projeto

O projeto começou como uma análise exploratória (EDA) dos **atletas dos Jogos Olímpicos de Paris 2024**, a partir do dataset [Olympics 2024](https://www.kaggle.com/datasets/willianoliveiragibin/olympics-2024) do Kaggle. Ao longo da EDA, o recorte foi se fechando nos atletas de **Rugby Sevens**: é uma modalidade com seleções masculinas e femininas de tamanho parecido e com dados de altura e peso preenchidos, o que permite comparar o perfil físico entre países e gêneros de forma justa.

O dataset tratado (`data/clean/dataset.csv`) tem **316 atletas** (157 do feminino e 159 do masculino). As variáveis quantitativas estudadas são:

| Variável | Significado |
| --- | --- |
| `height` | altura (cm) |
| `weight` | peso (kg) |
| `age` | idade (anos), calculada a partir da data de nascimento |

Os dois dashboards ficam no mesmo app, separados em **abas**.

### Dashboard 1: laboratório de distribuição e correlação

Um espaço para explorar as variáveis quantitativas e ver como elas se relacionam.

- **Filtros (barra lateral):**
  - seletor das variáveis que entram na análise (`height`, `weight`, `age`);
  - um slider de intervalo por variável, para excluir valores (por exemplo, extremos) e ver se isso muda a leitura;
  - opção "Distinguir por gênero", que separa o histograma por cor.
- **Distribuição:** histograma da variável escolhida numa lista, com a opção de comparar feminino e masculino.
- **Correlação:** mapa de calor com a correlação de Spearman entre as variáveis selecionadas (só o triângulo inferior, para não repetir valores).
- **Leitura rápida:** número de atletas, altura média, idade média e peso médio do recorte filtrado.

Tudo é recalculado quando um filtro muda. Com menos de 2 variáveis selecionadas, o app avisa que não há como calcular a correlação.

### Dashboard 2: KPIs para a comissão técnica

Responde à pergunta: **como as seleções de Rugby Sevens se comparam em perfil físico?** O público-alvo é a comissão técnica (treinadores, preparadores físicos e analistas de desempenho).

- **Filtros (topo da aba, independentes do Dashboard 1):** países e gênero.
- **KPIs:**
  - Nº de atletas: tamanho da amostra por trás dos indicadores;
  - Altura média;
  - Peso médio;
  - IMC médio: peso relativo à altura, para comparar grupos de portes diferentes.
- **Visuais (Altair):**
  - **Altura média por país:** barras clicáveis; clicar num país filtra os KPIs e os outros gráficos (shift para vários);
  - **Altura × peso:** dispersão com o feminino em triângulos roxos e o masculino em círculos azuis;
  - **Distribuição de idade:** faixas de 2 anos com barras lado a lado por gênero.

A justificativa de cada métrica está em [entregas/justificativa-metricas.md](entregas/justificativa-metricas.md), e os rascunhos de layout dos dois dashboards estão em [entregas/](entregas).

### Stack

Python, pandas e NumPy para os dados; Streamlit para o app; Plotly no Dashboard 1 e Altair no Dashboard 2; deploy no Streamlit Community Cloud.

### Estrutura do repositório

| Caminho | Conteúdo |
| --- | --- |
| `app.py` | o app com os dois dashboards |
| `src/data_loader.py` | leitura do dataset tratado, com cache |
| `notebooks/eda.ipynb` | EDA original (Aula 11) |
| `notebooks/eda-com-downloads.ipynb` | EDA com o download do dataset e a exportação para `data/clean/` |
| `data/clean/dataset.csv` | dataset tratado, lido pelo app |
| `entregas/` | rascunhos dos dashboards e justificativa das métricas |
| `prompts/` | declaração de uso de IA e template de prompt |

---

*As seções abaixo vêm do repositório-modelo da disciplina e explicam como rodar o projeto localmente.*

## Setup

Requer **Python 3.11 a 3.15**. Confira a sua versão antes de começar:

| Sistema | Verificar versão |
| --- | --- |
| macOS / Linux | `python3 --version` |
| Windows | `py --version` |

### 1. Criar e ativar o ambiente virtual

O nome do comando do Python muda por sistema (em muitas máquinas `python` nem existe). Use a linha do seu sistema:

| Sistema | Criar | Ativar |
| --- | --- | --- |
| macOS / Linux | `python3 -m venv .venv` | `source .venv/bin/activate` |
| Windows (PowerShell) | `py -m venv .venv` | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `py -m venv .venv` | `.venv\Scripts\activate.bat` |

Se você tem várias versões instaladas, escolha uma compatível, por exemplo `python3.12 -m venv .venv` (macOS/Linux) ou `py -3.12 -m venv .venv` (Windows).

Com o ambiente ativo, o terminal mostra `(.venv)` no início da linha. **A partir daqui os comandos são iguais em todos os sistemas**, porque dentro do venv `python` e `pip` sempre existem.

### 2. Instalar, configurar a IA e rodar

```bash
python -m pip install -r requirements.txt

# Skills de IA do Streamlit (ver seção "IA neste projeto")
streamlit skills --yes

streamlit run app.py
```

### Problemas comuns

- **`python: command not found` / `python` não é reconhecido:** use `python3` (macOS/Linux) ou `py` (Windows) só para criar o venv; depois de ativado, `python` funciona.
- **Linux (Debian/Ubuntu): `ensurepip is not available` ou `No module named venv`:** instale `sudo apt install python3-venv` (ou `python3.X-venv` para a sua versão).
- **Windows: "a execução de scripts foi desabilitada" ao ativar no PowerShell:** rode uma vez `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`, ou use o cmd.
- **Python fora de 3.11–3.15:** instale uma versão compatível em [python.org](https://www.python.org/downloads/) e crie o venv com ela, como no exemplo acima.
- **Apareceu `ModuleNotFoundError` ou `streamlit: command not found`:** o venv provavelmente não está ativo. Ative de novo e confira o `(.venv)` no prompt.
- **Erro de certificado no `pip install` (macOS, Python do python.org):** rode `Install Certificates.command`, na pasta Python 3.X em Aplicativos.
- **`DatasetNotFoundError` ao baixar o dataset no notebook (macOS, Python do python.org):** é o mesmo problema de certificado SSL (o `pandas` não consegue ler o CSV da UCI). Rode `Install Certificates.command` e reinicie o kernel. O notebook `eda-com-downloads.ipynb` já define `SSL_CERT_FILE` com o `certifi` como contorno.

## Estrutura de dados: `data/raw` vs `data/clean`

- `data/raw/`: o dataset **bruto**, como foi baixado. Nunca é editado à mão.
- `data/clean/`: o dataset **já tratado**, exportado na última célula do notebook de EDA (ex.: `df.to_csv("data/clean/dataset.csv", index=False)`). O `app.py` lê **somente** desta pasta, via `src/data_loader.py`.

### O que vai para o Git

| Pasta | Versionada? | Por quê |
| --- | --- | --- |
| `data/raw/` | **Não** (só o `.gitkeep`) | O bruto pode ser grande ou ter dados sensíveis, e o app não o usa. |
| `data/clean/` | **Sim** | O Streamlit Community Cloud faz deploy a partir do GitHub e só enxerga o que está no repositório. Sem o CSV tratado no repo, o app funciona na sua máquina e **quebra no deploy**. |

### Antes de dar `git push` com o dado tratado

- **O dado é público ou pode ser compartilhado?** Se não for claramente público, use um **repositório privado** (o Community Cloud permite conectar repositórios privados ao autorizar o GitHub; confirme na hora do deploy). Nesse caso, dê acesso de leitura ao professor (como colaborador ou pela organização).
- **Dado sensível** (nomes, CPF, e-mail, telefone, localização exata etc.): remova ou anonimize na EDA, antes de exportar para `data/clean/`. Isso vale mesmo em repositório privado.
- **Tamanho:** o GitHub rejeita arquivos acima de **100 MB**. Se o CSV tratado for grande, reduza colunas e linhas na EDA ou exporte em Parquet (`df.to_parquet(...)`, exige `pyarrow`).
- **Lembre de commitar o arquivo:** confira com `git status` que `data/clean/dataset.csv` aparece como novo arquivo.

## Passo a passo

O passo a passo detalhado de cada aula (Aulas 21, 22 e 23), com pré-requisitos e objetivos, está em [ROTEIRO.md](ROTEIRO.md). Comece por ele depois do Setup.

**Link do app (Aula 23):** <https://avd-20262-pratica-app-amandaaluzc.streamlit.app/>

## IA neste projeto

Este projeto usa o **streamlit skills**: um conjunto de instruções (arquivos `SKILL.md`) que a ferramenta de IA lê para escrever código Streamlit seguindo boas práticas (estrutura de layout, cache, widgets, etc.).

**Como instalar:** depois do `pip install -r requirements.txt`, rode na raiz do projeto:

```bash
streamlit skills        # interativo
streamlit skills --yes  # sem confirmações
```

O comando cria *symlinks* para as skills que acompanham a sua instalação do Streamlit, então elas se atualizam sozinhas quando você atualiza o pacote. (A opção `--global` instala para todos os projetos, em vez de só este.)

**Onde fica instalado:**

- `.claude/skills/`: lido pelo Claude Code.
- `.agents/skills/`: lido pelo Gemini CLI, que já encontra essa pasta sozinho.

Essas pastas **não são versionadas** (ver `.gitignore`): os symlinks apontam para o seu ambiente virtual e não funcionam em outra máquina. Cada pessoa roda `streamlit skills` no próprio clone.

**Se você usa outra ferramenta** (ChatGPT, Copilot Chat, etc.): abra o `SKILL.md` correspondente em `.agents/skills/` e cole o conteúdo manualmente no início do chat, antes do seu pedido.

O uso de IA deve ser declarado conforme a seção abaixo.

## Pasta `prompts/`

A pasta [prompts/](prompts) guarda só o que é sobre **uso de IA**: o template de prompt para transformar o rascunho de layout em esqueleto de código e a **Declaração de Uso de IA** exigida pelo Plano de Ensino. Veja [prompts/README.md](prompts/README.md).

## Pasta `entregas/`

A pasta [entregas/](entregas) guarda os artefatos de entrega que não são sobre IA: os rascunhos de layout de cada dashboard (`.jpg` ou `.png`) e a justificativa das métricas do Dashboard 2. Veja [entregas/README.md](entregas/README.md) para o detalhe de cada arquivo e o checklist por aula. Não coloque esses arquivos no `.gitignore`.
