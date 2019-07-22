from flask_wtf import Form
from wtforms import StringField,   SubmitField
from task_1_add.dao.userhelper import UserHelper

class SearchForm(Form):

    work_title = StringField('Work title: ')
    mark_value = StringField('Mark value: ')

    submit = SubmitField('Search')


    def get_result(self):
        helper = UserHelper()
        return helper.getWorks(self.mark_value.data, self.work_title.data)


