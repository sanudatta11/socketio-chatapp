from flask_wtf import Form
from wtforms.fields import StringField, SubmitField
from wtforms.validators import DataRequired


# Used for providing a nick to the person
class LoginForm(Form):
    name = StringField('Name',[DataRequired()])
    submit = SubmitField('Save Name')

class ChatroomForm(Form):
    room = StringField('ChatRoom',[DataRequired()])
    submit = SubmitField('Enter Chatroom')