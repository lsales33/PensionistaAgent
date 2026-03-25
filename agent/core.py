"""Classe principal do PensionistaAgent — orquestra skills e LLM providers."""

import os
from pathlib import Path

from dotenv import load_dotenv

from agent.router import route_query
from agent.skill_loader import SkillData, load_all_skills

# Carrega .env do diretório do projeto
load_dotenv(Path(__file__).resolve().parent.parent / ".env")

SYSTEM_PROMPT = """\
Você é um assistente especializado no atendimento a aposentados e pensionistas brasileiros.

Personalidade e estilo:
- Empático e paciente — o público é majoritariamente idoso (60+).
- Linguagem clara e simples — evite jargões técnicos. Quando precisar usar um termo técnico, explique-o.
- Direto e estruturado — use listas, passos numerados e headers quando apropriado.
- Honesto — se não souber algo ou a informação for incerta, diga claramente.
- Sem bajulação — não comece com "Ótima pergunta!" ou similares. Vá direto ao ponto.

Método de raciocínio (antes de responder):
1. Analise a pergunta — identifique a intenção real do usuário.
2. Identifique as dimensões-chave — quais fatores são relevantes.
3. Planeje a resposta — estruture formato e tom adequados.
4. Responda — de forma clara, acessível e fundamentada no conhecimento fornecido.

Restrições:
- NÃO invente dados estatísticos. Use apenas o que está no conhecimento prévio fornecido.
- NÃO dê conselhos financeiros específicos (ex: "invista em X"). Oriente a buscar profissionais.
- NÃO sermonize ou seja paternalista. Respeite a autonomia do idoso.
"""

# ── Provider registry ──────────────────────────────────────────────
PROVIDERS = {
    "groq": {
        "env_key": "GROQ_API_KEY",
        "default_model": "llama-3.3-70b-versatile",
        "label": "Groq (Llama 3.3 70B)",
        "free": True,
        "signup": "https://console.groq.com/keys",
    },
    "gemini": {
        "env_key": "GEMINI_API_KEY",
        "default_model": "gemini-2.0-flash",
        "label": "Google Gemini 2.0 Flash",
        "free": True,
        "signup": "https://aistudio.google.com/apikey",
    },
    "anthropic": {
        "env_key": "ANTHROPIC_API_KEY",
        "default_model": "claude-sonnet-4-20250514",
        "label": "Anthropic Claude",
        "free": False,
        "signup": "https://console.anthropic.com/",
    },
}


def _detect_provider() -> tuple[str | None, str]:
    """Auto-detecta qual provider tem API key configurada. Prioriza gratuitos."""
    forced = os.environ.get("LLM_PROVIDER", "").strip().lower()
    if forced and forced in PROVIDERS:
        key = os.environ.get(PROVIDERS[forced]["env_key"], "")
        if key and not key.endswith("AQUI"):
            return forced, key
    # Auto-detect: tenta gratuitos primeiro
    for name in ["groq", "gemini", "anthropic"]:
        info = PROVIDERS[name]
        key = os.environ.get(info["env_key"], "")
        if key and not key.endswith("AQUI"):
            return name, key
    return None, ""


