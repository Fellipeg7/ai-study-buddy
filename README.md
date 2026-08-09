# AI Study Buddy

Bot de estudos com IA que roda no Telegram. Eu criei ele porque queria uma forma mais inteligente de estudar -- resumir anotações de aula, criar flashcards automaticamente e revisar no momento certo pra nao esquecer.

## Sobre o projeto

Esse projeto surgiu da necessidade de organizar meus estudos na faculdade. A ideia e simples: voce manda suas anotações de aula pelo Telegram, a IA gera um resumo estruturado e flashcards, e o bot agenda revisoes no intervalo ideal usando o algoritmo de repetição espaçada SM-2.

Hoje ele ja ta funcional -- resumo de anotações, geração de flashcards e revisão espaçada basica. O roadmap inclui exportação pro Anki e integração com mais plataformas.

## Funcionalidades

| Recurso | Descrição |
|---------|-----------|
| Resumo de anotações | Envie suas anotações e receba um resumo estruturado gerado por IA |
| Geração de flashcards | O resumo vira automaticamente perguntas e respostas no formato Anki |
| Revisão espaçada | O algoritmo SM-2 agenda cada revisão no intervalo ideal (1, 6, 15+ dias) |
| Persistência local | Todo o histórico fica salvo em um banco SQLite |
| 100% no Telegram | Estude pelo celular, sem instalar mais nada |
| Exportação Anki | Flashcards compatíveis com a importação do Anki Desktop/AnkiDroid |

## Stack tecnológica

| Tecnologia | Papel no projeto |
|------------|-----------------|
| Python 3.11+ | Linguagem principal |
| python-telegram-bot | Comunicação com o Telegram (API assíncrona v20+) |
| OpenAI API | Resumos e geração de flashcards com IA |
| SQLite | Banco de dados local (módulo padrão do Python) |
| Anki | Formato de exportação dos flashcards |
| schedule | Agendamento das revisões diárias |

## Como executar

### 1. Clone o repositorio

git clone https://github.com/Fellipeg7/ai-study-buddy.git
cd ai-study-buddy

### 2. Crie um ambiente virtual e instale as dependências

python -m venv .venv
source .venv/bin/activate        # Linux/macOS
# .venv\Scriptsctivate         # Windows (PowerShell)

pip install -r requirements.txt

### 3. Configure as variáveis de ambiente

cp config.example.env config.env
# edite o config.env e preencha TELEGRAM_BOT_TOKEN e OPENAI_API_KEY

- **TELEGRAM_BOT_TOKEN** -- crie um bot com o @BotFather e copie o token que ele enviar.
- **OPENAI_API_KEY** -- gere uma chave em platform.openai.com/api-keys.

O bot lê o arquivo config.env automaticamente ao iniciar. Nunca versione esse arquivo -- ele esta no .gitignore.

### 4. Rode o bot

python -m src.bot

Abra o Telegram, procure o seu bot e envie /start. Para testar a repetição espaçada sem o bot, execute:

python -m src.study

## Estrutura do projeto

ai-study-buddy/
├── src/
│   ├── bot.py           # Bot do Telegram com handlers /start e /flashcard
│   └── study.py         # Classe Flashcard + algoritmo SM-2 de repetição espaçada
├── config.example.env   # Template de configuração (copie pra config.env)
├── requirements.txt     # Dependências Python
├── .gitignore           # Arquivos ignorados pelo Git
└── README.md            # Este arquivo

## Roadmap

- [x] Bot básico com /start e /flashcard
- [x] Algoritmo SM-2 de repetição espaçada
- [x] Persistência em SQLite
- [ ] Resumo de anotações com OpenAI API
- [ ] Exportação de flashcards no formato Anki (.apkg)
- [ ] Agendamento automático de revisões diárias
- [ ] Suporte a múltiplos idiomas
- [ ] Interface web para gerenciar flashcards

## Contribuindo

Se voce quiser contribuir, e so fazer um fork, criar uma branch e mandar um pull request. Qualquer melhoria é bem-vinda.

## Licença

Esse projeto esta sob a licença MIT -- veja o arquivo LICENSE para mais detalhes.
