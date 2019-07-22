from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators


class StudentForm(Form):

   student_code = HiddenField()


   student_name = StringField("Name: ",[
                                 validators.DataRequired("Please enter your name."),
                                 validators.Length(1, 10, "Name should be from 1 to 10 symbols")
                                 ])


   submit = SubmitField("Save")


