import pandas as pd
import re

df = pd.read_csv("datasets/svamp/SVAMP.csv")

bodies = df["Body"]
questions = df["Question"]
equations = df["Equation"]

def generate_full_question(index):
    body = bodies[index]
    question = questions[index]

    question = question
    if body[-1] == '.':
        problem = body + " " + question
    else:
        problem = body + ", " + question.lower()

    return question


def symbolize_problem(problem):
    len_nums = len(re.findall("\d+", problem))

    for i in range(len_nums):
        if problem[0].isdigit:
            output = re.sub('\d+ ', f"<{i+1}> ", problem, count=1)
            problem = output
        else:
            output = re.sub('\d+', f" <{i+1}>", problem, count=1)
            problem = output
        print(problem)
    
    return problem

def symbolize_equation(index):
    equation = equations[index]
    nums = re.findall("\d+", equation)
    variables = []

    for i in range(len(nums)):
        equation_index = equation.find(f" {nums[i]}.0")
        if equation_index != -1:
            equation_index += 1
        variables.append(f"<{i+1}>")

        if equation_index != -1:
            while equation_index != -1:
                for k in range(len(nums[i])+2):
                    equation = equation[:equation_index] + equation[equation_index+1:]
                equation = equation[:equation_index] + variables[i] + equation[equation_index:]
                print(f" {nums[i]}.0")
                equation_index = equation.find(f" {nums[i]}.0")
                if equation_index != -1:
                    equation_index += 1

    return equation, variables, nums