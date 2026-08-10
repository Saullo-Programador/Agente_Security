"""
Le gitleaks-report.json, semgrep-report.json, pip-audit-report.json e/ou
npm-audit-report.json (os que existirem) e escreve findings.json com uma
lista normalizada de achados, prontos para a etapa de resumo por IA.

Importante: nunca inclui o valor do segredo em si (campo Secret/Match do
gitleaks) no output - so o local (arquivo/linha) e a regra que bateu.
"""

import json
import os

OUTPUT_PATH = "findings.json"

SEVERITY_RANK = {"Critica": 3, "Alta": 2, "Media": 1, "Baixa": 0}


def safe_load(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, encoding="utf-8") as f:
            content = f.read().strip()
            return json.loads(content) if content else None
    except (json.JSONDecodeError, OSError):
        return None


def parse_gitleaks():
    data = safe_load("gitleaks-report.json")
    if not data:
        return []
    findings = []
    for leak in data:
        findings.append(
            {
                "tool": "gitleaks",
                "category": "Segredo exposto",
                "severity": "Critica",
                "title": f"Possivel segredo ({leak.get('RuleID', 'regra desconhecida')})",
                "location": f"{leak.get('File', '?')}:{leak.get('StartLine', '?')}",
                "detail": leak.get("Description", ""),
            }
        )
    return findings


SEMGREP_SEVERITY_MAP = {"ERROR": "Alta", "WARNING": "Media", "INFO": "Baixa"}


def parse_semgrep():
    data = safe_load("semgrep-report.json")
    if not data:
        return []
    findings = []
    for result in data.get("results", []):
        raw_sev = result.get("extra", {}).get("severity", "INFO")
        findings.append(
            {
                "tool": "semgrep",
                "category": "Codigo inseguro (SAST)",
                "severity": SEMGREP_SEVERITY_MAP.get(raw_sev, "Baixa"),
                "title": result.get("check_id", "regra semgrep"),
                "location": f"{result.get('path', '?')}:{result.get('start', {}).get('line', '?')}",
                "detail": result.get("extra", {}).get("message", ""),
            }
        )
    return findings


def parse_pip_audit():
    data = safe_load("pip-audit-report.json")
    if not data:
        return []
    deps = data if isinstance(data, list) else data.get("dependencies", [])
    findings = []
    for dep in deps:
        for vuln in dep.get("vulns", []):
            fixes = ", ".join(vuln.get("fix_versions", []) or []) or "sem correcao publicada"
            findings.append(
                {
                    "tool": "pip-audit",
                    "category": "Dependencia vulneravel",
                    "severity": "Alta",
                    "title": f"{dep.get('name')} {dep.get('version')} - {vuln.get('id')}",
                    "location": "requirements.txt",
                    "detail": f"{vuln.get('description', '')} Correcao: {fixes}",
                }
            )
    return findings


NPM_SEVERITY_MAP = {
    "critical": "Critica",
    "high": "Alta",
    "moderate": "Media",
    "low": "Baixa",
    "info": "Baixa",
}


def parse_npm_audit():
    data = safe_load("npm-audit-report.json")
    if not data:
        return []
    vulns = data.get("vulnerabilities", {})
    findings = []
    for name, info in vulns.items():
        findings.append(
            {
                "tool": "npm-audit",
                "category": "Dependencia vulneravel",
                "severity": NPM_SEVERITY_MAP.get(info.get("severity", "low"), "Baixa"),
                "title": f"{name} - {info.get('severity', 'desconhecida')}",
                "location": "package.json",
                "detail": f"Faixa afetada: {info.get('range', '?')}. "
                f"Correcao disponivel: {'sim' if info.get('fixAvailable') else 'nao'}",
            }
        )
    return findings


def aggregate():
    findings = (
        parse_gitleaks() + parse_semgrep() + parse_pip_audit() + parse_npm_audit()
    )
    findings.sort(key=lambda f: SEVERITY_RANK.get(f["severity"], 0), reverse=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)

    print(f"{len(findings)} achados agregados -> {OUTPUT_PATH}")


if __name__ == "__main__":
    aggregate()
