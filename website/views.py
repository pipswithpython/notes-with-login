from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        note = request.form.get('note')
        if not note or len(note) < 1:
            flash('Note is too short!', category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash('Note added!', category='success')
    return render_template('home.html', user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():
    data = request.json
    note_id = data.get('noteId')
    
    if not note_id:
        return jsonify({'error': 'Note ID is required.'}), 400
    
    try:
        note_id = int(note_id)
    except ValueError:
        return jsonify({'error': 'Invalid Note ID.'}), 400

    note = Note.query.get(note_id)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
            return jsonify({'message': 'Note deleted successfully.'}), 200
        else:
            return jsonify({'error': 'Unauthorized access.'}), 403
    return jsonify({'error': 'Note not found.'}), 404
