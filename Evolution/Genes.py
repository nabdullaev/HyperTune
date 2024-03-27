import random
from numbers import Number


class GeneType(object):
    def __init__(self, parameters):
        self.parameters = parameters
        self.value = None

    def get(self):
        raise NotImplementedError('Base gene type does not provide actions.')

    def copy(self):
        return self.__copy__()

    def crossover(self, other):
        raise NotImplementedError('Base gene type does not provide actions.')

    def mutate(self):
        raise NotImplementedError('Base gene type does not provide actions.')

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

    def __setattr__(self, key, value):
        if key != 'value':
            self.__dict__[key] = value
            return

        if value in self.parameters or value is None:
            self.__dict__[key] = value
            return

        raise ValueError('This gene does not support such value')

    def __copy__(self):
        return DiscreteGene(self.parameters)


class ContinuousGene(GeneType):
    def __init__(self, parameters):
        super().__init__(parameters)
        self.parameters = (min(self.parameters), max(self.parameters))

    def get(self):
        return self.parameters[0] + random.random() * (self.parameters[1] - self.parameters[0])

    def __setattr__(self, key, value):
        if key != 'value':
            self.__dict__[key] = value
            return

        if value is None or (isinstance(value, Number) and self.parameters[0] <= value <= self.parameters[1]):
            self.__dict__[key] = value
            return

        raise ValueError('This gene does not support such value')

    def __copy__(self):
        return ContinuousGene(self.parameters)


class CompositeGene(GeneType):
    def __init__(self, size, parameters):
        super().__init__(parameters)
        self.size = size

    def get(self):
        rng = self.parameters

        if type(rng) is tuple:
            return tuple([rng[0] + random.random() * (rng[1] - rng[0]) for _ in range(random.choice(self.size))])

        return tuple([random.choice(rng) for _ in range(random.choice(self.size))])

    def crossover(self, other):
        current_size = random.choice([len(self.value), len(other.value)])
        values_set = self.value + other.value
        return tuple([random.choice(values_set) for _ in range(current_size)])

    def mutate(self):
        return self.get()

    def __copy__(self):
        return CompositeGene(self.size, self.parameters)

    def __str__(self):
        return super().__str__() + f' size: {self.size}'
