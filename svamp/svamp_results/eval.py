import re

vars = ["w", "x", "y"]

string = "3 hello 1 he77o 2 hEllo"

for i in range(3):
    if string[0].isdigit:
        output = re.sub('\d+ ', f"<{i+1}> ", string, count=1)
        string = output
        print(output)
    else:
        output = re.sub('\d+', f" <{i+1}>", string, count=1)
        string = output
        print(output)