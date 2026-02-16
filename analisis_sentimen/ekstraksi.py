import pandas as pd
data = pd.json_normalize(pd.read_json("aveta.json"))
data.to_csv("aveta.csv", index=False)
