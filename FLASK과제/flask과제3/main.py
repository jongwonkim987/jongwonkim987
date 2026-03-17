from sqlalchemy import create_engine, Integer, String, Column
from sqlalchemy.orm import sessionmaker, declarative_base

# 데이트베이스 연결
engine = create_engine('sqlite:///users.db', echo=True)

# 데이터베이스 연결 통로: 세션 생성
Session_local = sessionmaker(bind=engine)

# 베이스 클래스 정의
Base = declarative_base()

# User 모델 정의: 사용자 이름을 저장하는 테이블
class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)

    def __repr__(self):
        return f"User(id={self.id}, name={self.name})"

# 테이블 생성
Base.metadata.create_all(bind=engine)

# <---------------------------------------------->

def run_single():
    db = Session_local() #직접 연결하는 코드
    # CREATE
    new_user = User(name="OZ_BE")
    db.add(new_user)
    db.commit()
    print("사용자 추가:", new_user)

    # READ
    user = db.query(User).first()
    print("사용자 조회:", user)

    # UPDATE
    if user:
        user.name = "OZ_BE_Updated"
        db.commit()
        print("사용자 수정:", user)

    # DELETE
    if user:
        db.delete(user)
        db.commit()
        print("사용자 삭제:", user)
    db.close()

def run_bulk():
    db = Session_local() #직접 연결하는 코드
    # 대량 CREATE
    new_users = [User(name="OZ_BE17"), User(name="OZ_BE18"), User(name="OZ_BE19")]
    db.add_all(new_users)
    db.commit()
    print("사용자 추가:", new_users)

    # READ
    ## 조건 조회
    first_users = db.query(User).filter(User.name == "OZ_BE17").first()
    print("조건 조회 사용자:", first_users)

    ## 패턴 검색
    pattern_users = db.query(User).filter(User.name.like("%BE%")).all()
    print("패턴 검색 사용자:", pattern_users)

    # 대량 UPDATE
    if pattern_users:
        for user in pattern_users:
            user.name = user.name + "_Updated"
        db.commit()
        print("대량 사용자 수정:", pattern_users)

    # 대량 DELETE
    db.query(User).delete()
    db.commit()
    print("대량 사용자 삭제 완료")

    db.close()

if __name__ == "__main__":
    #run_single()
    run_bulk()# 대량 작업 함수