class PensionistaAgent:
    def __init__(self, data_dir: str = "data"):
        self.skills = load_all_skills(data_dir)
        self.dry_run = False
        self.provider_name = None
        self.provider_label = "Nenhum"
        self.model = ""
        self.client = None

        provider, api_key = _detect_provider()

        if provider == "groq":
            from groq import Groq
            self.client = Groq(api_key=api_key)
            self.provider_name = "groq"
            self.model = os.environ.get("LLM_MODEL", PROVIDERS["groq"]["default_model"])
            self.provider_label = f"Groq ({self.model})"

        elif provider == "gemini":
            from google import genai
            self.client = genai.Client(api_key=api_key)
            self.provider_name = "gemini"
            self.model = os.environ.get("LLM_MODEL", PROVIDERS["gemini"]["default_model"])
            self.provider_label = f"Gemini ({self.model})"

        elif provider == "anthropic":
            import anthropic
            self.client = anthropic.Anthropic(api_key=api_key)
            self.provider_name = "anthropic"
            self.model = os.environ.get("LLM_MODEL", PROVIDERS["anthropic"]["default_model"])
            self.provider_label = f"Anthropic ({self.model})"

        else:
            self.dry_run = True
            self.provider_label = "DRY-RUN (sem API key)"

    def list_skills(self) -> list[str]:
        return list(self.skills.keys())

    def _build_context(self, selected_skills: list[SkillData]) -> str:
        sections = []
        for skill in selected_skills:
            sections.append(
                f"=== SKILL: {skill.name.upper()} ({skill.domain}) ===\n\n"
                f"{skill.background}"
            )
        return "\n\n---\n\n".join(sections)

    def _build_prompt_directives(self, selected_skills: list[SkillData]) -> str:
        directives = []
        for skill in selected_skills:
            if skill.prompt_template:
                directives.append(skill.prompt_template.strip())
        return "\n".join(directives)

    # ── Provider-specific call methods ──────────────────────────────

    def _call_groq(self, system: str, user_msg: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model,
            max_tokens=2048,
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": user_msg},
            ],
        )
        return response.choices[0].message.content or "(sem resposta)"

    def _call_gemini(self, system: str, user_msg: str) -> str:
        response = self.client.models.generate_content(
            model=self.model,
            contents=user_msg,
            config={
                "system_instruction": system,
                "max_output_tokens": 2048,
            },
        )
        return response.text or "(sem resposta)"

    def _call_anthropic(self, system: str, user_msg: str) -> str:
        response = self.client.messages.create(
            model=self.model,
            max_tokens=2048,
            system=system,
            messages=[{"role": "user", "content": user_msg}],
        )
        return response.content[0].text if response.content else "(sem resposta)"

    # ── Main generate ───────────────────────────────────────────────

    def generate_response(
        self,
        user_query: str,
        skill_name: str | None = None,
    ) -> dict:
        # 1. Seleciona skill(s)
        if skill_name and skill_name in self.skills:
            selected = [self.skills[skill_name]]
        else:
            selected = route_query(user_query, self.skills)

        skill_names = [s.name for s in selected]

        # 2. Monta contexto
        context = self._build_context(selected)
        directives = self._build_prompt_directives(selected)

        user_message = (
            f"{directives}\n\n"
            f"CONHECIMENTO PRÉVIO:\n{context}\n\n"
            f"PERGUNTA DO USUÁRIO:\n{user_query}"
        )

        # 3. Dry-run ou chamada real
        if self.dry_run or self.client is None:
            return {
                "skills_used": skill_names,
                "answer": (
                    f"[DRY-RUN] Prompt montado ({len(user_message)} chars):\n\n"
                    f"--- SYSTEM ---\n{SYSTEM_PROMPT[:300]}...\n\n"
                    f"--- USER MESSAGE ---\n{user_message[:800]}...\n\n"
                    f"[Configure uma API key no .env para chamada real]\n"
                    f"Opções gratuitas:\n"
                    f"  • GROQ_API_KEY → https://console.groq.com/keys\n"
                    f"  • GEMINI_API_KEY → https://aistudio.google.com/apikey"
                ),
                "dry_run": True,
                "provider": "none",
            }

        # Chama o provider correto
        callers = {
            "groq": self._call_groq,
            "gemini": self._call_gemini,
            "anthropic": self._call_anthropic,
        }
        try:
            answer = callers[self.provider_name](SYSTEM_PROMPT, user_message)
        except Exception as e:
            return {
                "skills_used": skill_names,
                "answer": f"❌ Erro ao chamar {self.provider_label}: {e}",
                "dry_run": False,
                "provider": self.provider_name,
            }

        return {
            "skills_used": skill_names,
            "answer": answer,
            "dry_run": False,
            "provider": self.provider_name,
        }
