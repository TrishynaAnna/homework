from task_1_add.dao.orm.model import *
from task_1_add.dao.db import OracleDb


db = OracleDb()

Base.metadata.create_all(db.sqlalchemy_engine)

session = db.sqlalchemy_session

# clear all tables in right order
session.query(ormAttempts).delete()
session.query(ormWorks).delete()
session.query(ormStudent).delete()

session.commit()

# populate database with new rows

Anna = ormStudent(student_name="Anna")

Cap = ormStudent(student_name= "Cap")

Java = ormWorks(work_title = 'Java',
                works=Anna)

Oracle = ormWorks(work_title='Oracle',
                  works=Cap)


Anna_mark = ormAttempts(mark_date = '20-06-2019',
                   mark_value=12,
                    attempts=Java)


Cap_mark = ormAttempts(attempts=Oracle,
                   mark_date = '27-06-2019',
                   mark_value=11)

# insert into database
session.add_all([Anna,Cap,Java,Oracle,Anna_mark,Cap_mark])

session.commit()