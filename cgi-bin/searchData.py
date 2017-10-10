import sqlite3
import sys
from logging import getLogger,Formatter,DEBUG,INFO,ERROR,StreamHandler,FileHandler

from RoleEnum import Role,returnRole

logger = getLogger(__name__)
logger.setLevel(DEBUG)

formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

streamHandler=StreamHandler(sys.stdout)
streamHandler.setLevel(INFO)
streamHandler.setFormatter(formatter)

fileHandler=FileHandler('searchData.log')
fileHandler.setLevel(DEBUG)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)


def search(trip):
    dbname = 'database.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()
    """
    sql="select name from sqlite_master where type='table' order by name"
    c.execute(sql)    
    ret=c.fetchall()
    print(len(ret))
    for line in ret:
        print(line)
    """

    print("検索対象={}</br>".format(trip))
    sql="select * from Village_participants where trip ='{}' order by village_num".format(trip)
    #sql="select village_num from Village_participants".format(sys.argv[1])
    logger.debug("execute sql: {}".format(sql))
    #print("execute sql: {}".format(sql))
    c.execute(sql)

    return c.fetchall()

if __name__ == "__main__":

    if len(sys.argv)==1:
        print("need arg")
        sys.exit(1)
    ret=search(sys.argv[1])
    print("HIT数 {}件".format(len(ret)))
    for line in ret:
        village_num=line[0]
        CN=line[2]
        role=Role(line[5]).name
        print("{}番地 CN：{} 役職：{}".format(village_num, CN , role) )
