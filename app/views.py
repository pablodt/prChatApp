from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user
from .models import Room, User, Membership
from . import database
import random

views = Blueprint("views", __name__)


@views.route("/")
def home():
    return render_template("home.html")


@views.route("/index")
@login_required
def index():
    return render_template("index.html", name=current_user.username)


@views.route("/create-room", methods=['GET', 'POST'])
@login_required
def create_room():
    if request.method == 'POST':
        name = request.form.get('room_name')

        if not name:
            flash('Name cannot be empty', category='error')
        else:
            rdm = random.randint(1000, 9999)
            while Room.query.filter_by(code=rdm).first():
                rdm = random.randint(1000, 9999)

            room = Room(name=name, creator=current_user.id, code=rdm)
            database.session.add(room)
            database.session.commit()

            flash('Room created', category='success')

            return redirect(url_for('views.chat', code=room.code))

    return render_template("create.html", name=current_user.username)


@views.route("/room/<code>", methods=['GET', 'POST'])
@login_required
def chat(code):
    room = Room.query.filter_by(code=code).first()

    return render_template("chat.html", room_name=room.name, name=current_user.username, room_id=room.id, user_id=current_user.id)


@views.route("/room/<code>/delete", methods=['GET', 'POST'])
@login_required
def delete_room(code):
    room = Room.query.filter_by(code=code).first()

    if current_user.id == room.creator:
        Room.query.filter_by(code=code).delete()
        database.session.commit()
    else:
        flash('You are not the creator', category='error')

    return redirect(url_for('views.my_rooms'))


@views.route("/join-room", methods=['GET', 'POST'])
@login_required
def join_room():
    if request.method == 'POST':
        code = request.form.get('room_code')

        if not code:
            flash('Code cannot be empty', category='error')
        else:
            room = Room.query.filter_by(code=code).first()

            if room.creator == current_user.id:
                flash('This room is yours', category='error')
                return redirect(url_for('views.chat', code=code))
            else:
                if Membership.query.filter_by(user_id=current_user.id, room_id=room.id).first():
                    flash('You have already joined this room', category='error')
                    return redirect(url_for('views.chat', code=code))
                else:
                    membership = Membership(room_id=room.id, user_id=current_user.id)
                    database.session.add(membership)
                    database.session.commit()
                    flash('Joined successfully', category='success')
                    return redirect(url_for('views.chat', code=code))

    return render_template("join.html", name=current_user.username)


@views.route("/my-rooms", methods=['GET', 'POST'])
@login_required
def my_rooms():
    if request.method == 'POST':
        print(request.form.get('rooms'))
    rooms = Room.query.filter_by(creator=current_user.id)
    users = User.query.all()
    memberships = Membership.query.filter_by(user_id=current_user.id)
    rooms2 = []

    for membership in memberships:
        rooms2.append(Room.query.filter_by(id=membership.room_id).first())

    return render_template("rooms.html", name=current_user.username, rooms=rooms, users=users, rooms2=rooms2,
                           user_id=current_user.id)