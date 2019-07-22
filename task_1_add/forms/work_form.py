from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class WorkForm(Form):
    work_title = HiddenField()

    student_code_fk = IntegerField("Code: ", [
        validators.DataRequired("Please enter student code."),
        validators.NumberRange(1, 99999, "Code should be from 1 to 99999 symbols")
    ])



    submit = SubmitField("Save")


