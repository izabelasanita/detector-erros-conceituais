# Detector de Erros Conceituais (MC3)

## Objetivo
Este projeto foi desenvolvido para apoiar as atividades práticas e de monitoria da disciplina de Introdução à Programação. Ele atua como um verificador de erros conceituais, uma ferramenta automatizada projetada para identificar **MC3** (*Misconceptions in Correct Code* - Erros Conceituais em Códigos Corretos) nas respostas enviadas pelos alunos via Moodle.

A ideia principal é detectar falhas de compreensão lógica ou estrutural em códigos que, apesar de compilarem e funcionarem sem erros de sintaxe, demonstram que o aluno não absorveu o conceito ideal da linguagem. Nossa versão conta com uma inteligência que quantifica a frequência desses erros dentro de um mesmo código, fornecendo métricas exatas de quantas vezes a infração ocorreu.

## Estrutura
O motor de detecção utiliza a classe `VisitorMC3`, extraída e adaptada do repositório original: https://github.com/eryckpedro/mc4. 

O nosso script principal (`detector_mc3.py`) importa essa classe para varrer um  JSON contendo as respostas da turma, gerando relatórios de desempenho e um ranking dos erros mais comuns. O projeto também utiliza a biblioteca `pyspellchecker` para validar nomenclaturas e evitar penalizar os alunos por usarem palavras reais curtas ou constantes válidas.

## Instalação e Dependências
Antes de executar a ferramenta, você precisa instalar a biblioteca de correção ortográfica que alimenta a nossa validação de variáveis. No terminal, execute:
```bash
pip install pyspellchecker
```
## Como Executar
1. Certifique-se de que o arquivo com as respostas dos alunos (em formato `.json`) está na mesma pasta do script.
2. No arquivo principal `detector_mc3.py`, altere o nome da variável `arquivo_entrada` pelo nome original do arquivo com as respostas, mantendo o `.json` no final.
3. Execute o arquivo principal via terminal:
```bash
python detector_mc3.py 
```
4. O sistema irá gerar dois arquivos de saída: um relatório textual detalhado (resultado.txt) e uma planilha consolidada (planilha_resultado.csv).