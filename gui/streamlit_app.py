import streamlit as st
import os
import sys
import json
from streamlit_lottie import st_lottie as stl
path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)
from evolution_algorithm.solver import Solver
import requests
from pathlib import Path
from PIL import Image

output_path = Path(__file__).parent
assets_path = output_path / Path(r"../assets")
vizs_path = output_path / Path(r"../assets/viz")
gui_path = output_path / Path(r"../assets/gui")


def main():
    st.set_page_config(page_title="Equation Solver using Genetic Algorithm", page_icon="🧬", layout="wide")
    
    background_color = """
        <style>
            body {
                background-color: #FFFFFF;
            }
        </style>
    """

    # Use st.markdown to apply the background color
    st.markdown(background_color, unsafe_allow_html=True)

    #Header Section
    with st.container():
        st.title("Equation Solver using Genetic Algorithm")
        st.write("##")

    st.sidebar.header("Equation to be solved")
    a = st.sidebar.text_input("Please input equation in the correct format", value="x^2+2*x-3")

    st.sidebar.info("Click the button below to solve the equation.")
    if st.sidebar.button("Solve"):

        if a == "":
            st.error("Please input an equation.")
            return
        elif a.count("=") != 0:
            st.error("Please input a valid equation.")
            return
        try:
            solver = Solver(equation = a)
            results = solver.solve()
            solution = str(results[0][-1])
            exc_time = results[3]
        
        except Exception:
            st.error("Please input a valid equation.")
            return
        

        st.success(f"The solution is x = {solution}")
        st.success(f"Execution time: {exc_time}")
        st.sidebar.info("Click the button below to view the results analysis.")

        with st.container():
            st.header("Results Analysis")
            st.write("###")
            st.write("The graph below shows the best fitness value for each generation.")
            left_column, right_column = st.columns(2)
            
            st.image(Image.open(vizs_path / Path("x.png")))
            st.image(Image.open(vizs_path / Path("y.png")))


    #--- Helper Section ---
    with st.container():
        st.write("---")
        left_column, right_column = st.columns(2)
        with left_column:
            st.header("The Method")
            st.write("Genetic Algorithm is a method of solving problems based on the theory of natural selection and evolution. It is a metaheuristic inspired by the process of natural selection that belongs to the larger class of evolutionary algorithms (EA).")
            st.image(Image.open(gui_path / Path("gaflowchart.png")))
            
            st.latex("x^2+2*x-3=0")
            st.write("The equation above is an example of the equation that can be solved using this application.")

        with right_column:
            st.header("Equation Syntax")
            st.write("The solver supports the following operators:")
            st.table({
                "Operator": "Syntax",
                "Addition": "+",
                "Subtraction": "-",
                "Multiplication": "*",
                "Division": "/",
                "Exponentiation": "^",
                "Parentheses": "()",
                "Square Root": "sqrt(x)",
                "sin": "sin(x)",
                "cos": "cos(x)",
                "tan": "tan(x)",
                "Square root": "sqrt(x)",
                "max": "max(x, y)",
                "min": "min(x, y)",
                "absolute value": "abs(x)",
            })

if __name__ == "__main__":
    main()
