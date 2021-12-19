from fuzzy import *
from plots import plot_memberships, plot_aggregations
from matplotlib import pyplot as plt


def bell(array, a, b, c):
    return 1 / (1 + abs((array - c) / a) ** (2 * b))


variables = {}

# input variables
pulse = LinguisticVariable("пульс", np.arange(0, 210.01, 0.5))
activity = LinguisticVariable("дл_акт", np.arange(0, 125.01, 0.5))
blood = LinguisticVariable("насыщ_кисл", np.arange(70, 100.5, .1))
feeling = LinguisticVariable("самочувствие", np.arange(0, 10.01, .1))

# output variables
intensity = LinguisticVariable("интенсивность", np.arange(0, 10.01, .1))
rest = LinguisticVariable("отдых", np.arange(0, 470.01, 0.1))
wb = LinguisticVariable("сост_организма", np.arange(0, 10.01, 0.1))

variables[pulse.name] = pulse
variables[activity.name] = activity
variables[blood.name] = blood
variables[feeling.name] = feeling
variables[intensity.name] = intensity
variables[rest.name] = rest
variables[wb.name] = wb

pulse.add_term("низкий", fuzz.zmf, 20, 70)
pulse.add_term("нормальный", fuzz.pimf, 45, 70, 90, 120)
pulse.add_term("высокий", fuzz.pimf, 90, 120, 130, 170)
pulse.add_term("оч_высокий", fuzz.smf, 140, 200)

activity.add_term("короткая", fuzz.trapmf, [0, 0, 15, 25])
activity.add_term("средняя", fuzz.trapmf, [20, 25, 35, 40])
activity.add_term("длинная", fuzz.trapmf, [30, 40, 65, 80])
activity.add_term("сл_длинная", fuzz.trapmf, [60, 100, 180, 180])

blood.add_term("критическое", fuzz.zmf, 70, 90)
blood.add_term("низкое", fuzz.pimf, 86, 89, 92, 95)
blood.add_term("нормальное", fuzz.smf, 93, 100)

feeling.add_term("оч_плохое", bell, 1.5, 2, 1.5)
feeling.add_term("плохое", bell, 1.5, 2, 3.5)
feeling.add_term("хорошее", bell, 1.5, 2, 5.5)
feeling.add_term("оч_хорошее", bell, 1.5, 2, 7.5)
feeling.add_term("великолепное", bell, 1.5, 2, 9.5)

intensity.add_term("низкая", bell, 1, 2, 1.5)
intensity.add_term("средняя", bell, 1, 2, 3.5)
intensity.add_term("высокая", bell, 1.2, 2, 6)
intensity.add_term("оч_высокая", bell, 1., 2, 8.5)

rest.add_term("короткое", fuzz.zmf, 20, 70)
rest.add_term("среднее", fuzz.pimf, 45, 95, 110, 180)
rest.add_term("длинное", fuzz.pimf, 120, 200, 240, 300)
rest.add_term("оч_длинное", fuzz.smf, 250, 450)

wb.add_term("оч_плохое", bell, 1, 2, 1.5)
wb.add_term("плохое", bell, 1, 2, 3.5)
wb.add_term("среднее", bell, 1.2, 2, 6)
wb.add_term("хорошее", bell, 1., 2, 8.5)

