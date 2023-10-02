from game_builder import GameBuilder
from config import Bots


if __name__ == "__main__":
    benchmarks = []
    for _ in range(1):
        game = GameBuilder().add_ship(D=100, q=0.5).add_bot(Bots.BOT4).build()
        benchmarks.append(game.play())
    
    print(*benchmarks)
