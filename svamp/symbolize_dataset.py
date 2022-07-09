import pandas as pd
import ast
import numpy as np

vars = [
    "w", "x", "y", "z"
]

df = pd.read_csv("svamp/svamp_results/augmented_svamp.csv")

symbolic_problems = df["Symbolic Problem"]
variables = df["Variables"]

def symbolize_dataset(index):
    var_index = 0
    problem = symbolic_problems[index]
    vars = variables[index]
    vars = ast.literal_eval(vars) 

    for i in range(len(vars)):
        while var_index == -1:
            var_index = problem.find(vars[i])
            for j in range(len(vars[i])):
                problem = problem[:var_index] + problem[var_index+1:]
            problem = problem[:var_index] + f"x{i+1}" + problem[var_index:]
    return problem


if __name__ == "__main__":
    data = pd.DataFrame(columns=["Question"], index=np.arange(len(variables)))
    for i in range(len(variables)):
        data["Question"][i] = symbolize_dataset(i)
        # questions = pd.DataFrame([symbolize_dataset(i)], columns=["Question"])
        # pd.concat([data, questions], ignore_index=True)
    data.to_csv("svamp/svamp_results/test.csv")