from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from contextlib import asynccontextmanager
# from example import router as test_router
# from database import database
from likedSector.likedSector import likedSector
import asyncio
from crawling.crawling import *

async def schedule_crawling(interval):
    while True:
        print("Running crawling...")
        # crawling()을 비동기로 실행 (CPU 작업이 아닌 IO 작업)
        await asyncio.to_thread(crawling)  
        print(f"Waiting for {interval} minutes...")
        await asyncio.sleep(interval * 60)  # 30분 대기

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("서버 시작 중...")
    
    # 주기적인 crawling 호출
    crawling_task = asyncio.create_task(schedule_crawling(30))

    yield  # 서버가 실행되는 동안

    # 서버 종료 시
    print("서버 종료 중...")
    crawling_task.cancel()  # crawling 작업 중단

app = FastAPI(lifespan=lifespan)

# CORS 설정 (필요한 경우)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# app.include_router(test_router.router, prefix="/test")
app.include_router(likedSector.router, prefix="/likedSector")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)