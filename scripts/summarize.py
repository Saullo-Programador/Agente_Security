"""
Le findings.json (achados normalizados dos scanners) e:
1. Pede ao Gemini um resumo executivo em portugues, priorizando o que
   importa primeiro.
2. Monta reports/<data>.md, reports/latest.md e reports/latest.json
   (usado pela pagina index.html).
"""

import json
import os
import re
import sys
from datetime import date

import requests

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")
GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest")
GEMINI_URL = (
    f"https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent?key={GEMINI_API_KEY}"
)

INPUT_PATH = "findings.json"
REPO_LABEL = os.environ.get("REPO_LABEL", "este repositorio")
CATEGORY_ORDER = ["Segredo exposto", "Dependencia vulneravel", "Codigo inseguro (SAST)"]

SUMMARY_PROMPT = """Voce e um analista de seguranca (AppSec) experiente.
Abaixo esta uma lista de achados brutos de scanners automaticos (gitleaks,
semgrep, pip-audit, npm audit) rodados neste repositorio.

Escreva um resumo executivo curto em portugues (4 a 6 frases, texto corrido,
sem markdown) para alguem que vai decidir o que corrigir primeiro. Destaque:
quantos achados sao realmente criticos/urgentes, qual categoria concentra
mais risco, e uma recomendacao objetiva do que atacar primeiro. Se a lista
estiver vazia, diga isso claramente e nao invente achados.

Achados (JSON):
{items}
"""


def get_ai_summary(findings):
    if not GEMINI_API_KEY:
        return "Resumo por IA indisponivel (GEMINI_API_KEY nao configurada)."

    if not findings:
        return "Nenhum achado nesta varredura. Nenhuma acao necessaria."

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": SUMMARY_PROMPT.format(
                            items=json.dumps(findings[:40], ensure_ascii=False)
                        )
                    }
                ]
            }
        ],
        "generationConfig": {"temperature": 0.2},
    }

    try:
        resp = requests.post(GEMINI_URL, json=payload, timeout=60)
        resp.raise_for_status()
        text = resp.json()["candidates"][0]["content"]["parts"][0]["text"]
        return re.sub(r"^```|```$", "", text.strip(), flags=re.MULTILINE).strip()
    except Exception as exc:  # nao deixa a falta de IA quebrar o relatorio
        print(f"[aviso] resumo por IA falhou: {exc}", file=sys.stderr)
        return "Resumo por IA indisponivel nesta execucao (falha na chamada da API)."


def build():
    with open(INPUT_PATH, encoding="utf-8") as f:
        findings = json.load(f)

    today = date.today().isoformat()
    ai_summary = get_ai_summary(findings)

    by_category = {}
    for item in findings:
        by_category.setdefault(item["category"], []).append(item)

    lines = [f"# Radar de Seguranca - {today}", "", f"Repositorio escaneado: `{REPO_LABEL}`", "", "## Resumo", "", ai_summary, ""]

    if not findings:
        lines.append("_Nenhum achado nesta varredura._")
    else:
        for category in CATEGORY_ORDER:
            entries = by_category.get(category)
            if not entries:
                continue
            lines.append(f"## {category} ({len(entries)})")
            lines.append("")
            for item in entries:
                lines.append(
                    f"- **[{item['severity']}]** {item['title']} — `{item['location']}`  \n"
                    f"  {item['detail']}"
                )
            lines.append("")

    lines.append("---")
    lines.append("_Gerado automaticamente por radar-seguranca._")

    os.makedirs("reports", exist_ok=True)
    report_text = "\n".join(lines)

    with open(f"reports/{today}.md", "w", encoding="utf-8") as f:
        f.write(report_text)
    with open("reports/latest.md", "w", encoding="utf-8") as f:
        f.write(report_text)
    with open("reports/latest.json", "w", encoding="utf-8") as f:
        json.dump(
            {"date": today, "repo": REPO_LABEL, "summary": ai_summary, "findings": findings},
            f,
            ensure_ascii=False,
            indent=2,
        )

    print(f"Relatorio gerado: reports/{today}.md ({len(findings)} achados)")


if __name__ == "__main__":
    build()
