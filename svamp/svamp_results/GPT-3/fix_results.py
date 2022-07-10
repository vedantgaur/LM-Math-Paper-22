import pandas as pd

df = pd.read_csv("svamp/svamp_results/GPT-3/results.csv")

df0 = pd.read_csv("svamp/svamp_results/wxyz_dataset.csv")
df1 = pd.read_csv("svamp/svamp_results/augmented_svamp.csv")

symbolic_answers = df0["Equation"]

numerical_answers = df1["Answer"]
numerical_equations = df1["Equation"]

for i in range(20):
    df["Symbolic Answers"][i] = symbolic_answers[i]
    print(f"Symbolic Answer: {symbolic_answers[i]}")
    print(f"------------------")

    df["Numerical Answers"][i] = numerical_answers[i]
    print(f"Numerical Answer: {numerical_answers[i]}")
    print(f"------------------")

    df["Numerical Equations"][i] = numerical_equations[i]
    print(f"Numerical Equation: {numerical_equations[i]}")
    print(f"------------------")

df.to_csv("svamp/svamp_results/GPT-3/fixed_results.csv")