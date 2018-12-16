import numpy as np
from math import sqrt
from copy import deepcopy
from random import uniform
import matplotlib.pyplot as plt

class Point:
    __centroid = 0
    def __init__(self, x, y, label):
        self.x = x
        self.y = y
        self.label = label
    def setCentroid(self, centroid):
        self.__centroid = centroid
    def getCentroid(self):
        return self.__centroid

def sum_error(inPoint, k, random):
    n = 0
    for item in inPoint:
        n += 1
    print(n)

    sum_tot = 0
    for i in range(0, k):
        sum = 0
        tot_data = 0
        for item in inPoint:
            if item.getCentroid() == i:
                sum += sqrt((item.x - random[0, i])**2 + (item.y - random[1, i])**2)
                tot_data += 1
        sum_tot += sum / tot_data

    sse = sum_tot / n
    print("Error ratio " + str(sse))

def drawGraph(inPoint, random, k):
    col = ['red', 'green', 'blue', 'yellow', 'magenta', 'cyan']
    for i in range(0, k):
        x = []
        y = []
        for item in inPoint:
            if (item.getCentroid() == i):
                x.append(item.x)
                y.append(item.y)
        # plt.scatter(x, y, color=np.random.randint(2, size=(1, 3)))
        plt.scatter(x, y, color=col[i])

    # -------------------------------

    # x = []
    # y = []
    #
    # for item in inPoint:
    #     x.append(item.x)
    #     y.append(item.y)
    #
    # plt.scatter(x, y, color=(0, 1, 0))

    # for i in range(0, k):
    #     plt.scatter(random[0,i], random[1,i])

    # -------------------------------

    plt.scatter(random[0], random[1], color='black', marker='x')

    plt.xlim(0, 140)
    plt.ylim(0, 180)
    plt.show()

def doElitism(inPoint, random, temp):
    new_random = deepcopy(temp)
    fitness = searchJmin(inPoint, random)
    # print("elitism : " + str(fitness))

    for i in range(0, int(len(random) / 2)):
        new_random[i] = random[fitness[i][1]]
    
    return new_random

def doMutation(random):
    for rand in random:
        probMut = 0.9
        p = uniform(0.0, 1.0)
        
        if p < probMut:
            r = int(uniform(0, len(rand)))
            epsilon = uniform(-1.0, 1.0)
            rand[r] += epsilon
    
    return random

def doCrossOver(random):
    for i in range(0, len(random)):
        if i % 2 != 0:
            continue
        else:
            # parent1 = random[i]
            # parent2 = random[i+1]
            
            probCO = 0.9
            p = uniform(0.0, 1.0)

            if p < probCO:
                leftBorder = int(uniform(0, len(random[i]) - 1))
                rightBorder = int(uniform(leftBorder + 1, len(random[i])))

                r = 0.4
                for j in range(leftBorder, rightBorder):
                    a = random[i][j]
                    b = random[i+1][j]
                    random[i][j] = r * a + (1 - r) * b
                    random[i+1][j] = r * b + (1 - r) * a
    return random

def doRoulette(fitness, inPoint):
    max = sum(fit[0] for fit in fitness)
    current = 0
    pick = uniform(0.0, max)
    for fit in fitness:
        current += fit[0]
        if current > pick:
            return fit

def searchJmin(inPoint, random):
    distance_tot = []
    x = 0
    for rand in random:
        distance = 0.0
        for item in inPoint:
            min = 1000000.0
            for i in range(0, len(rand)):
                if i % 2 != 0:
                    continue
                else:
                    distance_point = sqrt((rand[i] - item.x )**2 + (rand[i+1] - item.y)**2)
                    if distance_point < min:
                        # idx_min = i
                        min = distance_point
            # item.setCentroid(idx_min)
            distance += min
        distance_tot.append([distance, x])
        x += 1
    distance_tot.sort()
    return distance_tot

def read_file():
    with open("data/ruspini.txt") as f:
        data = [[int(num) for num in line.split(",")] for line in f]
    return data

def main():
    # MARK -> Read Ruspini File
    data = read_file()
    inPoint = []
    for item in data:
        inPoint.append(Point(item[0], item[1], item[2]))

    # MARK -> Input Centroid, Individu, and Loop
    n = int(input("Masukkan Jumlah Centroid : "))
    individu = int(input("Masukkan Jumlah Individu : "))
    loop = int(input("Masukkan Jumlah Loop : "))

    # MARK -> Random Data
    random = np.random.uniform(20.0, 140.0, [individu, n*2])
    
    # MARK -> Do Genetic Algorithm
    for i in range(0, loop):
        temp = deepcopy(random)
        
        # MARK -> Search Fitness 
        fitness = searchJmin(inPoint, random)
        print()
        print("J Min Data ke-" + str(i) + " \t: " + str(fitness[0][0]))

        # MARK -> Do Roulette Wheel
        for j in range(0, individu):
            result = doRoulette(fitness, inPoint)
            random[j] = temp[result[1]]
        
        # MARK -> Do Cross Over
        random = doCrossOver(random)

        # MARK -> Do Mutation
        random = doMutation(random)

        # MARK -> Do Elitism
        random = np.vstack((random, temp))
        random = doElitism(inPoint, random, temp)
    
    new_random = random[0]
    print(new_random)
    random = np.random.uniform(50.0, 110.0, [2, n])
    x = 0
    for i in range(0, 2):
        for j in range(0, n):
            random[i][j] = new_random[x]
            x += 2
        x = 1
    print(random)

    drawGraph(inPoint, random, n)
    temp = deepcopy(random)

    # MARK -> Do Clustering
    error = 1000000
    n_data = 0
    while error > 0.0001:
        error = 0.0
        for item in inPoint:
            n_data += 1
            min = 100000000.
            # distance = []
            for i in range(0, n):
                distance_point = sqrt((random.item(0, i) - item.x)**2 + (random.item(1, i) - item.y)**2)
                if distance_point < min:
                    idx_min = i
                    min = distance_point
            item.setCentroid(idx_min)


        for i in range(0, n):
            sum_x = 0
            sum_y = 0
            sum_i = 0
            for item in inPoint:
                if (int(item.getCentroid()) == i):
                    sum_x += item.x
                    sum_y += item.y
                    sum_i += 1
            try:
                x = sum_x / sum_i
                y = sum_y / sum_i
            except:
                x = 0
                y = 0

            if (x != 0 or y != 0):
                random[0, i] = x
                random[1, i] = y

            error += abs(temp[0, i] - x)
            error += abs(temp[1, i] - y)
            # print("temp : " + str(temp[0, i]) + " , x :  " + str(x))
        print()
        print(random)
        temp = deepcopy(random)
        print("error : " + str(error))
        drawGraph(inPoint, random, n)
    sum_error(inPoint, n, random)

if __name__ == "__main__":
    main()
    