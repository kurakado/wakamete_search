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


def search(trip,startNum=None,endNum=None, role=None):
 
    try:
        file="../search_history"
        f=open(file,"a")
        f.write(trip+"\n")
        f.close()
    except Exception as e:
        print(e)
    dbname = '/home/ec2-user/work/wakamete_search/database.db'
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
    sql="select * from Village_participants where trip ='{}' ".format(trip)
    if startNum:
        sql+=" and village_num > {} ".format(startNum)
    if endNum:
        sql+=" and village_num < {} ".format(endNum)
    if role:
        sql+=" and role_id = {} ".format(role)
    sql+="order by village_num"
    #sql="select village_num from Village_participants".format(sys.argv[1])
    logger.debug("execute sql: {}".format(sql))
    #print("execute sql: {}".format(sql))
    c.execute(sql)

    return c.fetchall()

if __name__ == "__main__":

    if len(sys.argv)==1:
        print("need arg")
        sys.exit(1)
    ret=search(sys.argv[1],19000,19300,1)
    print("HIT数 {}件".format(len(ret)))
    for line in ret:
        village_num=line[0]
        CN=line[2]
        role=Role(line[5]).name
        print("{}番地 CN：{} 役職：{}".format(village_num, CN , role) )
