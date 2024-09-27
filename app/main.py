from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
import json

app = FastAPI()

# Serve static files (CSS, JS, images, etc.)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Relax CORS policy
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Helper function to compare two JSON objects
def compare_json(env1_data, env2_data):
    env1_keys = set(env1_data.keys())
    env2_keys = set(env2_data.keys())

    missing_in_env1 = env2_keys - env1_keys
    missing_in_env2 = env1_keys - env2_keys

    common_keys = env1_keys & env2_keys
    value_differences = {
        key: {"env1_value": env1_data[key], "env2_value": env2_data[key]}
        for key in common_keys
        if env1_data[key] != env2_data[key]
    }

    result = {
        "missing_in_env1": list(missing_in_env1),
        "missing_in_env2": list(missing_in_env2),
        "value_differences": value_differences,
        "common_keys": list(common_keys),
    }
    return result

# Route to handle file upload and comparison
@app.post("/compare/")
async def compare_json_files(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    try:
        env1_data = json.loads(await file1.read())
        env2_data = json.loads(await file2.read())

        # Ensure the input is in the correct format (dict)
        if not isinstance(env1_data, dict) or not isinstance(env2_data, dict):
            return JSONResponse(content={"error": "Input must be a dictionary of key-value pairs."}, status_code=400)

        result = compare_json(env1_data, env2_data)
        return JSONResponse(content=result)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Serve the main page (index.html)
@app.get("/", response_class=HTMLResponse)
async def serve_static():
    with open("app/static/index.html") as f:
        return HTMLResponse(f.read())
