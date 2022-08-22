import os
import openai

import pandas as pd
import numpy as np

openai.api_key = os.getenv("OPENAI_API_KEY")

root_dir = "~/onedrive/desktop/research paper v2"
wxyz = pd.read_csv(f"{root_dir}/datasets/svamp/results/wxyz_dataset.csv")
augmented = pd.read_csv(f"{root_dir}/datasets/svamp/results/augmented_svamp.csv")

indices = np.load(f"{root_dir}/datasets/svamp/svamp_indices.npy")

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

symbolic_questions = wxyz["Question"]
symbolic_answers = wxyz["Equation"]

numerical_bodies = augmented["Body"]
numerical_questions = augmented["Question"]
numerical_answers = augmented["Answer"]
numerical_equations = augmented["Equation"]

prelim_question = """
Q: After resting they decided to go for a swim. If the depth of the water is w times Dean's height and he stands at x feet how much deeper is the water than Dean's height?

A: First, we need to find Dean's height. We know that the depth of the water is w times Dean's height, and we know that Dean is standing at x feet. This means that the depth of the water must be wx feet. 

Now, we need to find out how much deeper the water is than Dean's height. To do this, we need to subtract Dean's height from the depth of the water. We know that Dean's height is x feet, so the depth of the water must be wx - x feet. 

This means that the water is (wx - x) feet deeper than Dean's height.

Therefore, the answer (symbolic expression) is: 

wx - x\n\n
"""

prelim_question_steps = """
Q: After resting they decided to go for a swim. If the depth of the water is w times Dean's height and he stands at x feet how much deeper is the water than Dean's height?

A: Let's think step by step. 

First, we need to find Dean's height. We know that the depth of the water is w times Dean's height, and we know that Dean is standing at x feet. This means that the depth of the water must be wx feet. 

Now, we need to find out how much deeper the water is than Dean's height. To do this, we need to subtract Dean's height from the depth of the water. We know that Dean's height is x feet, so the depth of the water must be wx - x feet. 

This means that the water is (wx - x) feet deeper than Dean's height.

Therefore, the answer (symbolic expression) is: 

wx - x\n\n
"""

prelim_question_intermediate = """
Q: After resting they decided to go for a swim. If the depth of the water is w times Dean's height and he stands at x feet how much deeper is the water than Dean's height?

A: Let's think step by step. Introduce intermediate variables and solve the task symbolically. 

Let's denote the depth of the water by h.

h = w * x

If Dean is x feet tall then the depth of the water is h - x feet.

Plugging in for x we get that the water is wx - x feet deeper than Dean's height.

Therefore, the answer (symbolic expression) is: 

wx - x\n\n
"""

numeric_prelim_question = '''
Q: After resting they decided to go for a swim. If the depth of the water is 10 times Dean's height and he stands at 9 feet how much deeper is the water than Dean's height?

A: First, we need to find Dean's height in feet. 9 feet is the same as 9/1 feet, so we can say that Dean's height is 9/1 feet. 

Next, we need to find 10 times Dean's height in feet. 10 times 9/1 feet is the same as 90/1 feet, so we can say that 10 times Dean's height is 90/1 feet. 

Now, we need to find the difference between the depth of the water and Dean's height. The depth of the water is 90/1 feet and Dean's height is 9/1 feet, so the difference is 81/1 feet. 

We can simplify 81/1 feet to just 81 feet, so we can say that the depth of the water is 81 feet deeper than Dean's height.

Therefore the answer (numeric) is: 

81\n\n
'''

numeric_prelim_question_steps = '''
Q: After resting they decided to go for a swim. If the depth of the water is 10 times Dean's height and he stands at 9 feet how much deeper is the water than Dean's height?

A: Let's think step by step. 

First, we need to find Dean's height in feet. 9 feet is the same as 9/1 feet, so we can say that Dean's height is 9/1 feet. 

Next, we need to find 10 times Dean's height in feet. 10 times 9/1 feet is the same as 90/1 feet, so we can say that 10 times Dean's height is 90/1 feet. 

Now, we need to find the difference between the depth of the water and Dean's height. The depth of the water is 90/1 feet and Dean's height is 9/1 feet, so the difference is 81/1 feet. 

We can simplify 81/1 feet to just 81 feet, so we can say that the depth of the water is 81 feet deeper than Dean's height.

Therefore the answer (numeric) is: 

81\n\n
'''

numeric_prelim_question_intermediate = '''
Q: After resting they decided to go for a swim. If the depth of the water is 10 times Dean's height and he stands at 9 feet how much deeper is the water than Dean's height?

A: Let's think step by step. Introduce intermediate variables and solve the task symbolically. 

Let's denote Dean's height by h. Then the depth of the water is 10h. 

The difference between the depth of the water and Dean's height is 

10h-h=9h. 

Therefore the answer (numeric) is: 

9h = 9*9 = 81\n\n
'''


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
    prompt = f"{prelim_question}Q: {symbolic_questions[i]}\n\nA: "    
    return prompt

def symbolic_prompt_steps(i):
    prompt = f"{prelim_question_steps}Q: {symbolic_questions[i]}\n\nA: Let's think step by step. "
    return prompt

def symbolic_prompt_intermediate(i):
    prompt = f"{prelim_question_intermediate}Q: {symbolic_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically. "
    return prompt

def numeric_prompt(i):
    prompt = f"{numeric_prelim_question}Q: {numerical_bodies[i]} {numerical_questions[i]}\n\nA: "
    return prompt

def numeric_prompt_steps(i):
    prompt = f"{numeric_prelim_question_steps}Q: {numerical_bodies[i]} {numerical_questions[i]}\n\nA: Let's think step by step. "
    return prompt

def numeric_prompt_intermediate(i):
    prompt = f"{numeric_prelim_question_intermediate}Q: {numerical_bodies[i]} {numerical_questions[i]}\n\nA: Let's think step by step. Introduce intermediate variables and solve the task symbolically. "
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
    for i in range(len(indices)):
        index = int(indices[i])
        run_symbolic(index, i)
        run_numeric(index, i)
        print(f"DONE WITH {i+1}, INDEX {index}")
        data["Index"][i] = index

    data.to_csv(f"{root_dir}/.models/GPT-3/results/one_shot.csv")