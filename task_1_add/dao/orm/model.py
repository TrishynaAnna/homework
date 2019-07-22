from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

Base = declarative_base()


class ormStudent(Base):
    __tablename__ = 'orm_student'

    student_code = Column(Integer, primary_key=True)
    student_name = Column(String(10), nullable=False)
    Student_has_works = relationship("ormWorks", backref="works")



class ormWorks(Base):
    __tablename__ = 'orm_works'

    work_title = Column(String(10), primary_key=True)
    student_code_fk = Column(Integer, ForeignKey('orm_student.student_code'), nullable=False)

    Attempts_of_student_with_work = relationship("ormAttempts", backref = "attempts")


class ormAttempts(Base):
    __tablename__ = 'orm_attempts'

    work_title_fk = Column(String(10), ForeignKey('orm_works.work_title'), primary_key=True)
    mark_date = Column(Date, primary_key=True)
    mark_value = Column(Integer, nullable=True)




# ormStudent.orm_works = relationship("ormWorks", back_populates = "Student_has_works")
# ormWorks.orm_attempts = relationship("ormAttempts", back_populates = "Attempts_of_student_with_work")