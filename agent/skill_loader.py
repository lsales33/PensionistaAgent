"""Carrega e parseia skills em Markdown com YAML frontmatter."""

import os
from dataclasses import dataclass, field
from pathlib import Path

import frontmatter


@dataclass
class SkillData:
    name: str
    domain: str
    keywords: list[str]
    prompt_template: str
    background: str  # corpo Markdown sem o frontmatter
    source_path: str

    def matches(self, tokens: set[str]) -> int:
        """Retorna score de match: quantos keywords aparecem nos tokens."""
        return sum(1 for kw in self.keywords if kw in tokens)


def load_skill(path: str | Path) -> SkillData:
    """Carrega uma skill de um arquivo Markdown com frontmatter YAML."""
    path = Path(path)
    post = frontmatter.load(str(path))

    meta = post.metadata
    return SkillData(
        name=meta.get("skill_name", path.stem),
        domain=meta.get("domain", ""),
        keywords=[kw.lower() for kw in meta.get("keywords", [])],
        prompt_template=meta.get("prompt_template", ""),
        background=post.content,
        source_path=str(path),
    )


def load_all_skills(data_dir: str | Path) -> dict[str, SkillData]:
    """Carrega todas as skills .md de um diretório. Retorna dict {name: SkillData}."""
    data_dir = Path(data_dir)
    skills = {}

    for md_file in sorted(data_dir.glob("skill_*.md")):
        skill = load_skill(md_file)
        skills[skill.name] = skill

    return skills
