import random

from EvolutionaryLib import *


class MyChromosome(BaseChromosome):
    def __init__(self):
        super().__init__()

    def crossover(self, other):
        new = MyChromosome()
        self.copy(new)

        for field in new:
            new[field].value = random.choice([self[field], other[field]]).value

        return new

    def mutate(self, rate=0.3):
        new = MyChromosome()
        self.copy(new)

        for field in new:
            if random.random() < rate:
                new[field].value = new[field].get()
            else:
                new[field] = self[field]
        return new


if __name__ == '__main__':
    chromosome_factory = ChromosomeClassFactory(
        a=(1, 3),
        b=list(range(1, 20)),
        c={'n': 3, 'range': (1, 40)},
        d={'n': 2, 'range': list(range(1, 5))})

    c1 = chromosome_factory.generate(MyChromosome)
    print(c1)

    c2 = chromosome_factory.generate(MyChromosome)
    print(c2)

    c3 = c1.crossover(c2)
    print(c3)

    c3 = c3.mutate()
    print(c3)
