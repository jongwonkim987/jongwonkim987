"""
데이터 검증 계층 (Schemas Layer)
- Pydantic의 BaseModel을 사용하여 요청 및 응답 데이터의 형식 정의
"""
from pydantic import BaseModel


class TradeRequest(BaseModel):
    """매수/매도 요청 모델"""
    # TODO: 주문 수량(amount / int)과 주문 가격(price / float) 필드를 정의하세요
    amount: int
    price: float


class Token(BaseModel):
    """토큰 응답 모델"""
    # TODO: access_token(str)과 token_type(str) 필드를 정의하세요
    access_token: str
    token_type: str
