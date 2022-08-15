import pandas as pd
import re


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

def symbolize_equation(equation):
    len_nums = len(re.findall("\d+", equation))

    for i in range(len_nums):
        if equation[0].isdigit:
            output = re.sub('\d+ ', f"<{i+1}> ", equation, count=1)
            equation = output
        else:
            output = re.sub('\d+', f" <{i+1}>", equation, count=1)
            equation = output
        print(equation)
    
    return equation
