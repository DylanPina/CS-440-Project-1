from game_builder import GameBuilder
from config import Bots
from benchmark_assessment import BenchmarkAssessment


if __name__ == "__main__":
    benchmark = BenchmarkAssessment(iterations=10, d=10, q=0.5, bot_variant=Bots.BOT1).run()
    print(*benchmark)