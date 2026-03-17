from flask import Flask, jsonify, request
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
import os

app = Flask(__name__)

# instance 파일 자동 생성/ 데이터베이스 설정
BASE_DIR = os.path.dirname(__file__)
INSTANCE_DIR = os.path.join(BASE_DIR, "todos.db")
os.makedirs(INSTANCE_DIR, exist_ok=True)

DATABASE_URL = f"sqlite:///{os.path.join(INSTANCE_DIR, "todos.db")}"
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# 데이터베이스 모델 정의
class Todo(Base):
    __tablename__ = "todos"
    id = Column(Integer, primary_key=True, index=True)
    task = Column(String, nullable=False)
    def __repr__(self):
        return f"Todo(id={self.id}, task={self.task})"

# 테이블 생성
Base.metadata.create_all(bind=engine)

# READ : 전체 항목 조회
@app.route("/todos", methods=["GET"])
def get_todos():
    db = SessionLocal()
    todos = db.query(Todo).all()
    db.close()
    return jsonify([{todo.id: todo.task} for todo in todos])

# READ : 특정 항목 조회
@app.route("/todos/<int:todo_id>", methods=["GET"])
def get_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)
    db.close()

    if not todo:
        return jsonify({"error": "Todo not found"}), 404
    return jsonify({todo_id: todo.id, "task": todo.task})

# CREATE : 새로운 항목 조회
@app.route("/todos", methods=["POST"])
def create_todo():
    data = request.get_json()
    db = SessionLocal()
    new_todo = Todo(task=data.get("task"))
    db.add(new_todo)
    db.commit()
    db.refresh(new_todo) # 새로 생성된 항목의 ID를 가져오기 위해 새로고침
    db.close()

    return jsonify({"id": new_todo.id, "task": new_todo.task}), 201
    

# UPDATE : 특정 항목 수정
@app.route("/todos/<int:todo_id>", methods=["PUT"])
def update_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)

    if not todo:
        db.close()
        return jsonify({"error": "Todo not found"}), 404
    
    data = request.get_json()
    todo.task = data["task"]
    db.commit()
    updated = {"id": todo.id, "task": todo.task}
    db.close()
    return jsonify(updated)

# DELETE : 특정 항목 삭제
@app.route("/todos/<int:todo_id>", methods=["DELETE"])
def delete_todo(todo_id):
    db = SessionLocal()
    todo = db.query(Todo).get(todo_id)

    if not todo:
        db.close()
        return jsonify({"error": "Todo not found"}), 404
    
    db.delete(todo)
    db.commit()
    db.close()
    return jsonify({"deleted": todo_id}), 204

if __name__ == "__main__":
    app.run(debug=True, port=1004)