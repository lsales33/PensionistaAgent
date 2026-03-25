"""Roteia a query do usuário para a(s) skill(s) mais relevante(s)."""

import re
import unicodedata

from agent.skill_loader import SkillData


def _normalize(text: str) -> str:
    """Remove acentos e converte para minúsculas."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c)).lower()


def _tokenize(text: str) -> set[str]:
    """Tokeniza texto em palavras normalizadas (sem acentos, minúsculas)."""
    normalized = _normalize(text)
    return set(re.findall(r"[a-z0-9]+", normalized))


def route_query(
    query: str,
    skills: dict[str, SkillData],
    threshold: int = 1,
) -> list[SkillData]:
    """
    Retorna lista de skills ordenadas por relevância (maior score primeiro).

    - Se nenhuma skill atinge o threshold, retorna todas (fallback multi-skill).
    - Se apenas uma atinge, retorna só ela.
    - Se múltiplas atingem, retorna todas acima do threshold ordenadas por score.
    """
    tokens = _tokenize(query)

    scored: list[tuple[int, SkillData]] = []
    for skill in skills.values():
        # Normaliza keywords da skill para comparar sem acentos
        normalized_keywords = [_normalize(kw) for kw in skill.keywords]
        score = sum(1 for kw in normalized_keywords if kw in tokens)
        if score >= threshold:
            scored.append((score, skill))

    if not scored:
        # Fallback: retorna todas as skills como contexto combinado
        return list(skills.values())

    scored.sort(key=lambda x: x[0], reverse=True)
    return [skill for _, skill in scored]
