import sqlite3
import datetime


class data_processor:
    def __init__(self, columns):
        
        self.columns = columns

    def data_processor(self, data=[]):
        conn = sqlite3.connect('covid.db')
        c = conn.cursor()

        for row in data:
            county_name = row[9]
            table_name = county_name.lower().replace(" ", "_").replace(".", "_")
            d1 = datetime.datetime.strptime(row[8],"%Y-%m-%dT%H:%M:%S")
            sql_statement = "INSERT INTO " + table_name + " VALUES ("
            sql_statement = sql_statement + "'" +str(d1) + "' ," 
            sql_statement += str(row[10]) + " ," 
            sql_statement += str(row[11]) + " ," 
            sql_statement += str(row[12]) + " ," 
            sql_statement += str(row[13]) + " ," 
            sql_statement = sql_statement + "'" + str(datetime.datetime.now()) + "' )" 
            
            try:
                c.execute(sql_statement)

            except sqlite3.OperationalError:

                # if other batch already created this table
                # note: records will be not duplicated as the batches are unique
                try:
                    sql_log_table_insert_statement = "INSERT INTO county_tables VALUES ('{}','{}', '{}')".format(table_name, county_name, str(datetime.datetime.now())) 
                    sql_insert_statement = "CREATE TABLE " + table_name + " (test_date timestamp, num_pos real, cumm_case real, total_test real, cumm_test real, load_date timestamp) "
                    c.execute(sql_log_table_insert_statement)
                    c.execute(sql_insert_statement)
                    print("log : created table " + table_name , datetime.datetime.now())
                except:
                    continue
                c.execute(sql_statement)
            except:
                print("log : error inserting rec" + str(data))
                return False
        
        conn.commit()
        conn.close()

        return True