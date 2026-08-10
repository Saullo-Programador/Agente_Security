# radar-seguranca 🛡️📡

Agente que audita a segurança de um repositório automaticamente, a cada
`push`, `pull request` e semanalmente — sem precisar de servidor, tudo
gratuito, via GitHub Actions.

Combina três scanners open-source consagrados e usa IA só para **priorizar
e traduzir** os achados, não para "hackear" nada:

| Scanner | O que detecta |
|---|---|
| [gitleaks](https://github.com/gitleaks/gitleaks) | Segredos vazados no histórico do git (chaves de API, senhas, tokens) |
| [semgrep](https://semgrep.dev) | Padrões de código inseguro (SQL injection, XSS, etc.) — SAST |
| [pip-audit](https://github.com/pypa/pip-audit) / `npm audit` | Dependências com CVE conhecida |

O resultado é commitado em `reports/` e publicado numa página simples via
GitHub Pages, sempre mostrando a **última varredura**.

## ⚠️ Uso responsável

Esta ferramenta faz **análise estática e passiva** — ela lê código e
histórico de commits, nunca tenta explorar, invadir ou atacar nada. Rode
apenas em repositórios que você tem permissão de auditar (os seus, ou de
terceiros com autorização explícita). Testes de invasão ativa em sistemas
sem autorização são crime no Brasil (Lei 12.737/2012).

Se for rodar isto em um repositório privado com credenciais de cliente,
**mantenha o repositório privado** — o relatório commitado pode expor nomes
de arquivo e linha (nunca o segredo em si, que é sempre redigido).

## Auditando outro repositório (via link)

Além de escanear a si mesmo, este agente pode auditar **qualquer repositório público do GitHub** que você informar:

1. Vá em **Actions → Radar de Seguranca → Run workflow**.
2. No campo **repo_url**, cole o link do repositório (ex: `https://github.com/usuario/projeto`).
3. Rode. O relatório (`reports/latest.md` / `latest.json` / página) mostra qual repositório foi escaneado.

Deixando o campo vazio, ele volta a escanear este próprio repositório (comportamento padrão nos gatilhos automáticos de `push`, `pull request` e agendamento semanal).

**Limitação:** só funciona com repositórios **públicos** — não há autenticação configurada para clonar repositórios privados de terceiros.

## Como usar em qualquer repositório seu

1. Copie estas pastas/arquivos para o repositório que você quer auditar:
   ```
   .github/workflows/security-scan.yml
   scripts/
   requirements.txt
   ```
2. Adicione o secret `GEMINI_API_KEY` em **Settings → Secrets and
   variables → Actions** (chave grátis em [aistudio.google.com/apikey](https://aistudio.google.com/apikey)).
3. Rode manualmente pela aba **Actions → Radar de Seguranca → Run workflow**,
   ou espere o próximo push/PR/segunda-feira.

Sem a `GEMINI_API_KEY`, o agente ainda funciona — só o resumo executivo em
português fica desativado, a lista de achados continua completa.

## Testando este próprio repositório (para recrutadores)

Este repositório já roda o scan em si mesmo. Veja a aba **Actions** para o
histórico de execuções, ou a pasta **[reports/](./reports)** para os
relatórios. Ative o **GitHub Pages** (Settings → Pages → Deploy from a
branch → `main` / `(root)`) para ver a versão navegável.

## Bloqueio automático (gate)

`scripts/gate.py` faz o job falhar se algum achado de severidade
**Crítica** (segredo exposto) for encontrado — útil para bloquear o merge
de um Pull Request antes que um segredo vaze para a branch principal.
Achados Alta/Média/Baixa não bloqueiam, só ficam no relatório.

## Estrutura

```
scripts/
  aggregate.py    # normaliza a saida dos 3 scanners num formato unico
  summarize.py    # IA prioriza/traduz + monta o relatorio (md e json)
  gate.py         # falha o job se houver achado critico
.github/workflows/
  security-scan.yml
reports/
  AAAA-MM-DD.md
  latest.md / latest.json
index.html        # pagina do GitHub Pages
```

## Licença

MIT.
#
