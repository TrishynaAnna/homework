from flask_wtf import Form
from wtforms import StringField,   SubmitField,  PasswordField, DateField, HiddenField
from wtforms import validators
from datetime import date
from wtforms_components import DateRange


class HotelForm(Form):

   hotel_id = HiddenField()


   renavation_date = DateField("Date: ", [
                                 validators.DataRequired("Please enter renavation date."),
                                 DateRange(min = date.today())
   ])


   hotel_address = StringField("Address: ",[
                                 validators.DataRequired("Please enter hotel address."),
                                 validators.Length(3, 10, "mark should be from 3 to 10 symbols")
                                 ])


   submit = SubmitField("Save")


