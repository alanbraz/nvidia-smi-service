from fastapi import FastAPI, Path
import subprocess
import os

app = FastAPI()

calls = {} 

@app.get("/start/{id}")
def start(id):
    calls[id] = subprocess.Popen(["./power.sh", id])
    return { "message": "process started"}

#@app.get("/calls")
#def get_calls():
#    return calls

@app.get("/stop/{id}")
def stop(id):
    #try:
    calls[id].kill()
    del calls[id]
    #except:
    #    return { "message": "error killing process" }
    metrics = []
    if True:
        with open("/tmp/{}.log".format(id)) as f:
            for line in f:
                metrics.append(line.split(","))
        os.remove("/tmp/{}.log".format(id))
        metrics = [ (m[0], int(m[1])) for m in metrics ]
        return {"peak": max(m[1] for m in metrics), "average": sum(m[1] for m in metrics) / len(metrics), "data": metrics }
    #except:
    #    return { "message": "error getting metrics" }
