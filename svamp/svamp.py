import re
import pandas as pd

df = pd.read_csv("svamp/SVAMP.csv")

bodies = df["Body"]
questions = df["Question"]
equations = df["Equation"]

def parse(index):
    body = bodies[index]
    question = questions[index]
    equation = equations[index]

    question = question.lower()
    problem = body + " " + question
    # print(problem)

    nums = re.findall("\d+", problem)
    # print(nums)

    variables = []

    for i in range(len(nums)):
        num_index = problem.find(f"{nums[i]} ")
        equation_index = equation.find(f"{nums[i]}.0")
        variables.append(f"<{i+1}>")

        while num_index != -1:
            for j in range(len(nums[i])):
                problem = problem[:num_index] + problem[num_index+1:]
            problem = problem[:num_index] + variables[i] + problem[num_index:]
            num_index = problem.find(f"{nums[i]} ")
            print(problem)
            # print(f"Done with problem {i}")

        if equation_index != -1:
            while equation_index != -1:
                for k in range(len(nums[i])+2):
                    equation = equation[:equation_index] + equation[equation_index+1:]
                equation = equation[:equation_index] + variables[i] + equation[equation_index:]
                print(f"{nums[i]}.0")
                equation_index = equation.find(f"{nums[i]}.0")
                print(equation + "\n")
                # print(f"Done with equation {i}")

    # print(problem)
    # print(equation)
    # print(variables)
    return problem, equation, variables, nums


if __name__ == "__main__":
    print(len(df))
    data = pd.DataFrame(columns=["Symbolic Problem", "Symbolic Equation", "Variables", "Numbers"])
    # for _ in range(len(df)):
    for _ in range(28):
        symbolic_problem, symbolic_equation, variables, numbers = parse(_)
        datapoints = pd.DataFrame({
                                   "Symbolic Problem": [symbolic_problem],
                                   "Symbolic Equation": [symbolic_equation], 
                                   "Variables": [variables], 
                                   "Numbers": [numbers]
                                 })
        data = pd.concat([data, datapoints], ignore_index = True)
        # print(data)
        print(f"Done with Question {_+1}\n")
    data.to_csv("svamp/svamp_results/temp_dataset.csv")