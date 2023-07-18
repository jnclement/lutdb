import psycopg2 as psy
from datetime import datetime
import time

def rcs_string(rack, crate, slot):
    return (rack + "_" + str(crate) + "_" +str(slot))

def create_board_table(rack, crate, slot):
    command = "CREATE TABLE IF NOT EXISTS " +  rcs_string(rack, crate, slot) + "( dt TIMESTAMP NOT NULL, lut TEXT NOT NULL, serial TEXT NOT NULL );"
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


def insert_lut(serial, lut, rack, crate, slot):
    dat = str(datetime.now()).split(".")[0]
    command = "INSERT INTO " + rcs_string(rack, crate, slot) + " (dt, lut, serial) VALUES ('" + dat + "', '" + lut + "', '" + serial + "');"
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

def get_recent_lut(rack, crate, slot):
    command = "SELECT * from " + rcs_string(rack, crate, slot) + " ORDER BY dt DESC LIMIT 1;"
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
    
def get_lut(rack, crate, slot, date):
    lut = ""
    if date == 0:
        return get_recent_lut(rack, crate, slot)
    command = "SELECT * from " + rcs_string(rack, crate, slot) + " WHERE dt LIKE " + date + " LIMIT 1;"
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

def get_all_lut(rack, crate, slot):
    command = "SELECT * from " + rcs_string(rack, crate, slot) + " ORDER BY dt DESC;"
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

def file_lut_to_db(serial, filename, rack, crate, slot):
    lut = []
    lutstr = ""
    with open(filename,"r") as thefile:
        for line in thefile:
            lut.append(line.strip())
    for i in range(len(lut)-1):
        lutstr += (lut[i] + ",")
    lutstr += lut[-1]
    insert_lut(serial, lutstr, rack, crate, slot)

def db_lut_to_file(rack, crate, slot, date):
    filename = rcs_string(rack, crate, slot) + "_lut.txt"
    lutstr = get_lut(rack, crate, slot, date)
    lut = lutstr.split(",")
    with open(filename, "w") as thefile:
        for value in lut:
            thefile.write(value + "\n")

#create_board_table("fake",0,0)
#insert_lut("E169000","0,1,2,3,4,5,6", "fake",0,0)
#time.sleep(10)
#insert_lut("E169000","0,1,2,3,4,5,6,7","fake",0,0)
#file_lut_to_db("E169000","testlut.txt","fake",0,0)
#print(get_lut("fake",0,0,0))
#print(get_all_lut("E169000"))
#db_lut_to_file("fake",0,0,0)
