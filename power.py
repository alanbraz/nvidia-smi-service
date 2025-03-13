from fastapi import FastAPI
import subprocess
import os
import pandas as pd
import numpy as np
import json

app = FastAPI()

calls = {} 

@app.get("/start/{id}")
def start(id):
    calls[id] = subprocess.Popen(["./power.sh", id])
    return { "message": "process started"}

@app.get("/stop/{id}")
def stop(id):
    try:
        calls[id].kill()
        del calls[id]
    except:
        return { "message": "error killing process" }
    try:
        metrics = []
        # Read the text file into a DataFrame, specifying the delimiter as '\t' (tab)
        df = pd.read_csv("/tmp/{}.log".format(id), sep='\s+', header=0)
        df = df.drop(index=0)
        mapping_dict = {'-': None}
        df = df.replace(mapping_dict)
        for c in df.columns[2:].to_list():
            df[c] = df[c].astype(float)
        js = json.loads(df[(df["busy"]>=0)].to_json())
        os.remove("/tmp/{}.log".format(id))
        metrics = [ [js["Time"][i], js["pwr"][i]] for i in js["pwr"].keys() ]
        return {"peak": np.nan_to_num(np.max(df[(df["busy"]>1)]["pwr"]), nan=0), "average": np.nan_to_num(np.mean(df[(df["busy"]>1)]["pwr"]), nan=0), "data": metrics }
    except:
       return { "message": "error getting metrics" }            
