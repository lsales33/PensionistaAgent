"""Script de setup para expor o PensionistaAgent à internet."""

import os
import sys
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_DIR))


def setup_ngrok():
    """Configura e inicia túnel ngrok."""
    token = os.environ.get("NGROK_AUTHTOKEN", "")
    if not token:
        print("=" * 60)
        print("  SETUP — Expor PensionistaAgent na Internet")
        print("=" * 60)
        print()
        print("Você precisa de um authtoken do ngrok (grátis):")
        print()
        print("  1. Acesse: https://dashboard.ngrok.com/signup")
        print("  2. Crie conta com Google/GitHub")
        print("  3. Copie seu authtoken em:")
        print("     https://dashboard.ngrok.com/get-started/your-authtoken")
        print()
        token = input("Cole seu NGROK_AUTHTOKEN aqui: ").strip()
        if not token:
            print("Authtoken vazio. Abortando.")
            return

    from pyngrok import conf, ngrok

    conf.get_default().auth_token = token

    port = int(os.environ.get("PORT", 8080))
    tunnel = ngrok.connect(port, "http")
    public_url = tunnel.public_url

    print()
    print("=" * 60)
    print(f"  URL PÚBLICA: {public_url}")
    print(f"  Chat Web:    {public_url}")
    print(f"  WhatsApp:    {public_url}/webhook/whatsapp")
    print("=" * 60)
    print()
    print("Para WhatsApp (Twilio):")
    print(f"  Webhook URL: {public_url}/webhook/whatsapp")
    print()
    print("Pressione Ctrl+C para encerrar o túnel.")

    try:
        input()  # Mantém aberto
    except KeyboardInterrupt:
        ngrok.kill()
        print("\nTúnel encerrado.")


if __name__ == "__main__":
    setup_ngrok()
