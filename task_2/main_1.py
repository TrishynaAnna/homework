from flask import Flask, render_template, request, redirect, url_for
from task_2.dao.helper import *
from task_2.forms.hotel_form import HotelForm

import json

app = Flask(__name__)
app.secret_key = 'development key'




@app.route('/', methods=['GET', 'POST'])
def root():
    form = HotelForm()
    helper = Helper()
    hotels_data = helper.Get_hotel()
    return render_template('hotel.html', form = form, hotels = hotels_data)




@app.route('/edit_hotel/<value>', methods=['GET'])
def edit_hotel(value):
    print(value)
    form = HotelForm()
    helper = Helper()
    hotels_data = helper.Get_hotel(value)

    form.hotel_id.data = hotels_data[0][0]
    form.renavation_date.data = hotels_data[0][1]
    form.hotel_address.data = hotels_data[0][2]

    return render_template('hotel_form.html', form=form, form_name="Edit hotel", action="save_hotel")


@app.route('/save_hotel', methods=['GET', 'POST'])
def save_hotel():
    form = HotelForm()

    if form.validate() == False:
        return render_template('hotel_form.html', form=form, form_name="Edit hotel", action="save_hotel")
    else:

        helper = Helper()
        helper.Update_hotel(form.hotel_id.data, form.renavation_date.data, form.hotel_address.data)

        return redirect(url_for('root'))



if __name__ == '__main__':
    app.run(debug=True)