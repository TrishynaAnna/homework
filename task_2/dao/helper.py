from task_2.dao.credentials import *
import cx_Oracle


class Helper:

    def __init__(self):
        self.db = cx_Oracle.connect(username, password, databaseName)

    def Update_hotel(self, hotel_id, renavation_date, hotel_address):
        cursor = self.db.cursor()

        cursor.callproc("update_hotel.upd_hotel", [hotel_id, renavation_date.strftime("%d.%m.%Y"), hotel_address])

        cursor.close()
        return

    def Get_hotel(self, hotel_id=None):

        cursor = self.db.cursor()

        if hotel_id:
            query = 'SELECT * FROM "HOTEL" WHERE hotel_id = '+hotel_id
        else:
            query = 'SELECT * FROM "HOTEL"'
        cursor.execute(query)
        result = cursor.fetchall()

        cursor.close()
        # self.db.close()

        return result




if __name__ == "__main__":

    helper = Helper()
