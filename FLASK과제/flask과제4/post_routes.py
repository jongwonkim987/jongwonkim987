from __future__ import annotations

from datetime import datetime
from flask import Blueprint, render_template, request, redirect, url_for, abort
from sqlalchemy import String, Text, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

post_bp = Blueprint("posts", __name__)

# ---- SQLAlchemy Base / Model ----
class Base(DeclarativeBase):
    pass

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

# ---- DB Session Factory (app.py에서 주입) ----
_SessionLocal = None

def init_db(session_factory):
    global _SessionLocal
    _SessionLocal = session_factory

def get_session():
    if _SessionLocal is None:
        raise RuntimeError("DB 세션 팩토리가 초기화되지 않았습니다. app.py에서 init_db(SessionLocal)를 호출하세요.")
    return _SessionLocal()

# ---- Routes ----
@post_bp.get("/")
def index():
    with get_session() as db:
        posts = db.query(Post).order_by(Post.id.desc()).all()
    return render_template("index.html", posts=posts)

@post_bp.get("/posts/new")
def new_post():
    return render_template("post_form.html", mode="create", post=None)

@post_bp.post("/posts")
def create_post():
    title = (request.form.get("title") or "").strip()
    content = (request.form.get("content") or "").strip()

    if not title or not content:
        # 간단 처리: 필수값 없으면 작성 폼으로 복귀
        return render_template("post_form.html", mode="create", post={"title": title, "content": content}, error="제목/내용은 필수입니다.")

    with get_session() as db:
        post = Post(title=title, content=content)
        db.add(post)
        db.commit()
        db.refresh(post)

    return redirect(url_for("posts.detail", post_id=post.id))

@post_bp.get("/posts/<int:post_id>")
def detail(post_id: int):
    with get_session() as db:
        post = db.get(Post, post_id)
        if not post:
            abort(404)
    return render_template("post_detail.html", post=post)


@post_bp.get("/posts/<int:post_id>/edit")
def edit_post(post_id: int):
    with get_session() as db:
        post = db.get(Post, post_id)
        if not post:
            abort(404)
    return render_template("post_form.html", mode="edit", post=post)


@post_bp.post("/posts/<int:post_id>/update")
def update_post(post_id: int):
    title = (request.form.get("title") or "").strip()
    content = (request.form.get("content") or "").strip()

    if not title or not content:
        # 수정 폼으로 다시
        return render_template("post_form.html", mode="edit", post={"id": post_id, "title": title, "content": content}, error="제목/내용은 필수입니다.")

    with get_session() as db:
        post = db.get(Post, post_id)
        if not post:
            abort(404)

        post.title = title
        post.content = content
        db.commit()

    return redirect(url_for("posts.detail", post_id=post_id))

@post_bp.post("/posts/<int:post_id>/delete")
def delete_post(post_id: int):
    with get_session() as db:
        post = db.get(Post, post_id)
        if not post:
            abort(404)

        db.delete(post)
        db.commit()

    return redirect(url_for("posts.index"))