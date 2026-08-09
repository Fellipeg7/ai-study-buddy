"""
AI Study Buddy — Núcleo de estudo.

Contém o modelo de Flashcard e a implementação do algoritmo de
repetição espaçada SM-2 (SuperMemo):

    https://super-memory.com/english/ol/sm2.htm

O SM-2 é o algoritmo clássico por trás de ferramentas como Anki e
Mnemosyne: a cada revisão, o usuário avalia a dificuldade do card com
uma nota de 0 a 5, e o algoritmo decide o próximo intervalo de revisão.

Uso rápido:

    card = Flashcard("O que é repetição espaçada?", "Revisar no momento ideal...")
    sm2 = SM2()
    sm2.review(card, quality=5)   # acertou com facilidade
    print(card.interval)          # 1 (primeira revisão)
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date, timedelta


@dataclass
class Flashcard:
    """Um par pergunta/resposta com o estado da repetição espaçada."""

    question: str
    answer: str
    repetitions: int = 0        # revisões bem-sucedidas consecutivas
    interval: int = 1           # intervalo atual, em dias
    ease_factor: float = 2.5    # fator de facilidade (EF)
    due_date: str = field(default_factory=lambda: date.today().isoformat())

    def __str__(self) -> str:
        return f"Q: {self.question}\nR: {self.answer}"


QUALITY_LABELS: dict[int, str] = {
    5: "perfeito — resposta imediata e correta",
    4: "certo — com pequena hesitação",
    3: "certo — com bastante esforço",
    2: "errado — mas a resposta pareceu familiar",
    1: "errado — mas lembrei da resposta ao ver",
    0: "erro total — nem lembrava do card",
}


class SM2:
    """Algoritmo de repetição espaçada SM-2.

    Regras (resumo):
      - qualidade < 3  → o card volta ao início (repetitions = 0, interval = 1)
      - qualidade >= 3 → repetitions += 1 e o intervalo cresce:
            rep 1 → 1 dia; rep 2 → 6 dias; rep n → interval × ease_factor
      - ease_factor é reajustado pela fórmula do SM-2 (mínimo 1.3)
    """

    MIN_EASE_FACTOR = 1.3
    FIRST_INTERVAL = 1
    SECOND_INTERVAL = 6

    def review(self, card: Flashcard, quality: int) -> Flashcard:
        """Aplica uma avaliação (0–5) e agenda a próxima revisão do card."""
        if not 0 <= quality <= 5:
            raise ValueError("quality deve ser um inteiro entre 0 e 5")

        if quality < 3:
            # Resposta errada: o ciclo recomeça.
            card.repetitions = 0
            card.interval = self.FIRST_INTERVAL
        else:
            card.repetitions += 1
            if card.repetitions == 1:
                card.interval = self.FIRST_INTERVAL
            elif card.repetitions == 2:
                card.interval = self.SECOND_INTERVAL
            else:
                card.interval = round(card.interval * card.ease_factor)

        # Reajusta o fator de facilidade (nunca abaixo do mínimo).
        card.ease_factor = max(
            self.MIN_EASE_FACTOR,
            card.ease_factor
            + (0.1 - (5 - quality) * (0.08 + (5 - quality) * 0.02)),
        )

        # Agenda a próxima revisão.
        card.due_date = (date.today() + timedelta(days=card.interval)).isoformat()
        return card


def sample_deck() -> list[Flashcard]:
    """Baralho de exemplo usado pelo bot até existir integração com SQLite."""
    return [
        Flashcard(
            "O que é repetição espaçada?",
            "Técnica de estudo que revisa o conteúdo em intervalos crescentes, "
            "pouco antes de ele ser esquecido.",
        ),
        Flashcard(
            "Qual a fórmula de reajuste do fator de facilidade no SM-2?",
            "EF' = EF + (0.1 − (5 − q) × (0.08 + (5 − q) × 0.02)), "
            "com mínimo de 1.3.",
        ),
        Flashcard(
            "O que acontece quando a qualidade é menor que 3 no SM-2?",
            "O ciclo recomeça: repetitions volta a 0 e o intervalo volta a 1 dia.",
        ),
    ]


def _demo() -> None:
    """Simula 6 revisões de um card sempre avaliado com qualidade 5."""
    card = Flashcard("Exemplo", "Resposta")
    sm2 = SM2()
    print("Simulação: um card revisado sempre com qualidade 5\n")
    print(f"{'Revisão':>8} | {'Nota':>4} | {'Intervalo':>9} | {'EF':>5}")
    print("-" * 42)
    for i in range(1, 7):
        sm2.review(card, quality=5)
        print(f"{i:>8} | {5:>4} | {card.interval:>5} dias | {card.ease_factor:.2f}")


if __name__ == "__main__":
    _demo()
