# test_app.py
from fastapi import FastAPI
import uvicorn

app = FastAPI()


@app.get("/")
def root():
    return {"message": "Hello World"}


if __name__ == '__main__':
    # --------------------------
    # 3. 确保Uvicorn日志级别足够低
    # --------------------------
    uvicorn.run(
        "test_app:app",
    )
