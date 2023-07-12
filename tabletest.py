import psycopg2 as psy
from datetime import datetime
import time

def create_board_table(serial):
    command = "CREATE TABLE IF NOT EXISTS " + str(serial) + "( dt TIMESTAMP NOT NULL, lut TEXT NOT NULL );"
    try:
        conn = psy.connect(database='play',user='phnxrc')
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psy.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def insert_lut(serial, lut):
    dat = str(datetime.now()).split(".")[0]
    command = "INSERT INTO " + serial + " (dt, lut) VALUES ('" + dat + "', '" + lut + "');"
    try:
        conn = psy.connect(database='play',user='phnxrc')
        cur = conn.cursor()
        cur.execute(command)
        cur.close()
        conn.commit()
    except (Exception, psy.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def get_recent_lut(serial):
    command = "SELECT * from " + serial + " ORDER BY dt DESC LIMIT 1;"
    lut = ""
    try:
        conn = psy.connect(database='play',user='phnxrc')
        cur = conn.cursor()
        cur.execute(command)
        lut = cur.fetchone()[1]
    except (Exception, psy.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return lut
    
def get_lut(serial, date):
    lut = ""
    if date == 0:
        return get_recent_lut(serial)
    command = "SELECT * from " + serial + " WHERE dt LIKE " + date + " LIMIT 1;"
    try:
        conn = psy.connect(database='play',user='phnxrc')
        cur = conn.cursor()
        cur.execute(command)
        lut = cur.fetchone()[1]
    except (Exception, psy.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return lut

def get_all_lut(serial):
    command = "SELECT * from " + serial + " ORDER BY dt DESC;"
    lut = ""
    try:
        conn = psy.connect(database='play',user='phnxrc')
        cur = conn.cursor()
        cur.execute(command)
        lut = cur.fetchall()
    except (Exception, psy.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return lut

def insert_lut_from_file(serial, filename):
    lut = []
    lutstr = ""
    with open(filename,"r") as thefile:
        for line in thefile:
            lut.append(line.strip())
    for i in range(len(lut)-1):
        lutstr += (lut[i] + ",")
    lutstr += lut[-1]
    insert_lut(serial, lutstr)

def lut_to_file(serial, filename, date):
    lutstr = get_lut(serial, date)
    lut = lutstr.split(",")
    with open(filename, "w") as thefile:
        for value in lut:
            thefile.write(value + "\n")

#create_board_table("E169000")
#insert_lut("E169000","0,1,2,3,4,5,6")
#time.sleep(10)
#insert_lut("E169000","0,1,2,3,4,5,6,7")
#insert_lut_from_file("E169000","testlut.txt")
#print(get_recent_lut("E169000"))
#print(get_all_lut("E169000"))
lut_to_file("E169000","testout.txt",0)
