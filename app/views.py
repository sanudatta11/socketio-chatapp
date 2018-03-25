from flask import render_template, session, redirect, request, url_for
from flask_socketio import emit, join_room, leave_room
from app import app,socketio
from app.forms import LoginForm, ChatroomForm

messageMap = {}
roomMap = {}
roomArray = []
usersCount = 0

@app.route('/',methods=['GET','POST'])
def index():
    form = LoginForm()
    if form.validate_on_submit():
        session['name'] = form.name.data
        return redirect(url_for('chatrooms'))
    elif request.method == 'GET':
        form.name.data = session.get('name', '')
    return render_template('index.html', form=form)

@app.route('/chatrooms',methods=['GET','POST'])
def chatrooms():
    name = session.get('name', '')
    form = ChatroomForm()
    if name == '':
        return redirect(url_for('index'))
    if form.validate_on_submit():
        room = form.room.data
        session['room'] = room
        return redirect('/chat/'+ room)
    return render_template('chatroom.html',name=name,rooms=roomArray,form=form)

@app.route('/chat/', defaults={'room': None},methods=['GET','POST'])
@app.route('/chat/<room>',methods=['GET','POST'])
def chat(room):
    name = session.get('name', '')
    if room is None:
        room = session.get('room', '')
    else:
        session['room'] = room
    if name == '' or room == '':
        return redirect(url_for('index'))
    return render_template('chat.html', name=name, room=room)


# Socket Views

@socketio.on('joined', namespace='/chat')
def joined(message):
    """Sent by clients when they enter a room.
    A status message is broadcast to all people in the room."""
    global usersCount
    room = session.get('room')
    if room not in roomMap:
        roomArray.append(room)
        roomMap[room] = True
    join_room(room)
    emit('status', {'msg': session.get('name') + ' has entered the room.'}, room=room,broadcast=True)
    if room in messageMap:
        tempArray = messageMap[room][-50:]
        emit('messageHistory', {'msgList': tempArray}, room=room)
    else:
        emit('doneHistory',{'done' : 'true'},room=room)
    usersCount += 1

@socketio.on('text', namespace='/chat')
def text(message):
    """Sent by a client when the user entered a new message.
    The message is sent to all people in the room."""
    room = session.get('room')
    tempObj = {}
    if(room not in messageMap):
        messageMap[room] = []
    tempString = session.get('name') + ':' + message['msg']
    messageMap[room].append(tempString)
    emit('message', {'msg': session.get('name') + ':' + message['msg']}, room=room)


@socketio.on('left', namespace='/chat')
def left(message):
    """Sent by clients when they leave a room.
    A status message is broadcast to all people in the room."""
    global usersCount
    room = session.get('room')
    leave_room(room)
    if(usersCount > 0):
        usersCount -= 1
    emit('status', {'msg': session.get('name') + ' has left the room.'}, room=room)
