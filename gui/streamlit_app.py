import streamlit as st
import os
import sys

path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, path)
from evolution_algorithm.solver import Solver


def main():
    st.title("Equation Solver using Genetic Algorithm")

    st.sidebar.header("Equation to be solved")
    a = st.sidebar.text_input("a", value=1)

    st.sidebar.info("Click the button below to solve the equation.")
    if st.sidebar.button("Solve"):

        solver = Solver(equation = a)
        solution = solver.solve()

        st.success(f"The solution is x = {solution}")

if __name__ == "__main__":
    main()
