"""Servidor HTTP para o PensionistaAgent — serve HTML, API REST e webhook WhatsApp."""

import json
import os
import sys
from http.server import HTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# Garante que o diretório raiz do projeto está no path
PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))

from agent.core import PensionistaAgent

agent = PensionistaAgent(data_dir=str(PROJECT_DIR / "data"))

STATIC_DIR = PROJECT_DIR / "static"


class AgentHandler(SimpleHTTPRequestHandler):
    """Handler que serve arquivos estáticos e endpoints da API."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(STATIC_DIR), **kwargs)

    def do_GET(self):
        path = urlparse(self.path).path

        if path == "/api/skills":
            self._send_json(self._get_skills_info())
            return

        # Fallback: serve arquivos estáticos (index.html, etc.)
        super().do_GET()

    def end_headers(self):
        # Evita cache de HTML para garantir versão atualizada
        if hasattr(self, 'path') and (self.path == '/' or self.path.endswith('.html')):
            self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
            self.send_header('Pragma', 'no-cache')
            self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        path = urlparse(self.path).path
        content_len = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_len)

        if path == "/api/chat":
            try:
                data = json.loads(body)
            except (json.JSONDecodeError, ValueError):
                self._send_json({"error": "JSON inválido"}, status=400)
                return

            query = data.get("query", "").strip()
            if not query:
                self._send_json({"error": "query vazia"}, status=400)
                return

            skill = data.get("skill") or None
            result = agent.generate_response(user_query=query, skill_name=skill)
            self._send_json(result)
            return

        if path == "/webhook/whatsapp":
            self._handle_whatsapp(body)
            return

        self._send_json({"error": "Endpoint não encontrado"}, status=404)

    # ── WhatsApp (Twilio) webhook ───────────────────────────────────

    def _handle_whatsapp(self, body: bytes):
        """Processa mensagem do Twilio WhatsApp e responde com TwiML."""
        try:
            params = parse_qs(body.decode("utf-8"))
            incoming_msg = params.get("Body", [""])[0].strip()
            from_number = params.get("From", [""])[0]
        except Exception:
            incoming_msg = ""
            from_number = "desconhecido"

        if not incoming_msg:
            self._send_twiml("Envie uma pergunta e eu respondo! 🧓")
            return

        # Comandos especiais
        lower = incoming_msg.lower()
        if lower in ("oi", "olá", "ola", "hi", "hello", "menu"):
            self._send_twiml(
                "🧓 *PensionistaAgent*\n\n"
                "Sou um assistente para aposentados e pensionistas.\n\n"
                "Posso ajudar com:\n"
                "📊 Perfil demográfico\n"
                "🏦 Questões bancárias\n"
                "📱 Usabilidade digital\n\n"
                "Envie sua pergunta! Exemplo:\n"
                "_Como proteger idosos de golpes bancários?_"
            )
            return

        if lower == "skills":
            nomes = ", ".join(agent.list_skills())
            self._send_twiml(f"Skills carregadas: {nomes}")
            return

        # Gera resposta real
        print(f"[WhatsApp] {from_number}: {incoming_msg[:80]}")
        result = agent.generate_response(user_query=incoming_msg)
        answer = result["answer"]

        # Twilio limita mensagem a ~1600 chars
        if len(answer) > 1500:
            answer = answer[:1497] + "..."

        skills_tag = ", ".join(result["skills_used"])
        reply = f"{answer}\n\n_[Skills: {skills_tag}]_"
        self._send_twiml(reply)

    def _send_twiml(self, message: str):
        """Envia resposta em formato TwiML para o Twilio."""
        # Escapa XML characters
        safe = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        twiml = (
            '<?xml version="1.0" encoding="UTF-8"?>'
            "<Response>"
            f"<Message>{safe}</Message>"
            "</Response>"
        )
        body = twiml.encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/xml; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _get_skills_info(self) -> dict:
        """Retorna info das skills carregadas + status."""
        skills_info = {}
        for name, skill in agent.skills.items():
            skills_info[name] = {
                "domain": skill.domain,
                "keywords": skill.keywords,
            }
        return {
            "skills": skills_info,
            "dry_run": agent.dry_run,
            "provider": agent.provider_name or "none",
            "provider_label": agent.provider_label,
            "model": agent.model,
        }

    def _send_json(self, data: dict, status: int = 200):
        body = json.dumps(data, ensure_ascii=False).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """Responde pre-flight CORS."""
        self.send_response(204)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def log_message(self, format, *args):
        """Log mais limpo."""
        print(f"[{self.log_date_time_string()}] {args[0]}")


def main():
    port = int(os.environ.get("PORT", 8080))
    host = os.environ.get("HOST", "0.0.0.0")
    server = HTTPServer((host, port), AgentHandler)
    print(f"PensionistaAgent server rodando em http://localhost:{port}")
    print(f"Skills carregadas: {len(agent.skills)} — {', '.join(agent.list_skills())}")
    print(f"Provider: {agent.provider_label}")
    print(f"Modo: {'DRY-RUN' if agent.dry_run else 'LIVE'}")
    print(f"WhatsApp webhook: http://localhost:{port}/webhook/whatsapp")
    print("Ctrl+C para parar.\n")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServidor encerrado.")
        server.server_close()


if __name__ == "__main__":
    main()
