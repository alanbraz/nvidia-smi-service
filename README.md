# nvidia-smi-service
REST API to start monitoring power metrics with nvidia-smi and capture its comsumption


```
uvicorn --host 0.0.0.0 --port 8000 power:app --root-path /power --app-dir /cos
```
