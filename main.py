"""CLI interativo do PensionistaAgent."""

import sys
from pathlib import Path

# Garante que o diretório do projeto está no sys.path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from agent.core import PensionistaAgent


def print_header():
    print("\n" + "=" * 60)
    print("  🧓 PensionistaAgent — Assistente para Aposentados")
    print("=" * 60)
    print()


def print_help():
    print("  Comandos disponíveis:")
    print("  /skills          Lista skills carregadas")
    print("  /skill <nome>    Força uso de uma skill específica")
    print("  /dry             Toggle modo dry-run")
    print("  /help            Mostra esta ajuda")
    print("  /quit            Sai do programa")
    print()


def main():
    data_dir = PROJECT_DIR / "data"

    if not data_dir.exists():
        print(f"ERRO: Diretório de dados não encontrado: {data_dir}")
        sys.exit(1)

    agent = PensionistaAgent(data_dir=str(data_dir))

    print_header()
    print(f"  Skills carregadas: {', '.join(agent.list_skills())}")
    print(f"  Modo: {'🔧 DRY-RUN (sem API key)' if agent.dry_run else '🟢 LIVE (API conectada)'}")
    print()
    print_help()

    forced_skill = None

    while True:
        try:
            prompt = f"[skill:{forced_skill}] > " if forced_skill else "> "
            user_input = input(prompt).strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nAté logo! 👋")
            break

        if not user_input:
            continue

        # Comandos especiais
        if user_input.startswith("/"):
            cmd = user_input.lower().split()
            match cmd[0]:
                case "/quit" | "/exit" | "/q":
                    print("\nAté logo! 👋")
                    break
                case "/skills":
                    for name in agent.list_skills():
                        skill = agent.skills[name]
                        print(f"  • {name}: {skill.domain} ({len(skill.keywords)} keywords)")
                    print()
                case "/skill":
                    if len(cmd) < 2:
                        forced_skill = None
                        print("  Skill forçada removida — usando auto-routing.")
                    elif cmd[1] in agent.skills:
                        forced_skill = cmd[1]
                        print(f"  Skill forçada: {forced_skill}")
                    else:
                        print(f"  Skill '{cmd[1]}' não encontrada. Disponíveis: {', '.join(agent.list_skills())}")
                    print()
                case "/dry":
                    agent.dry_run = not agent.dry_run
                    print(f"  Modo dry-run: {'LIGADO 🔧' if agent.dry_run else 'DESLIGADO 🟢'}")
                    print()
                case "/help":
                    print_help()
                case _:
                    print(f"  Comando desconhecido: {cmd[0]}. Digite /help.")
                    print()
            continue

        # Query normal
        print()
        result = agent.generate_response(user_input, skill_name=forced_skill)

        skills_str = ", ".join(result["skills_used"])
        print(f"  [Router] Skills: {skills_str}")
        if result["dry_run"]:
            print(f"  [Modo DRY-RUN]")
        print(f"  {'─' * 50}")
        print()
        print(result["answer"])
        print()


if __name__ == "__main__":
    main()
