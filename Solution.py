from populations import Populations
from random import random
from random import randint
import random
class Solution:
    def __init__(self,p=Populations,number_nurses=0,days=0,generations=0):
        self.pop=p.get_populations()
        self.days=days
        self.generations=generations
        self.ld = int(number_nurses * (1 / 4))
        self.ln = int(number_nurses * (1 / 4))
        self.lm = int(number_nurses * (1 / 5))
        self.best_tabels = []
        self.best_fitness = []

    def atleast(self,day, night, midnight):
        pen2 = 0
        if day < self.ld or midnight < self.lm or night < self.ln:
            pen2 = -1
        return pen2

    def hard_constrain(self,popu):
        fit = []
        for tap in range(len(popu)):

            for d in range(len(popu[tap][0])):
                day = 0
                night = 0
                midnight = 0
                dayoff = 0
                for n in range(len(popu[tap])):
                    if popu[tap][n][d] == 1:
                        day += 1
                    elif popu[tap][n][d] == 3:
                        midnight += 1
                    elif popu[tap][n][d] == 2:
                        night += 1
                    elif popu[tap][n][d] == 0:
                        dayoff += 1
            fit.append(self.atleast(day, night, midnight))

        return fit

    def night_after_day(self,pop=[], fit=[]):
        for tap in range(len(pop) - 1):
            if fit[tap] == -1:
                continue
            else:
                for n in range(len(pop[tap])):
                    for d in range(0, self.days - 2):
                        if pop[tap][n][d] == 3 and pop[tap][n][d + 1] == 1:
                            fit[tap] += 1

    def no_repeat(selff,pop, fit):
        for index1 in range(len(pop)):
            if fit[index1] == -1:
                continue
            else:
                for index2 in range(len(pop[index1])):
                    index3 = 0
                    while index3 < len(pop[index1][index2]) - 2:
                        if pop[index1][index2][index3] == 0 and pop[index1][index2][index3 + 1] == 0 and \
                                pop[index1][index2][index3 + 2] == 0:
                            fit[index1] += 1
                            index3 += 1
                        else:
                            index3 += 1

    def holiday4(self,pop=[], fit=[]):
        for index1 in range(len(pop)):
            if fit[index1] == -1:
                continue
            else:
                for index2 in range(len(pop[index1])):
                    if pop[index1][index2].count(0) < 1:
                        fit[index1] += 1

    def selection(self,popu=[], fit=[]):
        i = 0
        while i < len(popu):
            if fit[i] == -1:
                popu.pop(i)
                fit.pop(i)
            else:
                i += 1

    def sort_fit_pop(self,fit=[], pop=[]):
        for index1 in range(len(pop) - 1):
            for index2 in range(len(pop) - 1):
                if fit[index2] > fit[index2 + 1]:
                    temp = fit[index2]
                    fit[index2] = fit[index2 + 1]
                    fit[index2 + 1] = temp
                    temp = pop[index2]
                    pop[index2] = pop[index2 + 1]
                    pop[index2 + 1] = temp

    def allFitneess(self,pop=[]):
        fit = self.hard_constrain(pop)
        print("fit before selection", len(fit))
        print("pop before selection", len(pop))
        self.night_after_day(pop, fit)
        self.no_repeat(pop, fit)
        self.holiday4(pop, fit)
        self.selection(pop, fit)
        self.sort_fit_pop(fit, pop)
        print("fit after selection", len(fit))
        print("pop after selection", len(pop))

        return fit

    def mutation(self,parent=[], fit=[]):
        print("parent in mutation len", len(parent))
        x1 = random.randint(0, len(parent) - 1)
        x2 = random.randint(0, len(parent) - 1)
        x3 = random.randint(0, len(parent) - 1)
        if x1 != x2:
            vec1 = parent[x1]
            vec2 = parent[x2]
            vec3 = parent[x3]
            fit_vec3 = fit[x3]
            fit_vec4 = 0
            vec4 = []
            for nurse in range(len(vec1)):
                temp = []
                for day in range(0, self.days):
                    temp.append(vec2[nurse][day] - vec1[nurse][day])
                vec4.append(temp)
            for nur in range(len(vec4)):
                for dy in range(0, self.days):
                    if vec4[nur][dy] < 0:
                        vec4[nur][dy] = vec4[nur][dy] * -1
            for nur in range(len(vec4)):
                for dy in range(0, self.days - 1):
                    if vec4[nur][dy] == 3 and vec4[nur][dy + 1] == 1:
                        fit_vec4 += 1
            for nur in range(len(vec4)):
                for dy in range(0, self.days - 2):
                    if vec4[nur][dy] == 0 and vec4[nur][dy + 1] == 0 and \
                            vec4[nur][dy + 2] == 0:
                        fit_vec4 += 1
            for nur in range(len(vec4)):
                for dy in range(0, self.days):
                    if vec4[nur].count(0) == 0:
                        fit_vec4 += 1

            if fit_vec3 < fit_vec4:
                parent[x3] = vec4
                fit[x3] = fit_vec4

    def evolve(self,mutate, select_random, select_best, pop=[], fit=[]):
        # select best
        select_best_length = int(len(pop) * select_best)
        parent = pop[:select_best_length]
        parents_fitness = fit[:select_best_length]
        # random select
        for random_child in pop[select_best_length:]:
            if select_random > random.random():
                index = pop.index(random_child)
                parent.append(random_child)
                parents_fitness.append(fit[index])
        # ----------mutation--------------------------------
        if len(parent) <= 1:
            return parent
        else:
            if mutate > random.random():
                self.mutation(parent, parents_fitness)
            parents_length = len(parent)

            desired_length = len(pop) - parents_length

            children = []
            # -------------------------Crossover---------------------------------
            while len(children) < desired_length:
                male = random.randint(0, parents_length - 1)
                female = random.randint(0, parents_length - 1)
                if male != female:
                    male = parent[male]
                    female = parent[female]
                    half = round(len(male) / 4)
                    child = male[:half] + female[half:]
                    children.append(child)
            for item in children:
                parent.append(item)
        return parent

    def find_best_solution(self):
        pop=self.pop
        for t in range(0, self.generations - 1):
            if len(pop) <= 1:
                break
            else:
                fitness = self.allFitneess(pop)
                parents = self.evolve(0.6, 0.3, 0.2, pop, fitness)
                if len(parents) <= 1:
                    self.best_fitness.append(fitness[0])
                    self.best_tabels.append(pop[0])
                    return
                else:
                    fitness = self.allFitneess(pop)
                    pop = parents

                    if len(fitness) <= 0:
                        return
                    else:
                        self.best_fitness.append(fitness[0])
                        self.best_tabels.append(pop[0])

    def get_solution(self):
        return_index = self.best_fitness.index(min(self.best_fitness))
        solution = self.best_tabels[return_index]
        return solution

    def displaytTable(self):
        table=self.get_solution()
        data = ""
        data += "NURSES\t\t" + "  DAY 1\t" + "  DAY 2\t" + "  DAY 3\t" + "  DAY 4\t" + "  DAY 5\t" + "  DAY 6\t" + "  DAY 7" + "\n" + "---------------------------------------------------------------------------------------------------\n"



        for nurse in range(len(table)):
            data += f"Nurse {nurse + 1} " + "\t|    "

            for day in range(0, self.days):
                if table[nurse][day] == 1:
                    data += "D" + "\t|    "
                if table[nurse][day] == 2:
                    data += "N" + "\t|    "
                if table[nurse][day] == 3:
                    data += "M" + "\t|    "
                if table[nurse][day] == 0:
                    data += "H" + "\t|    "
            data += "\n"
        return data

    def save_data_in_file(self,nameFile="",data=""):
        python_file = open(nameFile+".txt", "w")

        python_file.write(data)
        python_file.close()