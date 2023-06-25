import uvicorn

# Importing app here makes the syntax cleaner as it will be picked up by refactors
from main import app

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=10)