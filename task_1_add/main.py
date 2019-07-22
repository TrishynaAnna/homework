from flask import Flask, render_template, request, redirect, url_for
from task_1_add.forms.search_form import SearchForm
from task_1_add.dao.orm.model import *
from task_1_add.dao.db import OracleDb
from task_1_add.forms.work_form import WorkForm
from task_1_add.forms.work_form_new import WorkFormNew
from task_1_add.forms.attempt_form import AttemptForm
from task_1_add.forms.student_form import StudentForm
from sqlalchemy.sql import func
from datetime import datetime

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import json

app = Flask(__name__)
app.secret_key = 'development key'




@app.route('/', methods=['GET', 'POST'])
def root():

    return render_template('index.html')




@app.route('/student', methods=['GET'])
def student():

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormStudent).all()

    return render_template('student.html', students = result)


@app.route('/work', methods=['GET'])
def work():

    db = OracleDb()

    #result = db.sqlalchemy_session.query(ormWorks).join(ormStudent).all()
    result = db.sqlalchemy_session.query(ormWorks).all()

    return render_template('work.html', works = result)


@app.route('/attempt', methods=['GET'])
def attempt():

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormAttempts).all()

    return render_template('attempt.html', attempts = result)


@app.route('/search', methods=['GET', 'POST'])
def search():

    search_form = SearchForm()

    if request.method=='GET':
        return render_template('search.html', form = search_form, result=None)
    else:
        return render_template('search.html', form = search_form, result=search_form.get_result())


@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():

    db = OracleDb()


    # SELECT
    #   orm_works.work_title, COUNT(orm_works.student_code_fk)
    # FROM ORM_WORKS JOIN ORM_ATTEMPTS
    #   ON orm_works.work_title = orm_attempts.work_title_fk
    # GROUP BY orm_works.work_title

    query1  = (
                db.sqlalchemy_session.query(
                                            ormWorks.work_title,
                                            func.count(ormWorks.student_code_fk).label('attempts_count')
                                          ).\
                                    outerjoin(ormAttempts).\
                                    group_by(ormWorks.work_title)
               ).all()


    # SELECT
    #   orm_student.student_name,
    #   COUNT(orm_works.work_title)
    # FROM ORM_STUDENT JOIN ORM_WORKS
    #   ON orm_student.student_code = orm_works.student_code_fk
    # GROUP BY orm_student.student_name

    query2 = (
        db.sqlalchemy_session.query(
            ormStudent.student_name,
            func.count(ormWorks.work_title).label('works_count')
        ). \
            outerjoin(ormWorks). \
            group_by(ormStudent.student_name)
    ).all()




    title, attempts_count = zip(*query1)
    bar = go.Bar(
        x=title,
        y=attempts_count
    )

    name, works_count = zip(*query2)
    pie = go.Pie(
        labels=name,
        values=works_count
    )



    data = {
                "bar":[bar],
                "pie":[pie]
           }
    graphsJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return render_template('dashboard.html', graphsJSON=graphsJSON)

#     =================================================================================================


@app.route('/new_student', methods=['GET','POST'])
def new_student():

    form = StudentForm()


    if request.method == 'POST':
        if form.validate() == False:
            return render_template('student_form.html', form=form, form_name="New student", action="new_student")
        else:
            new_student= ormStudent(
                                student_name = form.student_name.data
                            )
            db = OracleDb()
            db.sqlalchemy_session.add(new_student)
            db.sqlalchemy_session.commit()


            return redirect(url_for('student'))

    return render_template('student_form.html', form=form, form_name="New student", action="new_student")



@app.route('/edit_student', methods=['GET','POST'])
def edit_student():

    form = StudentForm()


    if request.method == 'GET':

        student_code =request.args.get('student_code')
        db = OracleDb()
        student = db.sqlalchemy_session.query(ormStudent).filter(ormStudent.student_code == student_code).one()

        # fill form and send to user
        form.student_code.data = student.student_code
        form.student_name.data = student.student_name

        return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")


    else:

        if form.validate() == False:
            return render_template('student_form.html', form=form, form_name="Edit student", action="edit_student")
        else:
            db = OracleDb()
            # find user
            student = db.sqlalchemy_session.query(ormStudent).filter(ormStudent.student_code == form.student_code.data).one()

            # update fields from form data
            student.student_code = form.student_code.data
            student.student_name = form.student_name.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('student'))





@app.route('/delete_student', methods=['POST'])
def delete_student():

    student_code = request.form['student_code']

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormStudent).filter(ormStudent.student_code ==student_code).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()


    return student_code


@app.route('/new_work', methods=['GET','POST'])
def new_work():

    form = WorkFormNew()


    if request.method == 'GET':

        student_code =request.args.get('student_code')

        form.student_code_fk.data = student_code

        return render_template('work_form.html', form=form, form_name="New work", action="new_work")

    else:
        db = OracleDb()
        student = len(db.sqlalchemy_session.query(ormWorks).filter(ormWorks.work_title == form.work_title.data).all())

        if form.validate() == False:
            return render_template('work_form.html', form=form, form_name="New work", action="new_work")
        elif student != 0:
            form.work_title.data = ""
            return render_template('work_form.html', form=form, form_name="New work", action="new_work")
        else:
            new_work= ormWorks(
                                work_title=form.work_title.data,
                                student_code_fk = form.student_code_fk.data
                            )
            db = OracleDb()
            db.sqlalchemy_session.add(new_work)
            db.sqlalchemy_session.commit()


            return redirect(url_for('work'))

    return render_template('work_form.html', form=form, form_name="New work", action="new_work")



