from flask_smorest import Blueprint, abort
from flask.views import MethodView
from schemas import BookSchema

blp = Blueprint("books", "books", url_prefix="/books", description="Operations on books")

books = []
current_id = 1

@blp.route("/")
class BookList(MethodView):
    @blp.response(200, BookSchema(many=True))
    def get(self):
        return books
    @blp.arguments(BookSchema)
    @blp.response(201, BookSchema)
    def get(self, new_data):
        global current_id
        new_data["id"] = current_id
        books.append(new_data)
        current_id += 1
        return new_data

@blp.route("/<int:book_id>")
class Book(MethodView):
    @blp.arguments(BookSchema)
    @blp.response(200, BookSchema)
    def put(self, update_data, book_id):
        book = next((b for b in books if b["id"] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        book.update(update_data)
        return book

    @blp.response(200, description="Deletes a book")
    def delete(self, book_id):
        global books
        book = next((b for b in books if b["id"] == book_id), None)
        if book is None:
            abort(404, message="Book not found")
        books = [b for b in books if b["id"] != book_id]
        return {"message": "Book deleted"}, 200