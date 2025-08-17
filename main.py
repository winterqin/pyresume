import uvicorn
from fastapi import FastAPI
from backend.config import settings
from backend.routers import application_router, platform_router

app = FastAPI(
    title="求职管理系统API",
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

# 包含路由
app.include_router(application_router)
app.include_router(platform_router)


@app.get("/")
async def root():
    return {"message": "求职管理系统API服务运行中"}


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == '__main__':
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        access_log=True,  # 关键参数
        log_level="info",  # 确保不是 "warning" 或更高
        reload=True
    )
