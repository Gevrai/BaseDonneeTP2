BEGIN
  --Bye Tables!
  FOR i IN (SELECT ut.table_name
              FROM USER_TABLES ut) LOOP
    EXECUTE IMMEDIATE 'truncate table '|| i.table_name;
  END LOOP;

END;