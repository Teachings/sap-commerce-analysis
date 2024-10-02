from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
import json
import re

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


# Function to parse the log and extract errors
def parse_log_file(log_content):
    errors = []
    # Define patterns to extract errors and ImpEx failures
    log_pattern = re.compile(r'{"instant":.*?"thread":"(.*?)".*?"level":"(ERROR)".*?"loggerName":"(.*?)".*?"message":"(.*?)","endOfBatch"')
    impex_failure_pattern = re.compile(r'ImpExException: (.*?) Aborting further passes')
    failed_lines_pattern = re.compile(r'Finally could not import (\d+) lines')

    for line in log_content.splitlines():
        match = log_pattern.search(line)
        if match:
            error_data = {
                "thread": match.group(1),
                "level": match.group(2),
                "loggerName": match.group(3),
                "message": match.group(4)
            }
            impex_failure_match = impex_failure_pattern.search(line)
            if impex_failure_match:
                error_data["cause"] = impex_failure_match.group(1)
            
            failed_lines_match = failed_lines_pattern.search(line)
            if failed_lines_match:
                error_data["failed_lines"] = failed_lines_match.group(1)

            errors.append(error_data)
    
    return errors

@app.post("/parse/logs")
async def parse_logs(file: UploadFile = File(...)):
    # Read the uploaded file content
    content = await file.read()
    # Decode the file content (assuming it's UTF-8)
    log_content = content.decode('utf-8')
    # Parse the log content
    errors = parse_log_file(log_content)
    # Return the parsed errors as JSON
    return JSONResponse(content=errors)

@app.get("/logs", response_class=HTMLResponse)
async def serve_logs_page():
    with open("app/static/logs.html", "r") as f:
        content = f.read()
    return HTMLResponse(content=content)

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
