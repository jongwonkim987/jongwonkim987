from flask import Flask
import yaml
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from post_routes import post_bp, init_db, Base


def load_config(path: str = "db.yaml") -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def create_app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "dev-secret-key"  # 폼/flash 등에 사용 가능

    cfg = load_config("db.yaml")
    db_url = cfg["db"]["url"]
    echo = bool(cfg["db"].get("echo", False))

    # SQLAlchemy 엔진/세션 팩토리
    engine = create_engine(db_url, echo=echo, future=True)
    SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

    # 테이블 생성(없으면 생성)
    Base.metadata.create_all(engine)

    # blueprint에 DB 세션 팩토리 주입
    init_db(SessionLocal)

    # 라우트 등록
    app.register_blueprint(post_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
