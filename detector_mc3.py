import json
import ast
import re
import csv
from typing import Any, Dict, List, Optional, Tuple
from VisitorMC3 import VisitorMC3

# --- Constantes do Professor ---
C4_MAX_ALLOWED_RANGEITER = 50
E2_MAX_ALLOWED_LISTS = 5
G4_MIN_VAR_CHRS = 4
G4_MIN_FNC_CHRS = 8
G4_MAX_ALLOWED_NONSIGNIFICANT = 70

def consertar_codigo(codigo_sujo: str) -> str:
    """Transforma blocos de espaços em quebras de linha para evitar SyntaxError."""
    return re.sub(r' {3,}', '\n', codigo_sujo)

def analisar_snippet_python(codigo_do_aluno: str, ranking_erros: Dict[str, int]) -> Optional[List[str]]:
    """Analisa um código e alimenta o ranking de erros em caso de detecção."""
    if not isinstance(codigo_do_aluno, str):
        return None

    codigo_formatado = consertar_codigo(codigo_do_aluno)

    try:
        parsed = ast.parse(codigo_formatado)
    except (SyntaxError, ValueError):
        # Captura apenas erros de código inválido, ignorando textos puros
        return None 

    visitor = VisitorMC3()
    resultados = {}
    
    try:
        resultados['A4'] = visitor.getA4(parsed)[0] 
        resultados['B6'] = visitor.getB6(parsed)
        resultados['B8'] = visitor.getB8(parsed)
        resultados['B9'] = visitor.getB9(parsed)
        resultados['B12'] = visitor.getB12(parsed)
        resultados['C1'] = visitor.getC1(parsed)
        resultados['C2'] = visitor.getC2(parsed)
        resultados['C4'] = visitor.getC4(parsed, C4_MAX_ALLOWED_RANGEITER)
        resultados['C8'] = visitor.getC8(parsed)
        resultados['D4'] = visitor.getD4(parsed)
        resultados['E2'] = visitor.getE2(parsed, E2_MAX_ALLOWED_LISTS)
        resultados['G4'] = visitor.getG4(parsed, G4_MIN_VAR_CHRS, G4_MIN_FNC_CHRS, G4_MAX_ALLOWED_NONSIGNIFICANT)
        resultados['G5'] = visitor.getG5(parsed)
        resultados['H1'] = visitor.getH1(parsed)
    except Exception as e:
        print(f"Erro inesperado no VisitorMC3: {e}")
        return None

    erros_encontrados = [mc3_nome for mc3_nome, teve_erro in resultados.items() if teve_erro]
    
    for erro in erros_encontrados:
        ranking_erros[erro] = ranking_erros.get(erro, 0) + 1
        
    return erros_encontrados

def processar_dados_turma(dados: Any) -> Tuple[Dict[str, Dict[str, List[str]]], Dict[str, int]]:
    """Percorre a estrutura JSON, extrai respostas e retorna o relatório e o ranking."""
    relatorio: Dict[str, Dict[str, List[str]]] = {}
    ranking: Dict[str, int] = {}

    def cacador_recursivo(estrutura_atual: Any):
        if isinstance(estrutura_atual, dict):
            p_nome = estrutura_atual.get('nome', '').strip()
            s_nome = estrutura_atual.get('sobrenome', '').strip()
            
            nome_completo = f"{p_nome} {s_nome}".strip() or "Aluno Desconhecido"
                    
            for chave, valor in estrutura_atual.items():
                if chave.lower().startswith('resposta'):
                    resultado = analisar_snippet_python(valor, ranking)
                    
                    if resultado is not None:
                        if nome_completo not in relatorio:
                            relatorio[nome_completo] = {}
                        relatorio[nome_completo][chave] = resultado
                        
        elif isinstance(estrutura_atual, list):
            for item in estrutura_atual:
                cacador_recursivo(item)

    cacador_recursivo(dados)
    return relatorio, ranking

def gerar_relatorios(relatorio_geral: dict, ranking_erros: dict, arq_txt: str, arq_csv: str):
    """Gera os arquivos de saída na formatação adequada."""
    with open(arq_txt, 'w', encoding='utf-8') as f_txt, \
         open(arq_csv, 'w', encoding='utf-8', newline='') as f_csv:
        
        escritor_csv = csv.writer(f_csv, delimiter=';')
        escritor_csv.writerow(['Aluno', 'Questão', 'Status', 'Erros (Siglas)'])
        
        for aluno, respostas in relatorio_geral.items():
            header = f"ESTUDANTE: {aluno}\n{'-'*60}\n"
            f_txt.write(header)
            
            for questao in sorted(respostas.keys()):
                erros = respostas[questao]
                if erros:
                    msg = f"  > {questao}: Erros MC³ detectados -> {', '.join(erros)}\n"
                    escritor_csv.writerow([aluno, questao, 'Com Erros', ', '.join(erros)])
                else:
                    msg = f"  > {questao}: Tudo OK (Nenhum erro conceitual).\n"
                    escritor_csv.writerow([aluno, questao, 'Tudo OK', ''])
                    
                f_txt.write(msg)
                
            f_txt.write("\n")

        # Ranking
        resumo = f"\n{'='*60}\nESTATÍSTICAS DA TURMA (RANKING DE ERROS)\n{'='*60}\n"
        if ranking_erros:
            for erro, quantidade in sorted(ranking_erros.items(), key=lambda x: x[1], reverse=True):
                resumo += f"  - Erro {erro}: cometeu-se {quantidade} vez(es)\n"
        else:
            resumo += "  Parabéns à turma! Nenhum erro conceitual foi detectado.\n"

        f_txt.write(resumo)
        print(f"Arquivos gerados com sucesso: {arq_txt} e {arq_csv}")

def main():
    arquivo_entrada = 'nome_arquivo.json'
    arquivo_saida_txt = 'resultado.txt'
    arquivo_saida_csv = 'planilha_resultado.csv'

    try:
        with open(arquivo_entrada, 'r', encoding='utf-8') as arquivo:
            dados_alunos = json.load(arquivo)
    except FileNotFoundError:
        print(f"ERRO: Não encontrei o arquivo '{arquivo_entrada}'. Verifique o nome da planilha.")
        return # Encerra o programa

    print("Analisando as respostas da turma... Aguarde.")
    relatorio_geral, ranking_erros = processar_dados_turma(dados_alunos)
    
    gerar_relatorios(relatorio_geral, ranking_erros, arquivo_saida_txt, arquivo_saida_csv)

# Garante que o script só rode se for chamado diretamente pelo terminal/IDE
if __name__ == '__main__':
    main()