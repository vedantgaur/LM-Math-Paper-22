import pandas as pd

from ..datasets.symbolize import generate_full_question, symbolize_equation, symbolize_problem

df = pd.read_csv("svamp/SVAMP.csv")

data = pd.DataFrame(columns=["Symbolic Problem", "Symbolic Equation", "Variables", "Numbers"])

for i in range(len(df)):
    problem = generate_full_question(i)
    symbolic_problem = symbolize_problem(i)
    _, variables, nums = symbolize_equation(i)
    datapoints = pd.DataFrame({
                                "Symbolic Problem": [symbolic_problem],
                                "Variables": [variables], 
                                "Numbers": [nums]
                             })
    data = pd.concat([data, datapoints], ignore_index = True)
    print(f"Done with Question {_+1}\n")

data.to_csv("svamp/svamp_results/temp_dataset.csv")