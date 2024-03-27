import os
import contextlib
from Evolution.Genes import *


class BaseChromosome(object):
    def __init__(self):
        for field in self:
            if field.startswith('_'):
                self[field].value = self[field].get()

    def crossover(self, other):
        raise NotImplementedError()

    def mutate(self):
        raise NotImplementedError()

    def copy(self, new):
        for field, constraint in self.__dict__.items():
            if field.startswith('_'):
                new.__dict__[field] = constraint.copy()

    def __getitem__(self, item):
        return self.__getattr__(item)

    def __setitem__(self, key, value):
        self.__setattr__(key, value)

    def __getattr__(self, item: str):
        if item.startswith('_'):
            return self.__dict__[item]

        return self.__dict__['_' + item].value

    def __setattr__(self, key, value):
        if key.startswith('_'):
            self.__dict__[key] = value
            return

        self.__dict__['_' + key].value = value

    def __iter__(self):
        res = []
        for field in self.__dict__:
            if field.startswith('_'):
                res.append(field)
        return iter(res)

    def __str__(self):
        res = '--Chromosome--\n'
        for field in self.__dict__:
            if field.startswith('_') and isinstance(self.__dict__[field], GeneType):
                res += field.strip('_') + ": " + str(getattr(self, field).value) + '\n'

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
                    if type(values['n']) is not list:
                        raise TypeError('number of composite genes passes as list')
                    if len(values['n']) < 2:
                        raise ValueError('number of composite genes should be >= 2')
                    if not isinstance(values['n'][0], int):
                        raise TypeError('possible sizes must be integers')

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
            instance.__dict__['_' + field] = constraint.copy()

        instance.__init__()
        return instance

    def __str__(self):
        res = ''
        for name, gene in self.constraints:
            res += f'{name}:\n'
            res += str(gene) + '\n\n'

        return res
