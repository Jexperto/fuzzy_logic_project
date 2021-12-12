import numpy as np
import skfuzzy as fuzz
from matplotlib import pyplot as plt


class LinguisticVariable:
    def __init__(self, name, range):
        self.name = name
        self.range = range
        self.mfs = {}
        self.fuzzified_variable = {}

    def add_term(self, name, membership_function, *membership_func_args, **membership_func_kwargs):
        self.mfs[name] = membership_function(self.range, *membership_func_args, **membership_func_kwargs)

    def process_crisp_value(self, input_var):
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


variables = {}

food = LinguisticVariable("food", np.arange(0, 10.01, 0.5))
service = LinguisticVariable("service", np.arange(0, 10.01, 0.5))
tip = LinguisticVariable("tip", np.arange(0, 25.01, 1.0))

variables[food.name] = food
variables[service.name] = service
variables[tip.name] = tip

service.add_term("bad", fuzz.trimf, [0, 0, 5])
service.add_term("medium", fuzz.trimf, [0, 5, 10])
service.add_term("good", fuzz.trimf, [5, 10, 10])

food.add_term("bad", fuzz.zmf, 0, 5)
food.add_term("medium", fuzz.pimf, 0, 4, 5, 10)
food.add_term("good", fuzz.smf, 5, 10)

tip.add_term("low", fuzz.trimf, [0, 0, 13])
tip.add_term("middle", fuzz.trimf, [0, 13, 25])
tip.add_term("high", fuzz.trimf, [13, 25, 25])

food.process_crisp_value(4.0)
service.process_crisp_value(9.5)

a = Rule(Or(Is("service", "bad"), Is("food", "bad")), Conclusion("tip", "low"))
b = Rule(Is("service", "medium"), Conclusion("tip", "middle"))
c = Rule(Or(Is("service", "good"), Is("food", "good")), Conclusion("tip", "high"))

ruleset = [a, b, c]

oggr = aggregate(np.fmax, activate(variables, ruleset, np.fmin))
print(f"Oggregation: {oggr}")

centroid = fuzz.defuzz(tip.range, oggr, 'centroid')

print(centroid)
