<div align="center">

# 📚 AI Study Buddy

**Bot de estudos com IA — resume anotações de aula, cria flashcards e agenda revisões espaçadas. Integrado com Telegram.**

![Python](https://img.shields.io/badge/Python-3.11%2B-3776AB?style=for-the-badge&logo=python&logoColor=white)
![OpenAI API](https://img.shields.io/badge/OpenAI%20API-gpt--4o-412991?style=for-the-badge&logo=openai&logoColor=white)
![Telegram Bot](https://img.shields.io/badge/Telegram%20Bot-2CA5E0?style=for-the-badge&logo=telegram&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![Anki](https://img.shields.io/badge/Anki-23B3E0?style=for-the-badge&logo=anki&logoColor=white)

</div>

---

O **AI Study Buddy** é um assistente de estudos que roda dentro do Telegram. Ele pega suas anotações de aula, usa a **OpenAI API** para transformá-las em resumos claros e flashcards, e agenda revisões no momento ideal para você não esquecer — graças ao algoritmo de **repetição espaçada (SM-2)**.

## ✨ Funcionalidades

|  | Recurso | Descrição |
|---|---|---|
| 🤖 | **Resumo de anotações** | Envie suas anotações e receba um resumo estruturado gerado por IA |
| 🃏 | **Geração de flashcards** | O resumo vira automaticamente perguntas e respostas no formato Anki |
| ⏰ | **Revisão espaçada** | O algoritmo SM-2 agenda cada revisão no intervalo ideal (1, 6, 15+ dias) |
| 🗄️ | **Persistência local** | Todo o histórico fica salvo em um banco SQLite — seus dados, seu controle |
| 📱 | **100% no Telegram** | Estude pelo celular, sem instalar mais nada |
| 📤 | **Exportação Anki** | Flashcards compatíveis com a importação do Anki Desktop/AnkiDroid |

## 🛠️ Stack tecnológica

| Tecnologia | Papel no projeto |
|---|---|
| [Python 3.11+](https://www.python.org/) | Linguagem principal |
| [python-telegram-bot](https://python-telegram-bot.org/) | Comunicação com o Telegram (API assíncrona v20+) |
| [OpenAI API](https://platform.openai.com/) | Resumos e geração de flashcards com IA |
| [SQLite](https://www.sqlite.org/) | Banco de dados local (módulo padrão do Python) |
| [Anki](https://apps.ankiweb.net/) | Formato de exportação dos flashcards |
| [schedule](https://github.com/dbader/schedule) | Agendamento das revisões diárias |

## 🚀 Como executar

### 1. Clone o repositório

```bash
git clone https://github.com/Fellipeg7/ai-study-buddy.git
cd ai-study-buddy
```

### 2. Crie um ambiente virtual e instale as dependências

```bash
python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scripts\activate         # Windows (PowerShell)

pip install -r requirements.txt
```

### 3. Configure as variáveis de ambiente

```bash
cp config.example.env config.env
# edite o config.env e preencha TELEGRAM_BOT_TOKEN e OPENAI_API_KEY
```

- **TELEGRAM_BOT_TOKEN** — crie um bot com o [@BotFather](https://t.me/BotFather) e copie o token que ele enviar.
- **OPENAI_API_KEY** — gere uma chave em [platform.openai.com/api-keys](https://platform.openai.com/api-keys).

> O bot lê o arquivo `config.env` automaticamente ao iniciar. Nunca versione esse arquivo — ele está no `.gitignore`.

### 4. Rode o bot

```bash
python -m src.bot
```

Abra o Telegram, procure o seu bot e envie `/start`. Para testar a repetição espaçada sem o bot, execute:

```bash
python -m src.study
```

## 📂 Estrutura do projeto

```
ai-study-buddy/
├── src/
│   ├── bot.py          # Bot do Telegram: comandos /start e /flashcard
│   └── study.py        # Flashcard + algoritmo de repetição espaçada (SM-2)
├── config.example.env  # Modelo de configuração (copie para config.env)
├── requirements.txt    # Dependências do projeto
├── LICENSE             # Licença MIT
└── README.md           # Este arquivo
```

## 🗺️ Roadmap

### ✅ Concluído
- [x] Esqueleto do bot no Telegram (`/start`, `/flashcard`)
- [x] Modelo de `Flashcard` e algoritmo de repetição espaçada SM-2 em `src/study.py`

### 🚧 Em desenvolvimento
- [ ] Integração com a OpenAI API (resumo de anotações e geração de flashcards)
- [ ] Persistência em SQLite (criar, consultar e atualizar flashcards)
- [ ] Exportação de baralhos no formato Anki (`.apkg`)

### 🔮 Planejado
- [ ] Agendamento de revisões diárias com `schedule`
- [ ] Comando `/review` para sessões de revisão com autoavaliação (0–5)
- [ ] Estatísticas de progresso e curva de esquecimento
- [ ] Suporte a múltiplas disciplinas e baralhos

## 🧠 Como funciona a repetição espaçada?

A **curva do esquecimento** (Ebbinghaus) mostra que, sem revisão, perdemos cerca de 50% do que aprendemos em poucos dias. A **repetição espaçada** combate isso revisitando o conteúdo **pouco antes de você esquecê-lo** — e cada revisão bem-sucedida empurra a próxima para mais longe.

### O algoritmo SM-2

Este projeto implementa o **SM-2**, o algoritmo clássico do [SuperMemo](https://super-memory.com/english/ol/sm2.htm). Cada flashcard guarda três números:

| Campo | Significado |
|---|---|
| `repetitions` | Quantas revisões consecutivas foram bem-sucedidas |
| `interval` | Intervalo atual em dias até a próxima revisão |
| `ease_factor` | Fator de facilidade (EF), começa em **2.5** |

A cada revisão você avalia a dificuldade do card com uma nota `q` de **0 a 5**:

- **`q < 3`** (errou): o ciclo recomeça — `repetitions = 0` e `interval = 1` dia.
- **`q >= 3`** (acertou): o intervalo cresce de forma geométrica:

```
1ª revisão:  interval = 1 dia
2ª revisão:  interval = 6 dias
3ª revisão+: interval = interval × ease_factor
```

O fator de facilidade se ajusta à dificuldade percebida a cada revisão:

```
EF' = EF + (0.1 − (5 − q) × (0.08 + (5 − q) × 0.02))   (mínimo 1.3)
```

Na prática: um card fácil (`q = 5`) tem o intervalo quase dobrado a cada revisão; um card difícil (`q = 3`) avança devagar; um card errado (`q < 3`) volta ao início. É assim que o bot "sabe" quando revisar cada conteúdo.

### Exemplo prático

Um card novo (`EF = 2.5`) revisado sempre com `q = 5`:

| Revisão | Intervalo | Cálculo | EF após |
|---|---|---|---|
| 1ª | 1 dia | (primeira revisão) | 2.6 |
| 2ª | 6 dias | (segunda revisão) | 2.7 |
| 3ª | 16 dias | 6 × 2.7 | 2.8 |
| 4ª | 45 dias | 16 × 2.8 | 2.9 |

Depois de 4 revisões, o conteúdo fica retido por mais de um mês — com apenas alguns minutos de esforço por revisão. 🎓

## 📄 Licença

Distribuído sob a licença **MIT**. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.

---

<div align="center">
Feito com 💙 para estudantes — <a href="https://github.com/Fellipeg7">Fellipeg7</a>
</div>
