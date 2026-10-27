# Justificativa das métricas — Dashboard 2

**Pergunta do dashboard:** como as seleções de Rugby Sevens se comparam em perfil físico e idade?
**Público-alvo:** comissão técnica (treinadores, preparadores físicos e analistas de desempenho).

## Métrica 1: Nº de atletas
- **Variável:** contagem de linhas do dataset (um atleta por linha)
- **O que mede:** quantos atletas há nos países e no gênero selecionados
- **Por que foi escolhida:** toda média só vale se a gente sabe sobre quantos atletas ela foi calculada
- **Público-alvo:** comissão técnica
- **Qual decisão pode ser apoiada por essa métrica?** Decidir se o grupo é grande o bastante para comparar seleções com segurança ou se é só uma impressão de poucos casos
- **O que comunica ao público-alvo:** o tamanho da amostra por trás dos demais indicadores

## Métrica 2: Altura média
- **Variável:** `height` (cm)
- **O que mede:** a altura típica do grupo selecionado
- **Por que foi escolhida:** estatura influencia o contato, a disputa de bola e o posicionamento no rugby
- **Público-alvo:** comissão técnica
- **Qual decisão pode ser apoiada por essa métrica?** Comparar o porte da própria seleção com o dos adversários ao planejar a estratégia de jogo
- **O que comunica ao público-alvo:** se a seleção é mais alta ou mais baixa que as demais

## Métrica 3: Peso médio
- **Variável:** `weight` (kg)
- **O que mede:** a massa corporal típica do grupo selecionado
- **Por que foi escolhida:** a massa pesa no impacto e na resistência ao contato, que são centrais no rugby
- **Público-alvo:** comissão técnica
- **Qual decisão pode ser apoiada por essa métrica?** Ajustar a preparação física e a estratégia de contato conforme o peso dos adversários
- **O que comunica ao público-alvo:** se o grupo tende a ser mais leve ou mais pesado que o restante

## Métrica 4: Idade mediana
- **Variável:** `age` (anos)
- **O que mede:** o valor central da idade: metade dos atletas é mais nova e metade é mais velha
- **Por que foi escolhida:** a mediana não é distorcida por poucos atletas muito jovens ou muito velhos, o que a média não garante
- **Público-alvo:** comissão técnica
- **Qual decisão pode ser apoiada por essa métrica?** Planejar renovação do elenco e carga de treino conforme a maturidade do grupo
- **O que comunica ao público-alvo:** se a seleção é, em geral, jovem ou experiente

## Métrica 5: IMC médio
- **Variável:** `weight` e `height`, combinadas como peso / (altura em metros)²
- **O que mede:** a massa corporal relativa à altura
- **Por que foi escolhida:** peso sozinho confunde atletas altos com atletas robustos; o IMC permite comparar grupos de portes diferentes
- **Público-alvo:** comissão técnica
- **Qual decisão pode ser apoiada por essa métrica?** Identificar se uma seleção é mais compacta e forte ou mais alta e esguia, e adaptar a preparação
- **O que comunica ao público-alvo:** o perfil corporal do grupo. Atenção: em atleta de força o IMC alto pode refletir massa muscular, não excesso de gordura

## Métrica 6: Amplitude de idade
- **Variável:** `age` (máximo − mínimo)
- **O que mede:** a distância entre o atleta mais novo e o mais velho do grupo
- **Por que foi escolhida:** complementa a mediana mostrando se o elenco é homogêneo ou se mistura gerações
- **Público-alvo:** comissão técnica
- **Qual decisão pode ser apoiada por essa métrica?** Avaliar o equilíbrio entre atletas experientes e jovens promessas na composição do elenco
- **O que comunica ao público-alvo:** o grau de variedade etária da seleção
