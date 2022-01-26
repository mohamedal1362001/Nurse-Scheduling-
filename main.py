from random import random
from random import randint
import random
# -----------------------------------------
days = 7
N = 50
ld =int(N*(1/4))
ln = int(N*(1/4))
lm = int(N*(1/5))
generations = 1000
#------------------------------------------

count =1000
populations = []
fitness = []
pen = 0
#1************************
def dis(t=[]):
    for table in range(len(t)):
        print(f"*************Solution{table}*****************")
        for nurse in range(len(t[table])):
            print("Nurse", nurse, "  ", t[table][nurse], "\n")
#2***********************
def func(n, end, start=0):
        return list(range(start, n)) + list(range(n + 1, end))
#----------------------------------------------------------------------
def indvidiual(n, d):
    table = []
    for i in range(n):
        l = []
        for x in range(d):
            if not l:
                l.append(random.randint(0, 3))
            elif l[x - 1] == 3:
                r = func(1, 4)
                l.append(random.choice(r))
            else:
                l.append(random.randint(0, 3))
        table.append(l)
    return table
# 3***********************
def population(c, n, d):
    pop = []
    for i in range(c):
        pop.append(indvidiual(n, d))
    return pop
# 4***********************
def atleast(day, night, midnight):
    pen2 = 0
    if    day < ld or  midnight < lm   or night < ln  :
        pen2 = -1
    return pen2

# -------------------------------------------------------------------#
def hard_constrain(popu):
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
        fit.append(atleast(day,night,midnight))

    return fit
# 5****************************
def night_after_day(pop=[], fit=[]):
    for tap in range(len(pop)-1):
        if fit[tap] == -1:
            continue
        else:
            for n in range(len(pop[tap])):
                for d in range(0, days-2):
                    if pop[tap][n][d] == 3 and pop[tap][n][d + 1] == 1:
                        fit[tap] += 1
# 6****************************
def no_repeat(pop, fit):
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
# 7***************************
def holiday4(pop=[], fit=[]):
    for index1 in range(len(pop)):
        if fit[index1] == -1:
            continue
        else:
            for index2 in range(len(pop[index1])):
                if pop[index1][index2].count(0) < 1:
                    fit[index1] += 1
# 8***************************
def selection(popu=[], fit=[]):
    i = 0
    while i < len(popu):
        if fit[i] == -1:
            popu.pop(i)
            fit.pop(i)
        else:
            i += 1
# --------------------------------------------
def sort_fit_pop(fit=[], pop=[]):
    for index1 in range(len(pop) - 1):
        for index2 in range(len(pop) - 1):
            if fit[index2] > fit[index2 + 1]:
                temp = fit[index2]
                fit[index2] = fit[index2 + 1]
                fit[index2 + 1] = temp
                temp = pop[index2]
                pop[index2] = pop[index2 + 1]
                pop[index2 + 1] = temp
#----------------------------------------------------------------------------------
def allFitneess(pop=[]):
    fit = hard_constrain(pop)
    print("fit before selection", len(fit))
    print("pop before selection", len(pop))
    night_after_day(pop, fit)
    no_repeat(pop, fit)
    holiday4(pop, fit)
    selection(pop, fit)
    sort_fit_pop(fit, pop)
    print("fit after selection", len(fit))
    print("pop after selection", len(pop))

    return fit
#*---------------------------------------------------------------------------
def evolve(mutate,select_random,select_best,pop=[],fit=[]):
    #select best
    select_best_length=int(len(pop)*select_best)
    parent = pop[:select_best_length]
    parents_fitness=fit[:select_best_length]
    #random select
    for random_child in pop[select_best_length:]:
        if select_random > random.random():
            index = pop.index(random_child)
            parent.append(random_child)
            parents_fitness.append(fit[index])
    #----------mutation--------------------------------
    if len(parent)<=1:
        return parent
    else:
        if mutate > random.random():
            mutation(parent,parents_fitness)
        parents_length = len(parent)

        desired_length = len(pop)-parents_length

        children = []
        #-------------------------Crossover---------------------------------
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

