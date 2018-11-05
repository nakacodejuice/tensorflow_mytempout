import sqlite3 as lite
import threading
import uuid

namedb = "/home/rootkit/forarduino.db"
con = lite.connect(namedb)
cur = con.cursor()
cur.execute("select * from mytemp"+" limit "+str(0)+","+str(100))
uid = str(uuid.uuid4())
tempfile = open('/tmp/tempcsv'+uid,'w')
s=''
i=0
for col in cur.description:
    if(i>2):
        s=s+','+col[0]
    else:
        s=col[0]
    i=i+1
tempfile.write(s+'\n')
for row in cur.fetchall():
    s= ''
    i=0
    for col in row:
        if(i>2):
            s= s+','+str(col)
        else:
            s = str(col)
        i=i+1
    tempfile.write(s+'\n')
tempfile.close()
con.commit()