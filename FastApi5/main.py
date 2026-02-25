"""
메인 엔트리 (Main Entry)
- FastAPI 앱 생성 및 라우터 등록
- 앱 시작 시 DB 테이블 생성 및 시세 생성기 실행
"""
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import asyncio

import models, auth, database
from routes import market, trade
from schemas import Token


app = FastAPI()

# CORS 설정
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# market과 trade 라우터 등록
app.include_router(market.router)
app.include_router(trade.router)


@app.on_event("startup")
async def startup_event():
    """앱 시작 시 실행될 로직: DB 테이블 생성"""
    # 비동기 엔진을 사용하여 DB 테이블 생성
    async with database.engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

    # 시세 생성기(market.price_generator)를 백그라운드 태스크로 실행
    asyncio.create_task(market.price_generator())


@app.post("/register")
async def register(
    username: str, password: str, db: AsyncSession = Depends(database.get_db)
):
    """회원가입"""
    # TODO: 중복 아이디를 확인하고, 새로운 유저를 생성하여 DB에 저장하세요
    result = await db.execute(select(models.User).where(models.User.username == username))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="이미 존재하는 아이디입니다.")

    new_user = models.User(
        username=username,
        password=auth.hash_password(password)
    )
    db.add(new_user)
    await db.commit()
    return {"msg": f"{new_user.username}님 회원가입이 완료됐습니다."}


@app.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(database.get_db),
):
    """로그인"""
    # TODO: 유저 정보를 확인하고, 비밀번호 검증 후 JWT 토큰을 발급하세요
    # 토큰 만료 시간은 현재시간 + 15분 입니다.
    user = await db.execute(select(models.User).where(models.User.username == form_data.username))
    user = user.scalar_one_or_none()

    if user is None or not auth.verify_passsword(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="아이디나 비밀번호가 틀렸습니다.")

    access_token = auth.create_access_token({"sub": user.username})
    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
