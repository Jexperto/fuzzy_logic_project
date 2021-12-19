import numpy as np
import skfuzzy as fuzz


class LinguisticVariable:
    def __init__(self, name, range):
        self.name = name
        self.range = range
        self.mfs = {}
        self.fuzzified_variable = {}
        self.crisp_value = -1

    def add_term(self, name, membership_function, *membership_func_args, **membership_func_kwargs):
        self.mfs[name] = membership_function(self.range, *membership_func_args, **membership_func_kwargs)

    def process_crisp_value(self, input_var):
        self.crisp_value = input_var
        for name, func in self.mfs.items():
            self.fuzzified_variable[name] = fuzz.interp_membership(self.range, func, input_var)


class BaseComparator:
    pass


class Is:
    def __init__(self, var, term):
        self.var = var
        self.term = term

    def get_degree(self, variables):
        return variables.get(self.var).fuzzified_variable[self.term]


class Or:
    def __init__(self, left, right):
        self.right = right
        self.left = left

    def get_degree(self, variables):
        return np.fmax(self.left.get_degree(variables), self.right.get_degree(variables))


class And:
    def __init__(self, left, right):
        self.right = right
        self.left = left

    def get_degree(self, variables):
        return np.fmin(self.left.get_degree(variables), self.right.get_degree(variables))


class Conclusion:
    def __init__(self, variable, term, weight=1.0):
        self.variable = variable
        self.term = term
        self.weight = weight


class Rule:
    def __init__(self, condition, conclusion):
        self.condition = condition
        self.conclusion = conclusion

    def set_conclusion(self, conclusion):
        self.conclusion = conclusion


def activate(variables, rules, func):
    activations = []
    for rule in rules:
        antecedent_evaluation = rule.condition.get_degree(variables)
        activations.append(func(antecedent_evaluation, variables[rule.conclusion.variable].mfs[rule.conclusion.term]))
    return activations


def aggregate(func, activations):
    first, *rest = activations
    if len(rest) == 1:
        return func(first, rest[0])
    return func(first, aggregate(func, rest))