intensity_ruleset = [
    Rule(Is("пульс", "низкий"), Conclusion("интенсивность", "низкая")),
    Rule(And(Is("пульс", "нормальный"), Is("дл_акт", "короткая")), Conclusion("интенсивность", "средняя")),
    Rule(And(Is("пульс", "нормальный"), Is("дл_акт", "средняя")), Conclusion("интенсивность", "средняя")),
    Rule(And(Is("пульс", "нормальный"), Is("дл_акт", "длинная")), Conclusion("интенсивность", "низкая")),
    Rule(And(Is("пульс", "нормальный"), Is("дл_акт", "сл_длинная")), Conclusion("интенсивность", "низкая")),
    Rule(And(Is("пульс", "высокий"), Is("дл_акт", "короткая")), Conclusion("интенсивность", "оч_высокая")),
    Rule(And(Is("пульс", "высокий"), Is("дл_акт", "средняя")), Conclusion("интенсивность", "высокая")),
    Rule(And(Is("пульс", "высокий"), Is("дл_акт", "длинная")), Conclusion("интенсивность", "средняя")),
    Rule(And(Is("пульс", "высокий"), Is("дл_акт", "сл_длинная")), Conclusion("интенсивность", "высокая")),
    Rule(Is("пульс", "оч_высокий"), Conclusion("интенсивность", "оч_высокая")),
]
rest_ruleset = [
    Rule(And(Is("пульс", "нормальный"), Is("насыщ_кисл", "нормальное")), Conclusion("отдых", "короткое")),
    Rule(And(Is("пульс", "низкий"), Is("насыщ_кисл", "низкое")), Conclusion("отдых", "оч_длинное")),
    Rule(And(Is("пульс", "низкий"), Is("насыщ_кисл", "критическое")), Conclusion("отдых", "оч_длинное")),
    Rule(And(Is("пульс", "низкий"), Is("насыщ_кисл", "критическое")), Conclusion("отдых", "оч_длинное")),
    Rule(And(And(Is("пульс", "высокий"), Is("насыщ_кисл", "нормальное")), Is("дл_акт", "длинная")), Conclusion("отдых", "среднее")),
    Rule(And(And(Is("пульс", "высокий"), Is("насыщ_кисл", "нормальное")), Is("дл_акт", "сл_длинная")),
         Conclusion("отдых", "длинное")),
    Rule(And(Is("пульс", "оч_высокий"), Is("насыщ_кисл", "нормальное")), Conclusion("отдых", "длинное")),
    Rule(And(Is("пульс", "оч_высокий"), Is("насыщ_кисл", "низкое")), Conclusion("отдых", "оч_длинное")),
    Rule(And(Is("дл_акт", "короткая"), Is("насыщ_кисл", "нормальное")), Conclusion("отдых", "короткое")),
    Rule(And(Is("дл_акт", "средняя"), Is("насыщ_кисл", "нормальное")), Conclusion("отдых", "короткое")),
]
wb_ruleset = [
    Rule(Is("пульс", "оч_высокий"), Conclusion("сост_организма", "плохое")),
    Rule(Is("насыщ_кисл", "критическое"), Conclusion("сост_организма", "оч_плохое")),
    Rule(Is("насыщ_кисл", "низкое"), Conclusion("сост_организма", "плохое")),
    Rule(And(Is("пульс", "высокий"), Is("дл_акт", "длинная")), Conclusion("сост_организма", "среднее")),
    Rule(And(Is("пульс", "оч_высокий"), Is("дл_акт", "длинная")), Conclusion("сост_организма", "плохое")),
    Rule(And(And(Is("пульс", "нормальный"), Is("насыщ_кисл", "нормальное")),
             Or(Is("самочувствие", "великолепное"), Or(Is("самочувствие", "оч_хорошее"), Is("самочувствие", "хорошее")))),
         Conclusion("сост_организма", "хорошее")),
    Rule(And(And(Is("пульс", "нормальный"), Is("насыщ_кисл", "нормальное")), Is("самочувствие", "плохое")), Conclusion("сост_организма", "среднее")),
    Rule(And(Is("пульс", "высокий"), Is("насыщ_кисл", "нормальное")), Conclusion("сост_организма", "среднее")),
    Rule(And(Is("пульс", "оч_высокий"), Is("насыщ_кисл", "нормальное")), Conclusion("сост_организма", "плохое")),
    Rule(Is("самочувствие", "оч_плохое"), Conclusion("сост_организма", "плохое")),
    Rule(Is("пульс", "низкий"), Conclusion("сост_организма", "плохое")),
]

pulse.process_crisp_value(float(input("Введите пульс: ")))
activity.process_crisp_value(float(input("Введите длительность активности (сек): ")))
blood.process_crisp_value(float(input("Введите уровень насыщения крови кислородом (%): ")))
feeling.process_crisp_value(float(input("Введите самочувствие: ")))

plot_memberships(variables.values())
plt.savefig("mfs.png")

aggr1 = aggregate(np.fmax, activate(variables, intensity_ruleset, np.fmin))
aggr2 = aggregate(np.fmax, activate(variables, rest_ruleset, np.fmin))
aggr3 = aggregate(np.fmax, activate(variables, wb_ruleset, np.fmin))

plot_aggregations({"интенсивность": aggr1, "отдых": aggr2, "сост_организма": aggr3},
                  {"интенсивность": intensity.range, "отдых": rest.range, "сост_организма": wb.range})
plt.savefig("aggrs.png")

centroid1 = fuzz.defuzz(intensity.range, aggr1, 'centroid')
centroid2 = fuzz.defuzz(rest.range, aggr2, 'centroid')
centroid3 = fuzz.defuzz(wb.range, aggr3, 'centroid')

print(f"Интенсивность - {centroid1}")
print(f"Время отдыха - {centroid2} сек")
print(f"Состояние организма - {centroid3} из 10")
