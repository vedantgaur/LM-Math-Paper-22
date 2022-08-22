import os
import openai

import pandas as pd
import numpy as np
import ast

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper v2"
wxyz = pd.read_csv(f"{root_dir}/datasets/svamp/results/wxyz_dataset.csv")
augmented = pd.read_csv(f"{root_dir}/datasets/svamp/results/augmented_svamp.csv")

indices = np.load(f"{root_dir}/datasets/svamp/svamp_indices.npy")

data = pd.DataFrame(
    columns=[
    "Index",
    "With Steps", 
    "Without Steps", 
    "With Intermediate Variables",
    "Numerical Answer",
    ], 
    index=np.arange(50)
    )

symbolic_questions = wxyz["Question"]
symbolic_answers = wxyz["Equation"]

numerical_bodies = augmented["Body"]
numerical_questions = augmented["Question"]
numerical_answers = augmented["Answer"]
numbers = augmented["Numbers"]

vars = ["w", "x", "y", "z"] 

def open_ai(_prompt):
    gpt3_response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0,
        max_tokens=256,
    )
    return gpt3_response

def step_two(prompt, response, i):
    input = f"{prompt}{response}\nGiven "
    nums = ast.literal_eval(numbers[i])
    for j in range(len(nums)):
        if j != len(nums)-1:
            print(i, j)
            input += f"{vars[j]} = {nums[j]} and "
        else:
            input += f"{vars[j]} = {nums[j]}, the answer is: "

    print(input)

    _gpt3_response = openai.Completion.create(
        model="text-davinci-002",
        prompt=input,
        temperature=0,
        max_tokens=256,
    )
    return _gpt3_response

def get_response(prompt):
    print(prompt)

    response = open_ai(prompt)
    response = response["choices"][0]["text"]
    response = response.strip('\n')

    return response

def get_step_two(prompt, response, i):
    _response = step_two(prompt, response, i)
    _response = _response["choices"][0]["text"]
    _response = _response.strip('\n')

    return _response


def symbolic_prompt(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: "    
    return prompt

def symbolic_prompt_steps(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step. "
    return prompt

def symbolic_prompt_intermediate(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically. "
    return prompt

def run(index, j):
    # WITHOUT STEPS
    response = get_response(symbolic_prompt(index))
    final_response = get_step_two(symbolic_prompt(index), response, index)
    print(f"no reasoning:  {final_response}")
    print(f"------------------")
    data["Without Steps"][j] = final_response

    # WITH STEPS
    response = get_response(symbolic_prompt_steps(index))
    final_response = get_step_two(symbolic_prompt_steps(index), response, index)
    print(f"with reasoning:  {final_response}")
    print(f"------------------")
    data["With Steps"][j] = final_response

    # WITH INTERMEDIARY
    response = get_response(symbolic_prompt_intermediate(index))
    final_response = get_step_two(symbolic_prompt_intermediate(index), response, index)
    print(f"no reasoning:  {final_response}")
    print(f"------------------")
    data["With Intermediate Variables"][j] = final_response

    # NUMERIC ANSWER KEY
    data["Numerical Answer"][j] = numerical_answers[index]
    print(f"Numerical Answer: {numerical_answers[index]}")
    print(f"------------------")


if __name__ == "__main__":
    for i in range(50):
        index = int(indices[i])
        run(index, i)
        print(f"DONE WITH {i+1}, INDEX {index}")
        data["Index"][i] = index

    data.to_csv(f"{root_dir}/.models/GPT-3/results/two_step.csv")