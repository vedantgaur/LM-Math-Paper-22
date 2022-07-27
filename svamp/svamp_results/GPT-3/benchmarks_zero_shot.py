import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "c:/users/vedan/onedrive/desktop/research paper"
df = pd.read_csv(f"{root_dir}/svamp/svamp_results/wxyz_dataset.csv")
df1 = pd.read_csv(f"{root_dir}/svamp/svamp_results/augmented_svamp.csv")

indices = np.load(f"{root_dir}/svamp/svamp_results/indices.npy")

data = pd.DataFrame(
    columns=[
    "Index",
    "Symbolic With Steps", 
    "Symbolic Without Steps", 
    "Symbolic With Intermediate Variables", 
    "Numerical With Steps", 
    "Numerical Without Steps", 
    "Numerical With Intermediate Variables",
    "Symbolic Answer", 
    "Numerical Answer",
    "Numerical Equation"
    ], 
    index=np.arange(50)
    )

symbolic_questions = df["Question"]
symbolic_answers = df["Equation"]

numerical_bodies = df1["Body"]
numerical_questions = df1["Question"]
numerical_answers = df1["Answer"]
numerical_equations = df1["Equation"]

def open_ai(_prompt):
    gpt3_response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0,
        max_tokens=256,
    )
    return gpt3_response

def get_response(prompt):
    print(prompt)

    response = open_ai(prompt)
    response = response["choices"][0]["text"]
    response = response.strip('\n')

    return response


def symbolic_prompt(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: "    
    return prompt

def symbolic_prompt_steps(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step. "
    return prompt

def symbolic_prompt_intermediate(i):
    prompt = f"Q: {symbolic_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically. "
    return prompt

def numeric_prompt(i):
    prompt = f"Q: {numerical_bodies[i]} {numerical_questions[i]}\n\nA: "
    return prompt

def numeric_prompt_steps(i):
    prompt = f"Q: {numerical_bodies[i]} {numerical_questions[i]}\n\nA: Let's think step by step. "
    return prompt

def numeric_prompt_intermediate(i):
    prompt = f"Q: {numerical_bodies[i]} {numerical_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically. "
    return prompt

def run_symbolic(index, j):
    # SYMBOLIC WITHOUT STEPS
    response = get_response(symbolic_prompt(index))
    print(f"Symbolic no reasoning:  {response}")
    print(f"------------------")
    data["Symbolic Without Steps"][j] = response

    # SYMBOLIC WITH STEPS
    response = get_response(symbolic_prompt_steps(index))
    print(f"Symbolic with reasoning:  {response}")
    print(f"------------------")
    data["Symbolic With Steps"][j] = response

    # SYMBOLIC WITH INTERMEDIARY
    response = get_response(symbolic_prompt_intermediate(index))
    print(f"Symbolic with intermediary:  {response}")
    print(f"------------------")
    data["Symbolic With Intermediate Variables"][j] = response

    # SYMBOLIC ANSWER KEY
    data["Symbolic Answer"][j] = symbolic_answers[index]
    print(f"Symbolic Answer: {symbolic_answers[index]}")
    print(f"------------------")

def run_numeric(index, k):
    # NUMERICAL WITHOUT STEPS
    response = get_response(numeric_prompt(index))
    print(f"Numerical no reasoning:  {response}")
    print(f"------------------")
    data["Numerical Without Steps"][k] = response

    # NUMERICAL WITH STEPS
    response = get_response(numeric_prompt_steps(index))
    print(f"Numerical with reasoning:  {response}")
    print(f"------------------")
    data["Numerical With Steps"][k] = response

    # NUMERIC WITH INTERMEDIARY
    response = get_response(numeric_prompt_intermediate(index))
    print(f"Numerical with intermediary:  {response}")
    print(f"------------------")
    data["Numerical With Intermediate Variables"][k] = response

    # NUMERIC ANSWER KEY
    data["Numerical Answer"][k] = numerical_answers[index]
    print(f"Numerical Answer: {numerical_answers[index]}")
    print(f"------------------")

    data["Numerical Equation"][k] = numerical_equations[index]
    print(f"Numerical Equation: {numerical_equations[index]}")
    print(f"------------------")


if __name__ == "__main__":
    for i in range(50):
        index = int(indices[i])
        run_symbolic(index, i)
        run_numeric(index, i)
        print(f"DONE WITH {i+1}, INDEX {index}")
        data["Index"][i] = index

    # data.to_csv("svamp/svamp_results/GPT-3/results.csv")
    data.to_csv(f"{root_dir}/svamp/svamp_results/GPT-3/results/zero_shot/zero_shot_results.csv")