import sqlite3 as lite
import threading
import uuid
import os


class csvfile(object):
    def __init__(self, path, todb):
        self.path = path
        self.todb = todb

    def __repr__(self):
        return "" % (self.path, self.todb)

def by_key(csvfile):
    return csvfile.todb

def selectfromdb(sql,namedb,fromdb, todb, event_for_wait, event_for_set):
    #event_for_wait.wait()
    #event_for_wait.clear()
    con = lite.connect(namedb)
    cur = con.cursor()
    cur.execute(sql+" limit "+str(fromdb)+","+str(todb))
    uid = str(uuid.uuid4())
    tempfile = open('/tmp/tempcsv-'+str(todb)+"-" + uid, 'w')
    s = ''
    i = 0
    for col in cur.description:
        if (i > 2):
            s = s + ',' + col[0]
        else:
            s = col[0]
        i = i + 1
    tempfile.write(s + '\n')
    for row in cur.fetchall():
        s = ''
        i = 0
        for col in row:
            if (i > 2):
                s = s + ',' + str(col)
            else:
                s = str(col)
            i = i + 1
        tempfile.write(s + '\n')
    tempfile.close()
    #con.commit()
    #event_for_set.set()

if __name__ == '__main__':
    namedb = "/home/rootkit/forarduino.db"
    sqlfile = "/home/rootkit/script"
    f= open(sqlfile,'r')
    sql = f.read()
    #con = lite.connect(namedb)
    #cur = con.cursor()
    listthread = []
    eold = threading.Event()
    firste = eold
    batch_size = 1000
    size = 40000
    i=0
    while i<size:
        e = threading.Event()
        listthread.append(threading.Thread(target=selectfromdb, args=(sql,namedb,i, i + batch_size-1,eold,e)))
        eold = e
        i = i + batch_size

    for thread in listthread:
        thread.start()
    #firste.set()
    exit = False
    while exit==False:
        exit = True
        for th in listthread:
            if(th.isAlive()):
                exit = False
    listfiles=[]
    for files in os.walk("/tmp/"):
        for file in files:
            if ((file.find("tempcsv-")!=-1)):
                todb = file.split('-')
                listfiles.append(csvfile(file,int(todb[1])))
    reslistfiles = sorted(listfiles,key = by_key)
    fres = open("outthread.csv","w")
    for resfile in reslistfiles:
        f = open("/tmp"+resfile,'r')
        fres.write(f.read())
        f.close()
        os.system("rm /tmp/"+resfile)
    fres.close()
