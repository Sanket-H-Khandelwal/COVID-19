import requests
import sqlite3
from utils import data_processor
import multiprocessing

# Initial step to create a db
# will not override table only create if there is none
conn = sqlite3.connect('covid.db')
c = conn.cursor()
# job to log the name of county tables created
try:
    c.execute('''CREATE TABLE county_tables
                 (county_db_name text, county_name text, created_date timestamp)''')

    conn.commit()
except sqlite3.OperationalError as e:
    print(str(e))

conn.close()


api = "https://health.data.ny.gov/api/views/xdss-u53e/rows.json?accessType=DOWNLOAD"
r = requests.get(api)
json_data = r.json()

columns = [d["name"] for d in json_data["meta"]["view"]["columns"]]
data = json_data["data"]

def divide_chunks(l, n): 
    for i in range(0, len(l), n):  
        yield l[i:i + n] 
  


# divine data in 10 batch, batch size can be changed
batch_data = list(divide_chunks(data, 10)) 

    

d = data_processor(columns)
cpu_count = multiprocessing.cpu_count()

if __name__ == '__main__':
    with multiprocessing.Pool(cpu_count) as p:
        p.map(d.data_processor, batch_data)
        print("log : processing done")