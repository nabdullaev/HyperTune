import random
import os
import contextlib


class GeneType(object):
    def __init__(self, values):
        self.values = values

    def get(self):
        raise NotImplementedError('Base gene type does not provide actions.')

    def __str__(self):
        return f'{self.__class__.__name__} {self.values}'

    def __repr__(self):
        return self.__str__()


class DiscreteGene(GeneType):
    def __init__(self, values):
        super().__init__(values)

    def get(self):
        return random.choice(self.values)


class ContinuousGene(GeneType):
    def __init__(self, values):
        super().__init__(values)

    def get(self):
        return self.values[0] + random.random() * (self.values[1] - self.values[0])


class CompositeGene(GeneType):
    def __init__(self, size, values):
        super().__init__(values)
        self.size = size

    def get(self):
        rng = self.values

        if type(rng) is tuple:
            return tuple([rng[0] + random.random() * (rng[1] - rng[0]) for _ in range(self.size)])

        return tuple([random.choice(rng) for _ in range(self.size)])

    def __str__(self):
        return super().__str__() + f' size: {self.size}'


class BaseChromosome(object):
    def __init__(self):
        for field in list(self.__dict__.keys()):
            if field.startswith('_'):
                self.__dict__[field.strip('_')] = self.__dict__[field].get()

    def crossover(self, other):
        raise NotImplementedError()

    def mutate(self):
        raise NotImplementedError()

    def get_field_names(self):
        return [field for field in self.__dict__ if not field.startswith('_')]

    def get_field_prototypes(self):
        return {field: self.__dict__[field] for field in self.__dict__ if field.startswith('_')}

    def copy_prototypes(self, new):
        for field, constraint in self.__dict__.items():
            if field.startswith('_'):
                new.__dict__[field] = constraint

    def copy_fields(self, new):
        for field, value in self.__dict__.items():
            if not field.startswith('_'):
                new.__dict__['_' + field] = value

    def copy(self, new):
        self.copy_fields(new)
        self.copy_prototypes(new)

    def __str__(self):
        res = '--Chromosome--\n'
        for field in self.__dict__:
            if not field.startswith('_'):
                res += field + ": " + str(getattr(self, field)) + '\n'

        return res


class ChromosomeClassFactory(object):
    def __init__(self, /, **constraints):
        self.constraints = []

        for constraint, values in constraints.items():
            if type(values) is list:
                constraint_data = DiscreteGene(values)

            elif type(values) is tuple:
                constraint_data = ContinuousGene(values)
            elif type(values) is dict:
                if set(values.keys()) == {'n', 'range'}:
                    if type(values['n']) is not int or values['n'] < 2:
                        raise TypeError('number of composite genes can be int >= 2 only')

                    if type(values['range']) not in {tuple, list}:
                        raise TypeError('range of composite genes can be only passed in list or tuple')

                    constraint_data = CompositeGene(values['n'], values['range'])
                else:
                    raise TypeError('Wrong composite type definition, only fields `n_values` & `datatype` are required')
            else:
                raise TypeError(f'Wrong constraint type: {type(values)} for parameter: {constraint}')

            self.constraints.append((constraint, constraint_data))

    def generate(self, chromosome: type):
        if type(chromosome) is not type:
            raise TypeError('`chromosome` argument must be of class `type`')
        if BaseChromosome not in chromosome.mro():
            raise TypeError('`chromosome` argument must be derived from BaseChromosome class')

        instance = chromosome()

        try:
            with open(os.devnull, "w") as f, contextlib.redirect_stdout(f):
                instance.crossover(None)
                instance.mutate()
        except NotImplementedError:
            raise NotImplementedError('You must implement crossover and mutate methods before creating chromosomes')
        except Exception:
            pass

        for field, constraint in self.constraints:
            instance.__dict__['_' + field] = constraint

        instance.__init__()
        return instance

    def __str__(self):
        res = ''
        for name, gene in self.constraints:
            res += f'{name}:\n'
            res += str(gene) + '\n\n'

        return res
