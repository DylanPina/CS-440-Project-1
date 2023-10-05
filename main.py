from game_builder import GameBuilder
from config import Bots
from benchmark_assessment import BenchmarkAssessment
import statistics
import matplotlib.pyplot as plt
from matplotlib.ticker import (MultipleLocator,
                               FormatStrFormatter,
                               AutoMinorLocator)

if __name__ == "__main__":
    ITR = 100
    DVAL = 100
    qvals = [0.05, 0.1, 0.15, 0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5,
             0.55, 0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1.0]

    for bot in Bots:
        successMap = []

        for qval in qvals:
            benchmark = BenchmarkAssessment(
                iterations=ITR, d=DVAL, q=qval, bot_variant=bot).run()
            print(*benchmark)

            success = []
            for mark in benchmark:
                if mark.outcome is True:
                    success.append(1)
                else:
                    success.append(0)

            successMap.append(statistics.mean(success))

        figure, axis = plt.subplots()
        # set title for graph, x and y axis
        axis.set_title(
            f"{bot} - {ITR} for each q value, ship of size {DVAL}x{DVAL}")
        axis.set_ylabel('Success Rate')
        axis.set_xlabel('q')
        # set limit for x and y axis
        axis.set_xlim(0, 1)
        axis.set_ylim(0, 1)
        # set major ticks multiple of 1
        axis.xaxis.set_major_locator(MultipleLocator(1))
        axis.xaxis.set_major_formatter(FormatStrFormatter('% 1.2f'))
        # set minor ticks multiple of 0.1
        axis.xaxis.set_minor_locator(MultipleLocator(0.1))
        axis.xaxis.set_minor_formatter(FormatStrFormatter('% 1.2f'))
        # plot, save, and clear
        axis.plot(qvals, successMap)
        plt.savefig(f"{bot}-ITR:{ITR}-D:{DVAL}")
        plt.clf()
