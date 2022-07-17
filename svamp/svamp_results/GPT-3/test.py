import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

_prompt = "Q: Each pack of dvds costs 76 dollars. If there is a discount of 25 dollars on each pack how much do you have to pay to buy each pack?\n\nA: "
response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

print(_prompt)
print(response)

print("=====================================================")

_prompt = 'Q: Dan had $ 3 left with him after he bought a candy bar. If he had $ 4 at the start how much did the candy bar cost?\n\nA: '
response = openai.Completion.create(
        model="text-davinci-002",
        prompt=_prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

print(_prompt)
print(response)