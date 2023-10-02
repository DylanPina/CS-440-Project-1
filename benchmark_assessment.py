from typing import List
from config import GameResult, Bots
from game_builder import GameBuilder


class BenchmarkAssessment:
    def __init__(self, iterations: int, d: int, q: int, bot_variant: Bots):
        self.iterations = iterations
        self.d = d
        self.q = q
        self.bot_variant = bot_variant
        self.results = []

    def run(self) -> List[GameResult]:
        benchmarks = []
        for _ in range(self.iterations):
            game = GameBuilder()\
                .add_ship(D=self.d, q=self.q)\
                .add_bot(self.bot_variant)\
                .build()
            benchmarks.append(game.play())
        return benchmarks
        
