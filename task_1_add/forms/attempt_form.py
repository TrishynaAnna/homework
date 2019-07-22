from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators


class AttemptForm(Form):

   work_title_fk = HiddenField()


   mark_date = HiddenField()


   mark_date_new = DateField("Date: ")


   mark_value = StringField("Mark: ",[
                                 validators.DataRequired("Please enter mark."),
                                 validators.Length(1, 3, "mark should be from 1 to 3 symbols")
                                 ])


   submit = SubmitField("Save")


