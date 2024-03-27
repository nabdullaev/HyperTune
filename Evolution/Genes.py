import random


class GeneType(object):
    def __init__(self, parameters):
        self.parameters = parameters
        self.value = None

    def get(self):
        raise NotImplementedError('Base gene type does not provide actions.')

    def copy(self):
        return self.__copy__()

    def __copy__(self):
        raise NotImplementedError('Base gene type does not provide actions.')

    def __str__(self):
        return f'{self.__class__.__name__} {self.parameters}'

    def __repr__(self):
        return self.__str__()


class DiscreteGene(GeneType):
    def __init__(self, parameters):
        super().__init__(parameters)

    def get(self):
        return random.choice(self.parameters)

    def __copy__(self):
        return DiscreteGene(self.parameters)


class ContinuousGene(GeneType):
    def __init__(self, parameters):
        super().__init__(parameters)

    def get(self):
        return self.parameters[0] + random.random() * (self.parameters[1] - self.parameters[0])

    def __copy__(self):
        return ContinuousGene(self.parameters)


class CompositeGene(GeneType):
    def __init__(self, size, parameters):
        super().__init__(parameters)
        self.size = size

    def get(self):
        rng = self.parameters

        if type(rng) is tuple:
            return tuple([rng[0] + random.random() * (rng[1] - rng[0]) for _ in range(self.size)])

        return tuple([random.choice(rng) for _ in range(self.size)])

    def __copy__(self):
        return CompositeGene(self.size, self.parameters)

    def __str__(self):
        return super().__str__() + f' size: {self.size}'
