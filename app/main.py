from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json

app = FastAPI()

# Serve static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Relax CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def process_missing_keys(env1_data, env2_data):
    env1_keys = set(env1_data.keys())
    env2_keys = set(env2_data.keys())
    return {
        "missing_in_env1": list(env2_keys - env1_keys),
        "missing_in_env2": list(env1_keys - env2_keys)
    }

def process_value_differences(env1_data, env2_data):
    common_keys = set(env1_data.keys()) & set(env2_data.keys())
    return {
        key: {"env1_value": env1_data[key], "env2_value": env2_data[key]}
        for key in common_keys if env1_data[key] != env2_data[key]
    }

def process_common_keys(env1_data, env2_data):
    common_keys = set(env1_data.keys()) & set(env2_data.keys())
    return {
        key: env1_data[key]
        for key in common_keys if env1_data[key] == env2_data[key]
    }

@app.post("/compare/missing-keys")
async def missing_keys(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    env1_data, env2_data = json.loads(await file1.read()), json.loads(await file2.read())
    result = process_missing_keys(env1_data, env2_data)
    return JSONResponse(content=result)

@app.post("/compare/value-differences")
async def value_differences(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    env1_data, env2_data = json.loads(await file1.read()), json.loads(await file2.read())
    result = process_value_differences(env1_data, env2_data)
    return JSONResponse(content=result)

@app.post("/compare/common-keys")
async def common_keys(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    env1_data, env2_data = json.loads(await file1.read()), json.loads(await file2.read())
    result = process_common_keys(env1_data, env2_data)
    return JSONResponse(content=result)

@app.get("/", response_class=HTMLResponse)
async def serve_static():
    with open("app/static/index.html", "r") as f:
        return HTMLResponse(content=f.read())
