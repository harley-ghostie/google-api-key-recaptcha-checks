# Google API Key & reCAPTCHA Validation Tools

![Status](https://img.shields.io/badge/STATUS-EM%20DESENVOLVIMENTO-brightgreen?style=for-the-badge)

Repositório com scripts para validação de exposição de chaves da API do Google e análise básica de restrição de domínio em chaves públicas do Google reCAPTCHA.

A proposta é apoiar análises autorizadas de segurança em aplicações web, principalmente em cenários de pentest, revisão de exposição de credenciais públicas e validação de configuração de chaves utilizadas no front-end.

> [!NOTE]
> Projeto em desenvolvimento.
>
> Este repositório reúne scripts de apoio para validação técnica e triagem de segurança. Os scripts podem passar por ajustes, refatoração e melhorias de precisão conforme novos cenários forem testados.

---

## Scripts disponíveis

| Script | Objetivo | Quando usar |
|---|---|---|
| `Validate_Recaptcha_Key.py` | Valida se uma site key do Google reCAPTCHA aparenta estar restrita ao domínio esperado. | Usar quando uma chave pública de reCAPTCHA for encontrada no front-end e for necessário verificar se há indício de ausência de restrição por domínio. |
| `verificar_chaves_api.py` | Busca chaves da API do Google em páginas web a partir de uma lista de URLs. | Usar durante análise de exposição de credenciais públicas em HTML, JavaScript ou páginas acessíveis sem autenticação. |

---

## Visão geral

Este repositório possui dois scripts com finalidades complementares.

O `Validate_Recaptcha_Key.py` é voltado para **validação de configuração de site keys do Google reCAPTCHA**, verificando se uma chave pública aparenta funcionar em um domínio de teste.

O `verificar_chaves_api.py` é voltado para **identificação de chaves da API do Google expostas em páginas web**, procurando padrões iniciados por `AIza`, normalmente associados a Google API Keys.

---

## 1. Validate_Recaptcha_Key.py

### Descrição

O `Validate_Recaptcha_Key.py` realiza uma validação simples para verificar se uma site key do Google reCAPTCHA aparenta estar restrita a domínios específicos.

O script envia uma requisição para o endpoint público do reCAPTCHA usando a chave informada e um domínio de teste no header `Referer`. A partir da resposta, ele tenta identificar se a chave funciona fora do domínio esperado ou se há indício de restrição.

---

### O que o script faz

O script executa as seguintes ações:

- recebe uma site key do Google reCAPTCHA configurada manualmente no código;
- define um domínio de teste para simular a origem da requisição;
- envia uma requisição HTTP para o endpoint público do reCAPTCHA;
- verifica se a resposta indica erro ou funcionamento;
- informa se a chave aparenta estar restrita ou não ao domínio.

---

### Quando usar

Use este script quando uma site key do reCAPTCHA for encontrada em uma aplicação web e houver necessidade de validar se ela está corretamente limitada ao domínio autorizado.

Cenários indicados:

```text
Busca por Google API Keys expostas
Análise de HTML público
Análise de arquivos JavaScript públicos
Validação de vazamento de chave em front-end
Triagem de aplicações web
Revisão de segurança em páginas públicas
Análise de URLs coletadas por crawler ou recon
```
---

### Campos que devem ser alterados

Antes de executar, altere a site key que será testada:

```python
test_site_key = "SITE_KEY_AQUI"
```

Exemplo genérico:

```python
test_site_key = "6LcXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
```

Altere também o domínio de teste:

```python
test_domain = "https://dominio-teste.com.br"
```

Esse domínio deve ser autorizado para o teste e, preferencialmente, controlado pela equipe responsável pela validação.

---

Exemplo:

```python
"co": "exemplo.com.br"
```

Na prática, os principais pontos de ajuste são:

```python
test_site_key = "SITE_KEY_AQUI"
test_domain = "https://exemplo.com.br"
"co": "exemplo.com.br"
```

---

### Exemplo de execução

```bash
python3 Validate_Recaptcha_Key.py
```

---

### Saída esperada

Caso a chave aparente funcionar no domínio de teste:

```text
The site key works on the test domain https://exemplo.com.br. It may not be restricted.
The site key is not properly restricted to specific domains.
```

Caso a chave aparente estar restrita:

```text
The site key does not work on the test domain https://exemplo.com.br. It may be restricted.
The site key appears to be properly restricted to specific domains.
```

---

### Interpretação dos resultados

Se a chave funcionar em um domínio não autorizado, isso pode indicar ausência de restrição adequada por domínio.

Esse comportamento não significa, sozinho, comprometimento da aplicação, mas pode permitir uso indevido da site key em outros sites, abuso de quota, aumento de custo operacional ou redução da confiabilidade do controle anti-automação.

A validação ideal deve ser complementada com revisão direta no painel do Google reCAPTCHA/Admin Console, verificando os domínios autorizados para a chave.

---

## 2. verificar_chaves_api.py

### Descrição

O `verificar_chaves_api.py` analisa uma lista de URLs em busca de possíveis chaves da API do Google expostas no conteúdo das páginas.

O script procura por padrões compatíveis com Google API Keys, normalmente iniciadas por:

```text
AIza
```

Ele acessa cada URL informada no arquivo `urls.txt`, coleta o conteúdo HTML retornado e aplica uma expressão regular para identificar possíveis chaves expostas.

---
### Arquivo de entrada

O script espera um arquivo chamado:

```text
urls.txt
```

Esse arquivo deve conter uma URL por linha.

Exemplo:

```text
https://exemplo.com.br/
https://exemplo.com.br/app.js
https://exemplo.com.br/static/main.js
https://exemplo.com.br/login
```

---

### Campo que deve ser alterado

Caso queira usar outro arquivo de entrada, altere a variável:

```python
urls_file = "urls.txt"
```

Exemplo:

```python
urls_file = "meus_alvos.txt"
```

---

### Regex utilizada

O script procura chaves no seguinte padrão:

```python
api_key_pattern = r'AIza[0-9A-Za-z-_]{35}'
```

Esse padrão identifica possíveis Google API Keys expostas no conteúdo retornado pelas URLs.

---

### Exemplo de execução

```bash
python3 verificar_chaves_api.py
```

---

### Exemplo de saída

```text
Verificando URL: https://exemplo.com.br/...
Chaves de API encontradas: ['AIzaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

Resumo das verificações:
URL: https://exemplo.com.br/ - Chaves encontradas: ['AIzaXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX']

Deseja salvar os resultados em um arquivo JSON? (s/n):
```

Caso opte por salvar, o resultado será gravado em:

```text
resultado_chaves_api.json
```

---

## Fluxo recomendado de uso

A ordem recomendada é:

```text
1. Coletar URLs públicas da aplicação
   ↓
2. Inserir as URLs no arquivo urls.txt
   ↓
3. Executar verificar_chaves_api.py
   ↓
4. Identificar possíveis Google API Keys expostas
   ↓
5. Validar manualmente o tipo da chave e suas restrições
   ↓
6. Caso a chave seja de reCAPTCHA, usar Validate_Recaptcha_Key.py
   ↓
7. Confirmar se há restrição adequada por domínio
```

---

### Dependências Python

Os scripts utilizam a biblioteca `requests`.

Instalação:

```bash
python3 -m pip install requests
```

---

## Limitações

O `verificar_chaves_api.py` identifica possíveis chaves com base em regex. Isso pode gerar falso positivo ou não identificar chaves ofuscadas, carregadas dinamicamente, retornadas após autenticação ou inseridas por JavaScript executado no navegador.

O `Validate_Recaptcha_Key.py` realiza uma validação simples baseada na resposta do endpoint público do reCAPTCHA. O resultado deve ser tratado como indício e não como confirmação absoluta. A confirmação deve ser feita no painel administrativo do Google, revisando as restrições configuradas para a chave.

---

## Aviso legal ⚠️

Estes scripts devem ser utilizados apenas em ambientes autorizados.

A finalidade é apoiar validações técnicas, pentests autorizados, análise defensiva, revisão de exposição de chaves e validação de restrições de domínio.

O uso contra sistemas sem autorização é proibido.
