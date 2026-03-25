# 🧓 PensionistaAgent

Agente de IA especializado no atendimento a **aposentados e pensionistas**, com sistema modular de **skills**, interface web (chat HTML), webhook WhatsApp e suporte **multi-provider** (Groq, Gemini, Anthropic).

> **Demo**: deploy gratuito no Render.com com LLM gratuita via Groq

## Arquitetura

```
User Query → Router (keyword match) → Skill selecionada → Prompt montado → LLM Provider → Resposta
```

### Skills disponíveis

| Skill | Arquivo | Domínio |
|---|---|---|
| 📊 Demografia | `data/skill_demografia.md` | Perfil geracional, pirâmide demográfica, INSS |
| 🏦 Bancos | `data/skill_bancos.md` | Crédito consignado, fraudes, atendimento |
| 📱 UX Sênior | `data/skill_ux.md` | Acessibilidade, WhatsApp, interfaces |

### Providers suportados (gratuitos)

| Provider | Modelo | Como obter |
|---|---|---|
| **Groq** (recomendado) | llama-3.3-70b-versatile | [console.groq.com](https://console.groq.com) |
| **Google Gemini** | gemini-2.0-flash | [aistudio.google.com](https://aistudio.google.com/apikey) |
| **Anthropic** | claude-3-haiku | [console.anthropic.com](https://console.anthropic.com) |

## Setup Local

```bash
# 1. Clone o repositório
git clone https://github.com/SEU_USUARIO/PensionistaAgent.git
cd PensionistaAgent

# 2. Crie o ambiente virtual
python -m venv venv
venv\Scripts\activate       # Windows
source venv/bin/activate    # Linux/Mac

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Configure a API key (pelo menos uma)
copy .env.example .env
# Edite .env com sua GROQ_API_KEY (ou GEMINI_API_KEY)

# 5. Rode o servidor web
python server.py
# Acesse http://localhost:8080

# 6. (Alternativa) Rode o CLI
python main.py
```

## Interface Web

O servidor (`server.py`) oferece:
- **Chat web** em `http://localhost:8080` — interface dark theme com seletor de skills
- **API REST**: `POST /api/chat` com JSON `{"query": "...", "skill": "..."}`
- **WhatsApp webhook**: `POST /webhook/whatsapp` (compatível com Twilio)

## Deploy no Render.com (Gratuito)

### Opção 1: Script automático (Windows)
```powershell
.\deploy.ps1
```

### Opção 2: Manual
1. Faça push do código para o GitHub
2. Acesse [render.com](https://render.com) e faça login com GitHub
3. Clique **New +** → **Web Service**
4. Conecte o repositório `PensionistaAgent`
5. O Render detecta automaticamente o `render.yaml`
6. Em **Environment**, adicione: `GROQ_API_KEY` = sua chave
7. Clique **Create Web Service**

O app ficará disponível em `https://pensionistaagent.onrender.com`

## Uso (CLI)

```
> Qual o perfil demográfico dos aposentados no Brasil?
[Router] Skill selecionada: demografia
[Resposta] ...

> /skills          # Lista skills disponíveis
> /skill bancos    # Força uso de uma skill específica
> /dry             # Toggle modo dry-run
> /quit            # Sai
```

## Modo Dry-Run

Se nenhuma API key estiver configurada, o agente opera em **modo dry-run**: monta o prompt completo e exibe sem chamar a API.

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
