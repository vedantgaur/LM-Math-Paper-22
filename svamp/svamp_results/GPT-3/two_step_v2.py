import os
import openai

import pandas as pd
import numpy as np
import ast

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "c:/users/vedan/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/wxyz_dataset.csv")
df1 = pd.read_csv(f"{root_dir}/svamp/svamp_results/augmented_svamp.csv")

indices = np.load(f"{root_dir}/svamp/svamp_results/indices_plus.npy")

data = pd.DataFrame(
    columns=[
    "Index",
    "With Steps", 
    "Without Steps", 
    "With Intermediate Variables",
    "Numerical Answer",
    ], 
    index=np.arange(150)
    )

symbolic_questions = df["Question"]
symbolic_answers = df["Equation"]

numerical_bodies = df1["Body"]
numerical_questions = df1["Question"]
numerical_answers = df1["Answer"]
numbers = df1["Numbers"]

vars = ["w", "x", "y", "z"] 

def open_ai(_prompt):
    gpt3_response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0,
        max_tokens=256,
    )
    return gpt3_response

def step_two(i):
    input = "Given "
    nums = ast.literal_eval(numbers[i])
    for j in range(len(nums)):
        if j != len(nums)-1:
            print(i, j)
            input += f"{vars[j]} = {nums[j]} and "
        else:
            input += f"{vars[j]} = {nums[j]}, the answer is: "

    return input


def get_response(prompt):
    print(prompt)

    response = open_ai(prompt)
    response = response["choices"][0]["text"]
    response = response.strip('\n')

    return response


def symbolic_prompt(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: \n\n{step_two(i)}" 
    print(prompt)   
    return prompt

def symbolic_prompt_steps(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step. \n\n{step_two(i)}"
    return prompt

def symbolic_prompt_intermediate(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically. \n\n{step_two(i)}"
    return prompt

def run(index, j):
    # WITHOUT STEPS
    response = get_response(symbolic_prompt(index))
    print(f"no reasoning:  {response}")
    print(f"------------------")
    data["Without Steps"][j] = response

    # WITH STEPS
    response = get_response(symbolic_prompt_steps(index))
    print(f"with reasoning:  {response}")
    print(f"------------------")
    data["With Steps"][j] = response

    # WITH INTERMEDIARY
    response = get_response(symbolic_prompt_intermediate(index))
    print(f"no reasoning:  {response}")
    print(f"------------------")
    data["With Intermediate Variables"][j] = response

    # NUMERIC ANSWER KEY
    data["Numerical Answer"][j] = numerical_answers[index]
    print(f"Numerical Answer: {numerical_answers[index]}")
    print(f"------------------")


if __name__ == "__main__":
    for i in range(150):
        index = int(indices[i])
        run(index, i)
        print(f"DONE WITH {i+1}, INDEX {index}")
        data["Index"][i] = index

    data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/two_step_v2/two_step_v2_150.csv")