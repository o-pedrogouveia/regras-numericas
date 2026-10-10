
# Adivinhador de Regras Numéricas

Projeto acadêmico desenvolvido em dupla, em Python, para a disciplina MC102 (Algoritmos e Programação de Computadores), da Universidade Estadual de Campinas (Unicamp), no primeiro semestre de 2026.

O projeto foi realizado como parte das atividades avaliativas da disciplina, com o objetivo de aplicar conceitos de programação, raciocínio algorítmico e estratégias de busca na resolução de problemas.

## Sobre o projeto

O desafio consiste em desenvolver um algoritmo capaz de identificar uma regra numérica desconhecida, selecionada previamente pelo ambiente do jogo. Para descobrir a regra, o algoritmo pode realizar consultas numéricas e receber informações sobre os resultados.

Cada consulta informa:

- Se o número consultado satisfaz a regra;
- Caso não satisfaça, se o número válido (isto é, pertencente à regra) mais próximo é maior ou menor que o número consultado.

Com base nessas informações, o algoritmo deve escolher as próximas consultas e, quando identificar uma possível solução, propor a regra e seus parâmetros.

## Regras numéricas possíveis

O problema considera números inteiros de 1 a 100.000 e três categorias de regras.

### 1. Resto de divisão

A regra seleciona os números cujo resto da divisão por um inteiro `k` é igual a `r`.

Exemplo:

`n % 5 == 2`

Nesse caso, os números válidos incluem `2, 7, 12, 17, ...`.

### 2. Potências perfeitas

A regra seleciona números que podem ser representados como potências inteiras de determinada ordem `p`.

Exemplo:

Para `p = 3`, os números válidos incluem `1, 8, 27, 64, ...`.

### 3. Intervalos numéricos

A regra seleciona todos os números pertencentes a um intervalo fechado `[a, b]`.

Exemplo:

Para o intervalo `[100, 105]`, os números válidos são `100, 101, 102, 103, 104, 105`.

Os parâmetros de cada regra são inicialmente desconhecidos e devem ser identificados pelo algoritmo.

## Estratégia implementada

O algoritmo foi estruturado em três estratégias de investigação, correspondentes às categorias de regras previstas no problema: potências perfeitas, restos de divisão e intervalos numéricos.

A função principal `player()` coordena essas estratégias, utilizando o histórico de consultas e variáveis de estado para determinar a próxima ação. O algoritmo não conhece previamente a categoria da regra e precisa identificá-la durante a execução.

### 1. Identificação de potências perfeitas

A investigação começa com uma consulta ao número `1`, que pertence a todas as regras de potência perfeita.

Caso a resposta seja positiva, o algoritmo inicia uma sequência de consultas envolvendo potências de base 3:

`3, 9, 27, 81, 243, ...`

Para uma regra de potência perfeita de ordem `p`, o primeiro valor da sequência `3¹, 3², ...` que satisfaz essa regra é `3^p`. Assim, a posição da primeira potência compatível permite identificar uma possível ordem `p` e propor a regra correspondente.

Chutes de regra incorretos e respostas incompatíveis permitem ao algoritmo abandonar essa hipótese e investigar outras categorias.

### 2. Identificação de regras de resto

Para regras da forma `n % k == r`, o objetivo é determinar dois parâmetros desconhecidos: o divisor `k` e o resto `r`.

Inicialmente, o algoritmo consulta valores predefinidos, escolhidos para investigar a existência de números válidos próximos ao início do domínio.

A partir das respostas, utiliza a direção do número válido mais próximo para orientar novas consultas. Nessa etapa, emprega deslocamentos progressivamente menores para localizar um número que satisfaça a regra.

Após identificar um valor relevante para o resto, a função `acha_divisor()` realiza consultas adicionais para localizar outra ocorrência da regra e determinar o divisor a partir da distância entre valores válidos.

A implementação também possui tratamentos específicos para situações em que o resto é zero.

### 3. Identificação de intervalos numéricos

Para regras que definem um intervalo fechado `[a, b]`, o algoritmo precisa encontrar seus limites inferior e superior.

A busca começa no número `50.000`, aproximadamente no centro do domínio permitido.

Quando o número consultado não pertence ao intervalo, a direção retornada pelo jogo determina o sentido da próxima consulta.

O algoritmo utiliza deslocamentos progressivamente menores, baseados em divisões sucessivas do domínio por potências de 2, até encontrar um número válido.

Após localizar um número pertencente ao intervalo, a função `busca_bordas()` procura suas extremidades:

- Para o limite superior, realiza consultas avançando de duas em duas unidades e verifica valores vizinhos quando ultrapassa a borda.
- Para o limite inferior, repete o procedimento no sentido contrário.
- Os limites globais `1` e `100.000` recebem tratamento específico.

### 4. Gerenciamento das consultas e do estado

A implementação utiliza listas, contadores e variáveis booleanas para controlar o progresso da investigação.

Entre as informações armazenadas estão:

- Histórico de números consultados e respostas recebidas;
- Números identificados como válidos;
- Potências e valores utilizados durante a investigação;
- Parâmetros intermediários e limites já identificados;
- Estratégia de investigação atualmente ativa.

Essas informações permitem que o algoritmo adapte suas próximas consultas aos resultados anteriores, em vez de investigar os números sequencialmente.

O estado é reinicializado pelo ambiente de avaliação no início de cada partida.


## Estrutura do repositório

```text
regras-numericas/
├── .gitignore
├── player.py
└── README.md
```

- **`player.py`:** implementação do algoritmo e de suas funções auxiliares.
- **`README.md`:** documentação e contextualização do projeto.

## Funcionamento e execução

A função principal possui a seguinte assinatura:

```python
player(number_guesses, rule_guesses)
```

Ela recebe:

- `number_guesses`: histórico das consultas numéricas e de suas respectivas respostas;
- `rule_guesses`: histórico das regras anteriormente propostas.

A função retorna uma das seguintes ações:

- `NUMBER`: realizar uma consulta numérica;
- `RULE`: propor uma regra numérica e seus parâmetros.

### Dependências do ambiente original

O arquivo `player.py` não é uma aplicação independente.

Ele foi desenvolvido para funcionar integrado ao ambiente fornecido pela disciplina, composto pelos arquivos:

- `game.py`: implementação das regras e da interface do jogo;
- `tournament.py`: execução de partidas automatizadas e avaliação de desempenho.

Esses arquivos não estão incluídos neste repositório, que contém somente a implementação desenvolvida para o desafio.

Portanto, a execução completa depende do ambiente original da disciplina ou de uma implementação compatível com a interface esperada.

## Desenvolvimento e avaliação

O projeto foi desenvolvido em dupla, envolvendo: planejamento de estratégias para identificar diferentes regras numéricas; implementação das funções em Python; utilização das respostas anteriores para orientar as próximas consultas; identificação e correção de problemas durante o desenvolvimento, e; avaliação do desempenho por meio de testes automatizados pela disciplina. 

A avaliação considerava a taxa de sucesso na identificação das regras, o número de tentativas por partida e a qualidade da implementação.

## Autores

Projeto desenvolvido em dupla por:

- Pedro Gouveia (https://github.com/o-pedrogouveia)
- Rodrigo Couto (https://github.com/rodrigor-couto)

Desenvolvido no primeiro semestre de 2026, na disciplina de MC102 da Unicamp.
