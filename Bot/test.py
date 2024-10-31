import pandas as pd
df = pd.read_csv('facebook_marketplace_data.csv', sep=',', usecols=['title'])

print(df)