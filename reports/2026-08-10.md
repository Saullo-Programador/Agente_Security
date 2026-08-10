# Radar de Seguranca - 2026-08-10

Repositorio escaneado: `Saullo-Programador/Agente_Security`

## Resumo

A análise automatizada de segurança identificou um total de três achados, todos classificados como de severidade alta e concentrados na categoria de dependências vulneráveis em Python. Não há ocorrências críticas ou urgentes no momento, mas os riscos identificados envolvem potenciais vazamentos de credenciais e negação de serviço através do arquivo requirements.txt. O maior risco reside na biblioteca requests, que apresenta vulnerabilidades que podem expor dados sensíveis ou permitir ataques locais caso funções específicas sejam acionadas. Como recomendação objetiva, a prioridade imediata deve ser a atualização das bibliotecas requests e protobuf para as versões corrigidas indicadas nos relatórios para eliminar a exposição conhecida.

## Dependencia vulneravel (3)

- **[Alta]** requests 2.32.3 - PYSEC-2026-1872 — `requirements.txt`  
  ### Impact  Due to a URL parsing issue, Requests releases prior to 2.32.4 may leak .netrc credentials to third parties for specific maliciously-crafted URLs.  ### Workarounds For older versions of Requests, use of the .netrc file can be disabled with `trust_env=False` on your Requests Session ([docs](https://requests.readthedocs.io/en/latest/api/#requests.Session.trust_env)).  ### References https://github.com/psf/requests/pull/6965 https://seclists.org/fulldisclosure/2025/Jun/2 Correcao: 2.32.4
- **[Alta]** requests 2.32.3 - PYSEC-2026-2275 — `requirements.txt`  
  Requests is a HTTP library. Prior to version 2.33.0, the `requests.utils.extract_zipped_paths()` utility function uses a predictable filename when extracting files from zip archives into the system temporary directory. If the target file already exists, it is reused without validation. A local attacker with write access to the temp directory could pre-create a malicious file that would be loaded in place of the legitimate one. Standard usage of the Requests library is not affected by this vulnerability. Only applications that call `extract_zipped_paths()` directly are impacted. Starting in version 2.33.0, the library extracts files to a non-deterministic location. If developers are unable to upgrade, they can set `TMPDIR` in their environment to a directory with restricted write access. Correcao: 2.33.0
- **[Alta]** protobuf 4.25.9 - PYSEC-2026-1805 — `requirements.txt`  
  A denial-of-service (DoS) vulnerability exists in google.protobuf.json_format.ParseDict() in Python, where the max_recursion_depth limit can be bypassed when parsing nested google.protobuf.Any messages.  Due to missing recursion depth accounting inside the internal Any-handling logic, an attacker can supply deeply nested Any structures that bypass the intended recursion limit, eventually exhausting Python’s recursion stack and causing a RecursionError. Correcao: 5.29.6, 6.33.5

---
_Gerado automaticamente por radar-seguranca._