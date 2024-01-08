import os
import sys
import timeit
import math
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

from shunting_yard.shunting_yard import shunting_yard
from shunting_yard.rpn import compute_rpn
import numpy as np
from random import random, randint, sample

print(shunting_yard("x^2 + 2*x + 1", variable="x"))


class Solver:
    def __init__(self, equation=None, min_range = -1e5, max_range = 1e5):
        self.min_range = min_range
        self.max_range = max_range
        self.equation = equation
        if not self.equation:
            exit(0)
    
        self.mutation_rate = 0.2
        self.elite = True
        self.elite_group = 32
        self.random_group = 8
        
        self.population = 200
        self.genome_length = 32

        self.current_gen = []
        self.next_gen = []
        self.fitness = []
        self.counter = 0
        
        # selecting the best child from a group of random_group
    def random_selection(self):
        random_child = sample(range(len(self.current_gen)), self.random_group)
        child_fitness = [self.fitness[g] for g in random_child]
        
        return self.current_gen[random_child[np.argmax(child_fitness)]]


        # cross overing some of the genes by a random cut
    def cross_over(self, genome_1, genome_2):  
        random_slice = randint(1, self.genome_length - 1)
        genome_1_child = genome_1[:random_slice] + genome_2[random_slice:]
        genome_2_child = genome_2[:random_slice] + genome_1[random_slice:]
            
        return genome_1_child, genome_2_child

        # mutating a random bit of a given genome by a crossing rate
    def mutate(self, genome):
        genome = list(genome)
        for g in range(len(genome)):
            if random() < self.mutation_rate:
                genome[g] = str((int(genome[g]) + 1) % 2)
                
        return "".join(genome)

       # transfer the best x childs of the previous generation to the next, x = elitism_group
    def elite_func(self):
        # global fitness, current_gen, next_gen
        best_childs = np.argsort(self.fitness)[-self.elite_group:]
        indx = self.elite_group - 1
        for i in best_childs:
            if len(self.next_gen) < self.elite_group:
                self.next_gen.append(self.current_gen[i])
            else:
                indx -= 1
                self.next_gen[indx] = self.current_gen[i]
                self.next_gen[self.population - self.elite_group + indx] = self.mutate(self.current_gen[i])
        for p in range(self.elite_group - 1):
            for g in range(p + 1, self.elite_group):
                try:
                    if abs(self.binary32_to_float(self.next_gen[p]) - self.binary32_to_float(self.next_gen[g])) < 0.05:
                        self.next_gen[g] =self.create_rand_genome()
                except OverflowError:
                       pass
                   

    # evaluating the fitness/accuracy of a given genome
    def fitness_evaluate(self, genome):
        try:
            self.counter += 1
            input_num = self.binary32_to_float(genome)
            eq = self.equation.replace('x', format(input_num, '.5f'))
            
            distance = abs(compute_rpn(shunting_yard(eq))  - 0)

            if  math.isnan(distance) or input_num > self.max_range or input_num < self.min_range:
                return 0
        
            return 1/ (1 + distance)
        except Exception:
            return 0
    
    
    # return the value of the left hand side 
    def y_return(self, x):
        return compute_rpn(shunting_yard(self.equation.replace('x', format(x, '.5f'))))
        
        
    # creating a new generation
    def create_new_gen(self):
        # global current_gen, next_gen
        if not self.elite:           
            if len(self.next_gen) == 0:
                for pop in range(int(self.population / 2)):
                    child_1, child_2 = self.cross_over(self.random_selection(), self.random_selection())
                    child_1, child_2 = self.mutate(child_1), self.mutate(child_2)
                    self.next_gen.append(child_1)
                    self.next_gen.append(child_2)
            else:
                for pop in range(int(self.population / 2)):
                    child_1, child_2 = self.cross_over(self.random_selection(), self.random_selection())
                    child_1, child_2 = self.mutate(child_1)
                    self.next_gen[pop * 2] = child_1
                    self.next_gen[pop * 2 + 1] = child_2
        else:
            # elitism function
            self.elite_func()
            if len(self.next_gen) == self.elite_group:
                for pop in range(int(self.elite_group/2), int(self.population / 2)):
                    child_1, child_2 = self.cross_over(
                        self.random_selection(), self.random_selection())
                    child_1, child_2 = self.mutate(
                        child_1), self.mutate(child_2)
                    self.next_gen.append(child_1)
                    self.next_gen.append(child_2)
            else:
                for pop in range(self.elite_group, int(self.population / 2)):
                    child_1, child_2 = self.cross_over(
                        self.random_selection(), self.random_selection())
                    child_1, child_2 = self.mutate(
                        child_1), self.mutate(child_2)
                    self.next_gen[pop * 2 - self.elite_group] = child_1
                    self.next_gen[pop * 2 + 1 - self.elite_group] = child_2

        self.current_gen = self.next_gen.copy()


        # updating the fitness
    def fitness_update(self):
        if len(self.fitness) == 0:
            for pop in range(self.population):
                self.fitness.append(self.fitness_evaluate(self.current_gen[pop]))
        else:
            for pop in range(self.population):
                self.fitness[pop] = self.fitness_evaluate(self.current_gen[pop])


       # creating generation 0 with random childs
    def create_gen_0(self):
        for pop in range(self.population):
            self.current_gen.append(self.create_rand_genome())


        # create random genome of length: genome_length=32
    def create_rand_genome(self):
        out = ''
        for g in range(self.genome_length):
            rand_num = randint(0, 1)
            out += str(rand_num)
            
        return out


    def binary32_to_float(self, binary_str):
        sign_bit = int( binary_str[0])
        exponent_bits = binary_str[1:9]
        fraction_bits = binary_str[9:]
        
        exponent = int(exponent_bits, 2) - 127
        fraction = 1 + sum(int(bit) * 2**(-i)
                               for i, bit in enumerate(fraction_bits, start=1))
        value = (-1) ** sign_bit * 2 ** exponent * fraction
        
        return value
          
            
    # solve equation
    def solve(self):
        x_result, y_result = [], []
        fitness = []
        
        self.create_gen_0()
        self.fitness_update()              
        self.create_new_gen()
        startTime = timeit.default_timer()
        while True: 
            self.fitness_update()
            best_index = np.argsort(self.fitness)[-1]
            best_binary = self.current_gen[best_index] 
            best_result = self.binary32_to_float(best_binary)
            if abs(best_result) < 1e-5:
                best_result = 0
            
            x_result.append(best_result)
            y_result.append(self.y_return(best_result))
            fitness.append(self.fitness[best_index])
            
            print('Result: ', best_result, '  ', \
                          'y: ', self.y_return(best_result), ' ',  'Fitness: ', self.fitness[best_index])
            self.create_new_gen()

            execution_time = timeit.default_timer() - startTime
            
            if (len(x_result) >= 2) and (len(fitness) >= 2) and (abs(x_result[-1] - x_result[-2]) <= 1e-9) and (fitness[-1] > 0.999) or execution_time > 10:
                print('%.3f'% (execution_time*1000) + 'ms')
                break
            
        if execution_time > 10:
            x_result = ["No solution!"]

        if x_result[0] != "No solution!":
            if abs(x_result[-1]) < 1e-6:
                x_result[-1] = 0
        
        return x_result, y_result, fitness, str('%.3f' % (execution_time*1000)) + 'ms'
