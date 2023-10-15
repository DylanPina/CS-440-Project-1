from game_builder import GameBuilder
from config import Bots
from benchmark_assessment import BenchmarkAssessment
from seed import Seed


if __name__ == "__main__":
    benchmark = BenchmarkAssessment(
        iterations=5, d=10, q=0.5, bot_variant=Bots.BOT4).run(output=True, seed=None)
    print(*benchmark)
