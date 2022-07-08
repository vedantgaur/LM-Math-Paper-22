import pandas as pd

# df = pd.read_csv("SVAMP.csv")
# df1 = pd.read_csv("temp.csv")

# data = df.join(df1)
# print(data)
# data.to_csv("augmented_svamp.csv")
df = pd.read_csv("augmented_svamp.csv")
df.drop(df.columns[1], axis=1, inplace=True)
df.to_csv("augmented_svamp.csv")