# Radar de Seguranca - 2026-08-10

Repositorio escaneado: `Saullo-Programador/Agente_Security`

## Resumo

O escaneamento de segurança identificou um total de três achados, todos classificados como de severidade alta e sem ocorrências críticas imediatas. A categoria que concentra todo o risco atual é a de dependências vulneráveis, originadas no arquivo requirements.txt do projeto. Os problemas envolvem falhas conhecidas nas bibliotecas requests e protobuf, afetando a integridade e a estabilidade da aplicação. Recomendo atacar primeiro a atualização da biblioteca requests para a versão 2.33.0 ou superior, o que resolve os dois primeiros alertas de uma só vez. Em seguida, proceda com a atualização do pacote protobuf para mitigar o risco de negação de serviço.

## Dependencia vulneravel (3)

- **[Alta]** requests 2.32.3 - PYSEC-2026-1872 — `requirements.txt`  
  ### Impact  Due to a URL parsing issue, Requests releases prior to 2.32.4 may leak .netrc credentials to third parties for specific maliciously-crafted URLs.  ### Workarounds For older versions of Requests, use of the .netrc file can be disabled with `trust_env=False` on your Requests Session ([docs](https://requests.readthedocs.io/en/latest/api/#requests.Session.trust_env)).  ### References https://github.com/psf/requests/pull/6965 https://seclists.org/fulldisclosure/2025/Jun/2 Correcao: 2.32.4
- **[Alta]** requests 2.32.3 - PYSEC-2026-2275 — `requirements.txt`  
  Requests is a HTTP library. Prior to version 2.33.0, the `requests.utils.extract_zipped_paths()` utility function uses a predictable filename when extracting files from zip archives into the system temporary directory. If the target file already exists, it is reused without validation. A local attacker with write access to the temp directory could pre-create a malicious file that would be loaded in place of the legitimate one. Standard usage of the Requests library is not affected by this vulnerability. Only applications that call `extract_zipped_paths()` directly are impacted. Starting in version 2.33.0, the library extracts files to a non-deterministic location. If developers are unable to upgrade, they can set `TMPDIR` in their environment to a directory with restricted write access. Correcao: 2.33.0
- **[Alta]** protobuf 4.25.9 - PYSEC-2026-1805 — `requirements.txt`  
  A denial-of-service (DoS) vulnerability exists in google.protobuf.json_format.ParseDict() in Python, where the max_recursion_depth limit can be bypassed when parsing nested google.protobuf.Any messages.  Due to missing recursion depth accounting inside the internal Any-handling logic, an attacker can supply deeply nested Any structures that bypass the intended recursion limit, eventually exhausting Python’s recursion stack and causing a RecursionError. Correcao: 5.29.6, 6.33.5

---
_Gerado automaticamente por radar-seguranca._