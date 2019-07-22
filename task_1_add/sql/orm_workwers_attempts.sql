CREATE OR REPLACE PACKAGE orm_workwers_attempts IS


    TYPE name_data IS RECORD(
        student_name ORM_STUDENT.STUDENT_NAME%TYPE,
        attempts_count INTEGER
    );


    TYPE tblnamedata IS TABLE OF name_data;

    FUNCTION GetStudentsNames (MARK_VALUE ORM_ATTEMPTS.MARK_VALUE%TYPE default null, WORK_TITLE ORM_WORKS.WORK_TITLE%TYPE default null)
        RETURN tblnamedata
        PIPELINED;

END orm_workwers_attempts;




CREATE OR REPLACE PACKAGE BODY orm_workwers_attempts IS

    FUNCTION GetStudentsNames (MARK_VALUE ORM_ATTEMPTS.MARK_VALUE%TYPE default null, WORK_TITLE ORM_WORKS.WORK_TITLE%TYPE default null)
        RETURN tblnamedata
        PIPELINED
    IS

        TYPE name_cursor_type IS REF CURSOR;
        name_cursor  name_cursor_type;

        cursor_data name_data;
        query_str varchar2(1000);

    begin

        query_str :='select orm_student.student_name, count(orm_works.work_title)
            from ORM_STUDENT JOIN ORM_WORKS ON
            orm_student.student_code = orm_works.student_code_fk
            JOIN ORM_ATTEMPTS ON
            orm_works.work_title = orm_attempts.work_title_fk ';

        -- optional part where
            if MARK_VALUE is not null and WORK_TITLE is not null then
             query_str:= query_str||' where trim(orm_works.work_title) = trim('''||WORK_TITLE||''') AND trim(orm_attempts.mark_value) = trim('''||MARK_VALUE||''') ';

            ELSIF MARK_VALUE is not null then
             query_str:= query_str||' where trim(orm_attempts.mark_value) = trim('''||MARK_VALUE||''') ';

            ELSIF WORK_TITLE is not null then
             query_str:= query_str||' where trim(orm_works.work_title) = trim('''||WORK_TITLE||''') ';
            end if;
        -- end optional part

        query_str := query_str||' GROUP BY orm_student.student_name';



        OPEN name_cursor FOR query_str;
        LOOP
            FETCH name_cursor into cursor_data;
            exit when (name_cursor %NOTFOUND);

            PIPE ROW (cursor_data);

        END LOOP;


    END GetStudentsNames;

END orm_workwers_attempts;
