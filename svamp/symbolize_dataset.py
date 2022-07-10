import pandas as pd
import ast
import numpy as np

replacements = [
    "w", "x", "y", "z"
]

df = pd.read_csv("svamp/svamp_results/augmented_svamp.csv")

symbolic_problems = df["Symbolic Problem"]
variables = df["Variables"]
symbolic_equations = df["Symbolic Equation"]

def symbolize_dataset(index):
    problem = symbolic_problems[index]
    equation = symbolic_equations[index]
    vars = variables[index]
    vars = ast.literal_eval(vars)
    print(problem)

    for i in range(len(vars)):
        var_index = problem.find(vars[i])
        while var_index != -1:
            if var_index != -1:
                for j in range(len(vars[i])):
                    problem = problem[:var_index] + problem[var_index+1:]
                problem = problem[:var_index] + replacements[i] + problem[var_index:]
                print(problem)
                print(var_index)
            var_index = problem.find(vars[i])
        
        equation_index = equation.find(vars[i])
        if equation_index != -1:
            while equation_index != -1:
                for k in range(len(vars[i])):
                    equation = equation[:equation_index] + equation[equation_index+1:]
                equation = equation[:equation_index] + replacements[i] + equation[equation_index:]
                equation_index = equation.find(vars[i])
                if equation_index != -1:
                    equation_index += 1
                print(equation + "\n")

    return problem, equation


if __name__ == "__main__":
    data = pd.DataFrame(columns=["Question", "Equation"], index=np.arange(len(variables)))
    for i in range(len(variables)):
    # for i in range(11):
        data["Question"][i], data["Equation"][i] = symbolize_dataset(i)
        print(data["Question"][i])
        # questions = pd.DataFrame([symbolize_dataset(i)], columns=["Question"])
        # pd.concat([data, questions], ignore_index=True)
    data.to_csv("svamp/svamp_results/wxyz_dataset.csv")