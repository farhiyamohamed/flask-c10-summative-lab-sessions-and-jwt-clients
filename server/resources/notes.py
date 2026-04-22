from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from extensions import db
from models import Note

notes_bp = Blueprint("notes", __name__, url_prefix="/notes")


# GET (pagination)
@notes_bp.get("/")
@jwt_required()
def get_notes():
    user_id = get_jwt_identity()
    page = request.args.get("page", 1, type=int)

    notes = Note.query.filter_by(user_id=user_id).paginate(page=page, per_page=5)

    return jsonify([
        {
            "id": n.id,
            "title": n.title,
            "content": n.content
        } for n in notes.items
    ])


# CREATE
@notes_bp.post("/")
@jwt_required()
def create_note():
    user_id = get_jwt_identity()
    data = request.get_json()

    note = Note(
        title=data["title"],
        content=data["content"],
        user_id=user_id
    )

    db.session.add(note)
    db.session.commit()

    return jsonify({"message": "Note created"}), 201


# UPDATE
@notes_bp.patch("/<int:id>")
@jwt_required()
def update_note(id):
    user_id = get_jwt_identity()

    note = Note.query.filter_by(id=id, user_id=user_id).first_or_404()

    data = request.get_json()

    note.title = data.get("title", note.title)
    note.content = data.get("content", note.content)

    db.session.commit()

    return jsonify({"message": "Note updated"})


# DELETE
@notes_bp.delete("/<int:id>")
@jwt_required()
def delete_note(id):
    user_id = get_jwt_identity()

    note = Note.query.filter_by(id=id, user_id=user_id).first_or_404()

    db.session.delete(note)
    db.session.commit()

    return jsonify({"message": "Note deleted"})