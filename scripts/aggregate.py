"""
Le gitleaks-report.json, semgrep-report.json e trivy-report.json (os que
existirem) e escreve findings.json com uma lista normalizada de achados,
prontos para a etapa de resumo por IA.

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


TRIVY_SEVERITY_MAP = {
    "CRITICAL": "Critica",
    "HIGH": "Alta",
    "MEDIUM": "Media",
    "LOW": "Baixa",
    "UNKNOWN": "Baixa",
}


def parse_trivy():
    data = safe_load("trivy-report.json")
    if not data:
        return []
    findings = []
    for result in data.get("Results", []) or []:
        target = result.get("Target", "?")
        for vuln in result.get("Vulnerabilities", []) or []:
            fixed = vuln.get("FixedVersion") or "sem correcao publicada"
            texto = (vuln.get("Title") or vuln.get("Description") or "")[:300]
            findings.append(
                {
                    "tool": "trivy",
                    "category": "Dependencia vulneravel",
                    "severity": TRIVY_SEVERITY_MAP.get(vuln.get("Severity", "UNKNOWN"), "Baixa"),
                    "title": f"{vuln.get('PkgName')} {vuln.get('InstalledVersion')} - {vuln.get('VulnerabilityID')}",
                    "location": target,
                    "detail": f"{texto} Correcao: {fixed}",
                }
            )
    return findings


def aggregate():
    findings = parse_gitleaks() + parse_semgrep() + parse_trivy()
    findings.sort(key=lambda f: SEVERITY_RANK.get(f["severity"], 0), reverse=True)

    with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
        json.dump(findings, f, ensure_ascii=False, indent=2)

    print(f"{len(findings)} achados agregados -> {OUTPUT_PATH}")


if __name__ == "__main__":
    aggregate()