@app.route('/edit_work', methods=['GET','POST'])
def edit_work():

    form = WorkForm()

    if request.method == 'GET':

        work_title = request.args.get('work_title')
        db = OracleDb()
        work = db.sqlalchemy_session.query(ormWorks).filter(ormWorks.work_title == work_title).one()

        # fill form and send to user
        form.work_title.data = work.work_title
        form.student_code_fk.data = work.student_code_fk

        return render_template('work_form.html', form=form, form_name="Edit work", action="edit_work")


    else:
        db = OracleDb()
        student = len(db.sqlalchemy_session.query(ormStudent).filter(ormStudent.student_code == form.student_code_fk.data).all())

        if form.validate() == False:
            return render_template('work_form.html', form=form, form_name="Edit work", action="edit_work")
        elif student == 0:
            form.student_code_fk.data = ""
            return render_template('work_form.html', form=form, form_name="Edit work", action="edit_work")
        else:
            db = OracleDb()
            # find user
            work = db.sqlalchemy_session.query(ormWorks).filter(ormWorks.work_title == form.work_title.data).one()

            # update fields from form data
            work.work_title = form.work_title.data
            work.student_code_fk = form.student_code_fk.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('work'))





@app.route('/delete_work', methods=['POST'])
def delete_work():

    work_title = request.form['work_title']

    db = OracleDb()

    result = db.sqlalchemy_session.query(ormWorks).filter(ormWorks.work_title == work_title).one()

    db.sqlalchemy_session.delete(result)
    db.sqlalchemy_session.commit()


    return work_title


@app.route('/new_attempt', methods=['GET','POST'])
def new_attempt():

    form = AttemptForm()


    if request.method == 'GET':

        work_title =request.args.get('work_title')

        form.work_title_fk.data = work_title

        return render_template('attempt_form.html', form=form, form_name="New attempt", action="new_attempt")

    else:
        db = OracleDb()
        student = len(db.sqlalchemy_session.query(ormAttempts).filter(ormAttempts.work_title_fk == form.work_title_fk.data)
                      .filter(ormAttempts.mark_date == form.mark_date_new.data).all())

        if form.validate() == False:
            return render_template('attempt_form.html', form=form, form_name="New attempt", action="new_attempt")
        elif student != 0:
            form.mark_date_new.data = ""
            return render_template('attempt_form.html', form=form, form_name="New attempt", action="new_attempt")
        else:
            new_attempt= ormAttempts(
                                work_title_fk=form.work_title_fk.data,
                                mark_date = form.mark_date_new.data,
                                mark_value = form.mark_value.data
                            )
            db = OracleDb()
            db.sqlalchemy_session.add(new_attempt)
            db.sqlalchemy_session.commit()


            return redirect(url_for('attempt'))

    return render_template('attempt_form.html', form=form, form_name="New attempt", action="new_attempt")



@app.route('/edit_attempt', methods=['GET','POST'])
def edit_attempt():

    form = AttemptForm()

    if request.method == 'GET':

        work_title_fk = request.args.get('work_title_fk')
        mark_date = datetime.strptime(request.args.get('mark_date'), '%Y-%m-%d').strftime('%d.%m.%y')
        db = OracleDb()
        arrempt = db.sqlalchemy_session.query(ormAttempts).filter(ormAttempts.work_title_fk == work_title_fk).filter(ormAttempts.mark_date == mark_date).one()

        # fill form and send to user
        form.work_title_fk.data = arrempt.work_title_fk
        form.mark_date.data = arrempt.mark_date
        form.mark_value.data = arrempt.mark_value

        return render_template('attempt_form.html', form=form, form_name="Edit attempt", action="edit_attempt")


    else:

        if form.validate() == False:
            return render_template('attempt_form.html', form=form, form_name="Edit attempt", action="edit_attempt")
        else:
            db = OracleDb()
            # find user

            mark_date = datetime.strptime(form.mark_date.data, '%Y-%m-%d').strftime('%d.%m.%y')
            arrempt = db.sqlalchemy_session.query(ormAttempts).filter(
                ormAttempts.work_title_fk == form.work_title_fk.data).filter(ormAttempts.mark_date == mark_date).one()

            # update fields from form data
            arrempt.work_title_fk = form.work_title_fk.data
            arrempt.mark_date = mark_date
            arrempt.mark_value = form.mark_value.data

            db.sqlalchemy_session.commit()

            return redirect(url_for('attempt'))





@app.route('/delete_attempt', methods=['POST'])
def delete_attempt():
    work_title_fk = request.form['work_title_fk']
    mark_date = datetime.strptime(request.form['mark_date'], '%Y-%m-%d').strftime('%d.%m.%y')
    db = OracleDb()
    arrempt = db.sqlalchemy_session.query(ormAttempts).filter(ormAttempts.work_title_fk == work_title_fk).filter(
        ormAttempts.mark_date == mark_date).one()

    db.sqlalchemy_session.delete(arrempt)
    db.sqlalchemy_session.commit()


    return work_title_fk



if __name__ == '__main__':
    app.run(debug=True)