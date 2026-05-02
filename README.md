# Detector de Erros Conceituais (MC4)

## Objetivo
Este projeto foi desenvolvido para apoiar as atividades práticas e de monitoria da disciplina de Introdução à Programação. Ele atua como um **MC4** (Verificador de Erros Conceituais), uma ferramenta automatizada projetada para identificar **MC3** (*Misconceptions in Correct Code* - Erros Conceituais em Códigos Corretos) nas respostas enviadas pelos alunos via Moodle.

A ideia principal é detectar falhas de compreensão lógica ou estrutural em códigos que, apesar de compilarem e funcionarem sem erros de sintaxe, demonstram que o aluno não absorveu o conceito ideal da linguagem.

## Estrutura e Dependências
O motor de detecção utiliza a classe `VisitorMC3`, extraída e adaptada do repositório original: https://github.com/eryckpedro/mc4. 

O nosso script principal (`detector_mc3.py`) importa essa classe para varrer um arquivo JSON contendo as respostas da turma, gerando relatórios de desempenho e um ranking dos erros mais comuns.

## Como Executar
1. Certifique-se de que a planilha com as respostas dos alunos (em formato `.json`) está na mesma pasta do script.
2. Altere o nome da variável `arquivo_entrada` pelo nome original do arquivo com as respostas, mantendo o `.json` no final.
3. Execute o arquivo principal via terminal:
```bash
python detector_mc3.py 
```
4. O sistema irá gerar dois arquivos de saída: um relatório textual detalhado (resultado.txt) e uma planilha consolidada (planilha_resultado.csv).