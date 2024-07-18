#Sync user.auth und profile zwischen zwei postgres datenbanken



import psycopg2
from collections import namedtuple

def select_single(connection,query):
    print("Select_single query {}".format(query))
    cur = connection.cursor()
    cur.execute(query)
    row = cur.fetchone()
    connection.commit()

    return row

def create_record(obj, fields):
    ''' given obj from db returns named tuple with fields mapped to values '''
    Record = namedtuple("Record", fields)
    mappings = dict(zip(fields, obj))
    return Record(**mappings)

def select_all(connection,query):
    cur = connection.cursor()

    cur.execute(query)
    colnames = [desc[0] for desc in cur.description]
    rows = cur.fetchall()
    for row in rows:
        print("Rows "+str(row['id']))
    return rows

def insert(connection,query):
    cur = connection.cursor()
    cur.execute(query)
    connection.commit()
    cur.close()


connection_source = psycopg2.connect(database = "profilewebsite",
                        user = "profilewebsite",
                        host= '127.0.0.1',
                        password = "12345678",
                        port = 5432)

connection_target = psycopg2.connect(database = "profilewebsite_2",
                        user = "profilewebsite",
                        host= '127.0.0.1',
                        password = "12345678",
                        port = 5432)

auth_user_source = select_all(connection_source,'select id,date_joined from auth_user;')
for auth_user_source_entry in auth_user_source:
    auth_user_target = select_single(connection_target,"select * from auth_user where id = {};".format(str(auth_user_source_entry[0])))
    if auth_user_target is None:
        #Insert row into target
        #print("Insert "+str(auth_user_source_entry['date_joined']))
        pass
    else:
        #Vergleiche die Timestamps und übertrage die neueste Version
        print("Halo")
