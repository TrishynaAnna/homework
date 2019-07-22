create or replace package update_hotel is

    procedure upd_hotel(
                            hotel_id_ in hotel.hotel_id%TYPE,
                            renavation_date_ in hotel.renavation_date%TYPE,
                            hotel_address_ in hotel.hotel_address%TYPE
                            );

end update_hotel;


create or replace PACKAGE BODY update_hotel is

     procedure upd_hotel(
                            hotel_id_ in hotel.hotel_id%TYPE,
                            renavation_date_ in hotel.renavation_date%TYPE,
                            hotel_address_ in hotel.hotel_address%TYPE
                            )
     is
     begin

         BEGIN
            UPDATE hotel SET renavation_date =renavation_date_, hotel_address = hotel_address_ WHERE hotel_id = hotel_id_;

            COMMIT;
         END;
     end upd_hotel;

end update_hotel;