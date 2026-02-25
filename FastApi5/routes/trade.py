"""
거래 라우터 (Trade Router)
- 사용자 자산 상태 조회 및 매수/매도 로직 처리
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import get_db
from auth import get_current_user
import models, schemas
from .market import manager

router = APIRouter()


@router.get("/user/status")
async def get_status(
    current_price: float,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """사용자 자산 상태 조회 실습"""

    # 현재 유저의 Portfolio 정보를 조회
    result = await db.execute(
        select(models.Portfolio).where(models.Portfolio.username == user.id)
    )
    p = result.scalar_one_or_none()

    # 포트폴리오 존재 여부에 따라 보유수량과 평단가 설정
    amount = p.amount if p else 0
    avg_price = p.avg_price if p else 0

    # 현재가 기준 수치 계산
    evaluation = amount * current_price          # 평가 금액
    profit = evaluation - (amount * avg_price)  # 평가 손익

    return {
        "cash": user.balance,
        "holdings": amount,
        "evaluation": evaluation,
        "profit": profit,
        "total_asset": user.balance + evaluation,
    }


@router.post("/trade/{action}")
async def trade(
    action: str,
    payload: schemas.TradeRequest,
    user: models.User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """매수 및 매도 처리 로직 실습"""

    username = user.username

    # 해당 유저의 포트폴리오 정보를 조회
    result = await db.execute(
        select(models.Portfolio).where(models.Portfolio.username == user.id)
    )
    p = result.scalar_one_or_none()

    if action == "buy":
        # 총 매수 비용 계산 및 잔액 부족 체크
        cost = payload.amount * payload.price
        if user.balance < cost:
            raise HTTPException(status_code=400, detail="잔액이 부족합니다.")

        # 잔액 차감
        user.balance -= cost

        # 포트폴리오 업데이트
        if p:
            # 기존 데이터가 있으면 가중 평균으로 평단가 갱신
            p.avg_price = (
                (p.avg_price * p.amount) + (payload.price * payload.amount)
            ) / (p.amount + payload.amount)
            p.amount += payload.amount
        else:
            # 기존 데이터가 없으면 새 Portfolio 생성
            new_p = models.Portfolio(
                username=user.id,
                amount=payload.amount,
                avg_price=payload.price,
            )
            db.add(new_p)

    elif action == "sell":
        # 매도 가능 여부 체크
        if not p or p.amount < payload.amount:
            raise HTTPException(status_code=400, detail="보유 수량이 부족합니다.")

        # 잔액 증가 및 보유 수량 차감
        user.balance += payload.amount * payload.price
        p.amount -= payload.amount

        # 수량이 0이 되면 포트폴리오 삭제
        if p.amount == 0:
            db.delete(p)

    # 변경 사항 저장
    await db.commit()

    # 전체 사용자에게 거래 알림 브로드캐스트
    await manager.broadcast({"type": "trade_news", "msg": f"🔔 {username}님 {action} 완료"})

    return {"msg": "success"}
