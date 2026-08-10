"""
Le reports/latest.json e encerra com codigo de saida 1 se houver algum
achado de severidade Critica - util para bloquear merge de PRs com
segredo exposto, por exemplo. Achados Alta/Media/Baixa nao bloqueiam.
"""

import json
import sys

with open("reports/latest.json", encoding="utf-8") as f:
    data = json.load(f)

criticos = [f for f in data["findings"] if f["severity"] == "Critica"]

if criticos:
    print(f"::error::{len(criticos)} achado(s) CRITICO(s) encontrados - veja reports/latest.md")
    for c in criticos:
        print(f" - {c['title']} em {c['location']}")
    sys.exit(1)

print("Nenhum achado critico. OK.")
