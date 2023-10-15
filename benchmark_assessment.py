from typing import List
from config import GameResult, Bots
from game_builder import GameBuilder
from seed import Seed


class BenchmarkAssessment:
    def __init__(self, iterations: int, d: int, q: int, bot_variant: Bots):
        self.iterations = iterations
        self.d = d
        self.q = q
        self.bot_variant = bot_variant
        self.results = []

    def run(self, output: bool = False, seed: Seed = None) -> List[GameResult]:
        benchmarks = []
        for _ in range(self.iterations):
            game = GameBuilder()\
                .add_ship(D=self.d, q=self.q, seed=seed)\
                .add_bot(self.bot_variant, q=self.q)\
                .build()
            benchmarks.append(game.play(output))
        return benchmarks
