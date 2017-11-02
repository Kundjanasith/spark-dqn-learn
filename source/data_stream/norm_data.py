import glob
import pandas as pd
path = 'historical_data/data'
filenames = glob.glob(path + "/*.csv")
for f in filenames:
    if f != "historical_data/data/current.csv":  
        x = pd.read_csv(f)
        x = x.drop_duplicates()
        n = f.split("/")[2]
        x.to_csv("historical_data/norm_data/"+n,index=False)