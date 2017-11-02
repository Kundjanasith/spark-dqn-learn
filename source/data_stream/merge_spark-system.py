import pandas as pd
spark_file = pd.read_csv("historical_data/spark/spark.csv")
system_file = pd.read_csv("historical_data/system/system.csv")

file = spark_file.join(system_file.set_index('time'), on='time')
file = file.dropna(subset=['cpu_user','cpu_system','bytes_in','bytes_out','worker'])

t = str(file.tail(1)['time']).split("    ")[1].split("\n")[0]
file.to_csv("historical_data/data/"+t+".csv", index=False)
file.to_csv("historical_data/data/current.csv", index=False)
