from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField, IntegerField
from wtforms import validators


class WorkFormNew(Form):

    student_code_fk = HiddenField()

    work_title = StringField("Title: ",[
                                    validators.DataRequired("Please enter work title."),
                                    validators.length(1, 15, "Code should be from 1 to 15 symbols")
                                 ])

    submit = SubmitField("Save")


