# PensionistaAgent

Agente de IA especializado no atendimento a **aposentados e pensionistas**, com sistema modular de **skills** (conhecimento de domínio em Markdown) orquestrado via Claude API.

## Arquitetura

```
User Query → Router (keyword match) → Skill selecionada → Prompt montado → Claude API → Resposta
```

### Skills disponíveis

| Skill | Arquivo | Domínio |
|---|---|---|
| Demografia | `data/skill_demografia.md` | Perfil geracional, pirâmide demográfica |
| Bancos | `data/skill_bancos.md` | Crédito consignado, fraudes, atendimento |
| UX Sênior | `data/skill_ux.md` | Acessibilidade, WhatsApp, interfaces |

## Setup

```bash
# 1. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate       # Windows

# 2. Instale as dependências
pip install -r requirements.txt

# 3. Configure a API key
copy .env.example .env
# Edite .env com sua ANTHROPIC_API_KEY

# 4. Rode o CLI
python main.py

# 5. (Opcional) Rode o chat Streamlit
streamlit run app.py
```

## Uso (CLI)

```
> Qual o perfil demográfico dos aposentados no Brasil?
[Router] Skill selecionada: demografia
[Resposta] ...

> /skills          # Lista skills disponíveis
> /skill bancos    # Força uso de uma skill específica
> /dry             # Toggle modo dry-run (mostra prompt sem chamar API)
> /quit            # Sai
```

## Modo Dry-Run

Se `ANTHROPIC_API_KEY` não estiver configurada, o agente opera em **modo dry-run**: monta o prompt completo e exibe sem chamar a API. Útil para validar routing e montagem de contexto.

## Adicionar nova skill

1. Crie um arquivo `.md` em `data/` com frontmatter YAML:

```yaml
---
skill_name: minha_skill
domain: meu domínio
keywords:
  - palavra1
  - palavra2
prompt_template: >
  Atue como especialista em X. Considere {background} para responder.
---

# Background

Conteúdo do conhecimento prévio aqui...
```

2. Reinicie o agente — a skill será detectada automaticamente.
