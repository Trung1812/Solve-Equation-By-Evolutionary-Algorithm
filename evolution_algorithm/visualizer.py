
import matplotlib.pyplot as plt
import pylab
import os
import sys
from pathlib import Path
from solver import Solver

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)

class Visualize:

    @staticmethod
    def plot_result(x_result, y_result):
        title_font = {'fontname': 'Consolas', 'size': 9, 'color': '#035B96'}
        tick_font = {'fontname': 'Consolas', 'size': 8, 'color': '#035B96'}
        

        save_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        save_folder = r"assets/viz"
        save_path = os.path.abspath(os.path.join(save_dir, save_folder))
        if os.path.exists(save_path) == False:
            os.makedirs(save_path)

        width, height = 369, 276
        dpi = 100

        # Plot for x
        plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)

        plt.plot([i for i in range(1, len(x_result) + 1)], x_result)
        plt.title('The values of \'x\' in each generation', title_font)

        plt.xticks(**tick_font)
        plt.yticks(**tick_font)
        plt.savefig(os.path.join(save_path, 'x.png'))


        # Plot for y
        plt.figure(figsize=(width/dpi, height/dpi), dpi=dpi)

        plt.plot([i for i in range(1, len(y_result) + 1)], y_result)
        plt.title('The values of \'y\' in each generation', title_font)

        plt.xticks(**tick_font)
        plt.yticks(**tick_font)
        plt.savefig(os.path.join(save_path, 'y.png'), bbox_inches='tight', pad_inches=0.1)



def main():
    # Handle the equation here
    equation = "x^2 - 5*x -8"

    solver = Solver(equation=equation, min_range=-7, max_range=7)
    x_result, y_result, fitness, execution_time=solver.solve()
    Visualize.plot_result(x_result, y_result)

if __name__ == '__main__':
    main()