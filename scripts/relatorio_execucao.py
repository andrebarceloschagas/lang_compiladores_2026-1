"""Gera relatório de execução para um exemplo MiniLang.

Este script executa o analisador léxico, o analisador sintático e o transpilador
para um arquivo .minilang e grava um relatório Markdown com os comandos, saídas,
arquivos gerados e eventuais erros.
"""

import argparse
import os
import subprocess
import sys


def run_command(cmd, cwd=None):
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    return {
        "cmd": " ".join(proc.args) if isinstance(proc.args, list) else proc.args,
        "returncode": proc.returncode,
        "stdout": proc.stdout.strip(),
        "stderr": proc.stderr.strip(),
    }


def main():
    parser = argparse.ArgumentParser(description="Gera relatório de execução de exemplo MiniLang")
    parser.add_argument("input", help="Arquivo .minilang de entrada")
    parser.add_argument("--report", default="relatorio_execucao.md", help="Arquivo de relatório Markdown de saída")
    parser.add_argument("--save-tokens", default=None, help="Arquivo para salvar tokens")
    parser.add_argument("--save-ast", default=None, help="Arquivo para salvar a AST")
    args = parser.parse_args()

    projeto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    exemplo = os.path.abspath(args.input)
    report_path = os.path.abspath(args.report)
    save_tokens = args.save_tokens or os.path.join(projeto_root, "saida_tokens.txt")
    save_ast = args.save_ast or os.path.join(projeto_root, "saida_ast.txt")

    commands = []

    if save_tokens:
        commands.append({
            "label": "Lexer",
            "args": [sys.executable, "src/lexer/main_lexer.py", exemplo, "--salvar", save_tokens],
        })

    report_py = os.path.splitext(exemplo)[0] + ".py"
    commands.append({
        "label": "Compilador completo",
        "args": [sys.executable, "src/compiler/main_compiler.py", exemplo, "--py", report_py] + (["--tokens", save_tokens] if save_tokens else []) + (["--ast", save_ast] if save_ast else []),
    })

    outputs = []

    for item in commands:
        result = run_command(item["args"], cwd=projeto_root)
        outputs.append({
            "label": item["label"],
            "cmd": result["cmd"],
            "returncode": result["returncode"],
            "stdout": result["stdout"],
            "stderr": result["stderr"],
        })

    generated_py = report_py

    report_lines = [
        f"# Relatório de execução: {os.path.basename(exemplo)}",
        "",
        "## Entrada",
        f"- Arquivo MiniLang: `{exemplo}`",
        f"- Diretório do projeto: `{projeto_root}`",
        "",
        "## Comandos executados",
    ]

    for item in outputs:
        status = "✅ Sucesso" if item["returncode"] == 0 else "❌ Falha"
        report_lines.append(f"### {item['label']}")
        report_lines.append(f"- Comando: `{item['cmd']}`")
        report_lines.append(f"- Status: {status} (exit code {item['returncode']})")
        if item["stdout"]:
            report_lines.append("- Saída padrão:")
            report_lines.append("```\n" + item["stdout"] + "\n```")
        if item["stderr"]:
            report_lines.append("- Erro padrão:")
            report_lines.append("```\n" + item["stderr"] + "\n```")
        report_lines.append("")

    report_lines.extend([
        "## Arquivos gerados",
        f"- Tokens salvos em: `{save_tokens}`",
        f"- AST salva em: `{save_ast}`",
        f"- Código Python gerado em: `{generated_py}`",
        "",
    ])

    if os.path.exists(save_tokens):
        with open(save_tokens, encoding="utf-8") as f:
            tokens_preview = "\n".join(f.read().splitlines()[:30])
        report_lines.append("## Amostra de tokens gerados")
        report_lines.append("```\n" + tokens_preview + "\n```")
        report_lines.append("")

    if os.path.exists(save_ast):
        with open(save_ast, encoding="utf-8") as f:
            ast_preview = "\n".join(f.read().splitlines()[:60])
        report_lines.append("## Amostra de AST gerada")
        report_lines.append("```\n" + ast_preview + "\n```")
        report_lines.append("")

    if os.path.exists(generated_py):
        with open(generated_py, encoding="utf-8") as f:
            py_content = f.read()
        report_lines.append("## Código Python transpilado")
        report_lines.append("```python\n" + py_content + "\n```")
        report_lines.append("")

    with open(report_path, "w", encoding="utf-8") as f:
        f.write("\n".join(report_lines))

    print(f"Relatório gerado em: {report_path}")


if __name__ == "__main__":
    main()
