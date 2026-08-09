"""
AI Study Buddy — Bot do Telegram.

Esqueleto mínimo com dois comandos:
    /start      — mensagem de boas-vindas
    /flashcard  — mostra um flashcard aleatório para revisão

Execute a partir da raiz do projeto:
    python -m src.bot

Requer a variável de ambiente TELEGRAM_BOT_TOKEN (veja config.example.env).
O arquivo config.env é carregado automaticamente se existir.
"""

import logging
import os
import random

from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# Importa o núcleo de estudo. O fallback permite executar tanto
# `python -m src.bot` quanto `python src/bot.py`.
try:
    from src.study import Flashcard, sample_deck
except ImportError:  # pragma: no cover — execução direta do arquivo
    from study import Flashcard, sample_deck  # type: ignore

# ---------------------------------------------------------------------------
# Configuração
# ---------------------------------------------------------------------------
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Baralho de exemplo em memória. Em breve, os cards virão do SQLite!
DECK: list[Flashcard] = sample_deck()


def _load_env_file(path: str = "config.env") -> None:
    """Carrega chave=valor de um arquivo .env simples (sem instalar dotenv).

    Linhas em branco e comentários (#) são ignorados. Variáveis já
    presentes no ambiente não são sobrescritas.
    """
    if not os.path.exists(path):
        return
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())


# ---------------------------------------------------------------------------
# Handlers
# ---------------------------------------------------------------------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Envia a mensagem de boas-vindas."""
    await update.message.reply_text(
        "👋 Olá! Eu sou o *AI Study Buddy*.\n\n"
        "Envie /flashcard para revisar um card, ou cole suas anotações "
        "de aula para eu gerar um resumo e flashcards (em breve!)."
    )


async def flashcard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Mostra a pergunta de um flashcard aleatório do baralho."""
    card: Flashcard = random.choice(DECK)
    await update.message.reply_text(
        f"🃏 *Pergunta:*\n{card.question}\n\n"
        "Responda mentalmente e depois confira a resposta (em breve! 📤)."
    )


# ---------------------------------------------------------------------------
# Bootstrap
# ---------------------------------------------------------------------------
def main() -> None:
    _load_env_file()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        raise SystemExit(
            "❌ TELEGRAM_BOT_TOKEN não encontrado.\n"
            "Copie config.example.env para config.env, preencha o token "
            "e tente novamente."
        )

    app = Application.builder().token(token).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("flashcard", flashcard))

    logger.info("Bot iniciado. Pressione Ctrl+C para encerrar.")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
