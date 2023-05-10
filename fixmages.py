import pandas as pd
import re

df = pd.read_csv('places.csv' ,index_col=0)
new_df = pd.read_csv('places-new.csv')

for i in range(len(new_df)):
        x = re.findall(r'(https?://\S+)', (new_df.iloc[i , 0]))[0]
        x = x.replace('"' , '')
        print(x)
        df.iloc[i, df.columns.get_loc('ImageUrl')] =x

df=df.reset_index(drop=True)
df.to_csv('places.csv')