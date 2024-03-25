from EvolutionaryLib import *


class MyChromosome(BaseChromosome):
    def __init__(self):
        super().__init__()

    def crossover(self, other):
        new = MyChromosome()
        self.copy_prototypes(new)

        return

    def mutate(self, rate=0.3):
        new = MyChromosome()
        self.copy_prototypes(new)
        prototypes = new.get_field_prototypes()

        for field in self.get_field_names():
            if random.random() < rate:
                setattr(new, field, prototypes['_' + field].get())
            else:
                setattr(new, field, getattr(self, field))

        return new


if __name__ == '__main__':
    chromosome_factory = ChromosomeClassFactory(a=list(range(1, 10)),
                                                b=(1, 5),
                                                c={'n': 4, 'range': (1, 100)},
                                                d={'n': 2, 'range': list(range(1, 5))}
                                                )
    print(chromosome_factory)
    c1 = chromosome_factory.generate(MyChromosome)
    c2 = chromosome_factory.generate(MyChromosome)

    print(c1)
    print(c1.mutate())

    print(c1.get_field_prototypes())
