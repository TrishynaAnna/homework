from task_1_add.dao.db import OracleDb


class UserHelper:

    def __init__(self):
        self.db = OracleDb()

    def getWorks(self, mark_value=None, work_title=None):

        if mark_value and work_title:
            data="'{0}', '{1}'".format(mark_value, work_title)
        elif mark_value:
            data = "'{0}', null".format(mark_value)
        elif work_title:
            data = "null, '{0}'".format(work_title)
        else:
            data="null, null"

        query = "select * from table(orm_workwers_attempts.GetStudentsNames({0}))".format(data)

        result = self.db.execute(query)
        return result.fetchall()




if __name__ == "__main__":

    helper = UserHelper()

    print(helper.getWorks('Java'))
    print(helper.getWorks())
