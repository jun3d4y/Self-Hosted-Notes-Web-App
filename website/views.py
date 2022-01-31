from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from sqlalchemy import desc

from .models import Note

views = Blueprint("views", __name__)

@views.route("/")
@login_required
def home() :
    note = Note.query.filter_by(user_id=current_user.id).order_by(desc(Note.modification_datetime)).first()
    if note is not None :
        return redirect(url_for('views.note', string_id=note.string_id))
    notes = Note.query.filter_by(user_id=current_user.id).order_by(desc(Note.modification_datetime)).all()
    return render_template("notes.html", notes=notes)

@views.route("/iframe")
def iframe() :
    return render_template("base.html")

@views.route("/note/<string_id>")
@login_required
def note(string_id) :
    note = Note.query.filter_by(user_id=current_user.id, string_id=string_id).first()
    if note is not None :
        notes = Note.query.filter_by(user_id=current_user.id).order_by(desc(Note.modification_datetime)).all()
        return render_template("notes.html", string_id=note.string_id, title=note.title, content=note.content, notes=notes)

    return render_template("404.html"), 404
