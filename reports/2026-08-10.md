# Radar de Seguranca - 2026-08-10

Repositorio escaneado: `https://github.com/Saullo-Programador/PontoJa.git`

## Resumo

A análise de segurança automatizada identificou um total de seis achados neste repositório, todos classificados como críticos e urgentes. A categoria que concentra 100% do risco é a de segredos expostos, especificamente chaves de API do Google Cloud Platform (GCP) vazadas em arquivos de configuração e código-fonte, como o google-services.json e o firebase_options.dart. Embora chaves do Firebase em clientes mobile possuam restrições naturais, a exposição pública dessas credenciais pode levar ao uso não autorizado de serviços e potenciais violações de dados. Como recomendação objetiva, a equipe deve priorizar imediatamente a remoção e rotação dessas chaves, além de implementar restrições de escopo e IP no console do GCP.

## Segredo exposto (6)

- **[Critica]** Possivel segredo (gcp-api-key) — `android/app/google-services.json:18`  
  Uncovered a GCP API key, which could lead to unauthorized access to Google Cloud services and data breaches.
- **[Critica]** Possivel segredo (gcp-api-key) — `lib/firebase_options.dart:34`  
  Uncovered a GCP API key, which could lead to unauthorized access to Google Cloud services and data breaches.
- **[Critica]** Possivel segredo (gcp-api-key) — `lib/firebase_options.dart:44`  
  Uncovered a GCP API key, which could lead to unauthorized access to Google Cloud services and data breaches.
- **[Critica]** Possivel segredo (gcp-api-key) — `lib/firebase_options.dart:52`  
  Uncovered a GCP API key, which could lead to unauthorized access to Google Cloud services and data breaches.
- **[Critica]** Possivel segredo (gcp-api-key) — `lib/firebase_options.dart:61`  
  Uncovered a GCP API key, which could lead to unauthorized access to Google Cloud services and data breaches.
- **[Critica]** Possivel segredo (gcp-api-key) — `lib/firebase_options.dart:70`  
  Uncovered a GCP API key, which could lead to unauthorized access to Google Cloud services and data breaches.

---
_Gerado automaticamente por radar-seguranca._