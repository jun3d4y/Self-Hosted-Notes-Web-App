from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user

from .randomString import get_random_string
from .models import Note
from .__init__ import db

api = Blueprint("api", __name__)


@api.route("/")
def home() :

    return jsonify({"version": "1.0.0"})

@api.route("/create", methods=['POST'])
@login_required
def create() :
    try :
        string_id = get_random_string()
        new_note = Note(user_id=current_user.id, string_id=string_id)
        db.session.add(new_note)
        db.session.commit()
        return jsonify({"status": "1", "string_id": string_id})
    except :
        return jsonify({"status": "0"})

@api.route("/delete", methods=["POST"])
@login_required
def delete() :
    string_id = request.json["string_id"]
    print(string_id)
    if string_id is not None :
        note = Note.query.filter_by(user_id=current_user.id, string_id=string_id)
        if note is not None :
            try :
                note.delete()
                db.session.commit()
                return jsonify({"status": "1"})
            except :
                return jsonify({"status": "0"})

    return jsonify({"status": "0"})

@api.route("/get_hash", methods=["POST"])
@login_required
def get_hash() :
    string_id = request.json["string_id"]

    if string_id is not None :
        note = Note.query.filter_by(user_id=current_user.id, string_id=string_id).first()
        if note is not None :
            return jsonify({"status": "1", "hash": note.hash})
    return jsonify({"status": "0"})

@api.route("/save", methods=["POST"])
@login_required
def save() :
    string_id = request.json["string_id"]
    title = request.json["title"]
    content = request.json["content"]
    new_hash = request.json["hash"]

    if string_id is not None and title is not None and content is not None :
        note = Note.query.filter_by(user_id=current_user.id, string_id=string_id).first()
        if note is not None :
            try :
                note.hash = new_hash
                note.title = title
                note.content = content
                db.session.commit()
                return jsonify({"status": "1"})
            except :
                return jsonify({"status": "0"})

    return jsonify({"status": "0"})
