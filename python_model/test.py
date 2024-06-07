import pandas as pd

X = pd.read_json("GP30_Results.json",orient="records",lines=True)
X