def mutation (parent=[],fit=[]):
    print("parent in mutation len", len(parent))
    x1=random.randint(0,len(parent)-1)
    x2=random.randint(0,len(parent)-1)
    x3=random.randint(0,len(parent)-1)
    if x1!=x2 :
        vec1 = parent[x1]
        vec2 = parent[x2]
        vec3 = parent[x3]
        fit_vec3=fit[x3]
        fit_vec4=0
        vec4= []
        for nurse in range(len(vec1)):
            temp = []
            for day in range(0,days):
                temp.append(vec2[nurse][day]-vec1[nurse][day])
            vec4.append(temp)
        for nur in range(len(vec4)):
            for dy in range(0,days):
                if vec4[nur][dy]<0:
                    vec4[nur][dy]=vec4[nur][dy]*-1
        for nur in range(len(vec4)):
            for dy in range(0,days-1):
                if vec4[nur][dy] == 3 and vec4[nur][dy + 1] == 1:
                    fit_vec4 += 1
        for nur in range(len(vec4)):
            for dy in range(0, days-2):
                if vec4[nur][dy] == 0 and vec4[nur][dy + 1] == 0 and \
                        vec4[nur][dy + 2] == 0:
                    fit_vec4 += 1
        for nur in range(len(vec4)):
            for dy in range(0, days):
                if vec4[nur].count(0) == 0:
                    fit_vec4 += 1

        if fit_vec3<fit_vec4:
            parent[x3]=vec4
            fit[x3]=fit_vec4


#--------------------------------------main------------
best_tabels = []
best_fitness = []
def main_function():
    populations = population(count, N, days)
    for t in range(0,generations-1):
        if len(populations) <=1:
            break
        else:
            fitness = allFitneess(populations)
            parents = evolve(0.6, 0.3, 0.2, populations, fitness)
            if len(parents) <=1 :
                best_fitness.append(fitness[0])
                best_tabels.append(populations[0])
                return
            else:
                fitness = allFitneess(populations)
                populations = parents

                if len(fitness)<= 0 :
                    return
                else:
                    best_fitness.append(fitness[0])
                    best_tabels.append(populations[0])
#--------------------------------------------------------------------------------
def table(table):
    shifts=N*31
    data=""
    data+="NURSES\t      "+"   DAY 1  "+"    DAY 2  "+"    DAY 3  "+"    DAY 4   "+"     DAY 5    "+"    DAY 6   "+"     DAY 7  "+"\n"+"---------------------------------------------------------------------------------------------------\n"



    print("NURSES\t      "," DAY 1  ","  DAY 2  ","    DAY 3  ","    DAY 4  ","    DAY 5  ","    DAY 6  ","    DAY 7  ")
    print("-----------------------------------------------------------------------------------------------------------------------------------------\n")
    for nurse in range(len(table)):
        data+=f"Nurse {nurse+1} "+"\t|    "
        print(f"Nurse {nurse+1} ",end="\t|    ")
        for day in range(0,days):
            if table[nurse][day]==1:
                data+="D"+"\t  |    "
                print("D",end="\t  |    ")
            if table[nurse][day] == 2:
                data+="N"+ "\t  |    "
                print("N", end="\t  |    ")
            if table[nurse][day] == 3:
                data+="M"+"\t  |    "
                print("M", end="\t  |    ")
            if table[nurse][day] == 0:
                data+="H"+"\t  |    "
                print("H", end="\t  |    ")
        data+="\n"
        print("\n")
    print("datat\n")
    print(data)
#-------------------------------------------------------------------------------
main_function()

return_index =best_fitness.index(min(best_fitness))
solution = best_tabels[return_index]
print("wrong",best_fitness[return_index])
table(solution)