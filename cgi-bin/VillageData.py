#! python3

import sqlite3
from logging import getLogger,Formatter,DEBUG,INFO,ERROR,StreamHandler,FileHandler
import sys
import os
import html
import shutil
from time import sleep

from bs4 import BeautifulSoup

from RoleEnum import Role,returnRole

logger = getLogger(__name__)
logger.setLevel(DEBUG)

formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')

streamHandler=StreamHandler(sys.stdout)
streamHandler.setLevel(INFO)
streamHandler.setFormatter(formatter)

fileHandler=FileHandler('villageData.log')
fileHandler.setLevel(DEBUG)
fileHandler.setFormatter(formatter)

logger.addHandler(streamHandler)
logger.addHandler(fileHandler)

#print(logger.handlers)



logger.debug("logger test")

def main(mode="debug"):
    ## DB準備
    dbname = '../database.db'
    conn = sqlite3.connect(dbname)
    c = conn.cursor()

    database_init(c,conn)

    if mode=="debug":
        #condig: utf-8
        htmlDataDir=r"/home/ec2-user/work/wakamete_search/village_data/"
        #for filename in ["18603.html", "18604.html", "18606.html"]:
        fig=0
        for filename in sorted(os.listdir(htmlDataDir)):
            filepath=htmlDataDir+filename
            if not os.path.isfile(filepath):
                logger.debug("{} is not file.".format(filepath))
                continue
            
            #htmldata=open(filepath,"r").read()
            try:
                print("open {}".format(filepath))
                htmldata=open(filepath,"r").read()
            except:
                logger.error("file read error:{}".format(filepath))
                continue
        
            try:
                ## HTMLデータの中から必要なデータを辞書型にパース
                villageData=parseVillageData(htmldata)
            
                ## DBに村データを登録
                ret=registData(c,conn,villageData)
                if ret == True:
                    shutil.move(filepath,
                                    r"../village_data/loaded/")
            except:
                shutil.move(filepath,r"../village_data/unload/")

            sleep(1)
            fig=(fig + 1) % 20
            if fig==0:
                conn.commit()
                conn.close()
                conn = sqlite3.connect(dbname)
                c = conn.cursor()

    ## DBデータをダンプ
    dumpDB(conn)

    #debug
    """
    sql="select * from Village_participants"
    print("execute sql: {}".format(sql))
    c.execute(sql)
    for line in c.fetchall():
        print(line)
    """

    conn.commit()
    ## DBコネクション終了
    conn.close()
    
def database_init(c,conn):
    """
    Villageテーブル：村情報
    Village_participantsテーブル：参加者の情報
    Roleテーブル：役職
    Campテーブル：勢力
    
    return (c,conn)
    """

    tableDatas=[{"name":"Camp",
                 "columns":"""camp_id integer"""},
                {"name":"Village",
                 "columns":"""village_num integer primary key,
                            people_num integer not null,
                            title text not null,
                            winner_camp"""},
                {"name":"Role",
                 "columns":"""role_id integer primary key,
                            camp_id integer,
                            FOREIGN KEY(camp_id) REFERENCES Camp(camp_id)"""},
                {"name":"Village_participants",
                 "columns":"""village_num integer,
                            member_id integer,
                            CN text not null,
                            HN text,
                            trip text,
                            role_id integer not null,
                            causeOfDeath integer,
                            deathDate integer,
                            primary key(village_num, member_id),
                            FOREIGN KEY(village_num) REFERENCES Village(village_num),
                            FOREIGN KEY(role_id) REFERENCES Role(role_id)"""}
                ]
    for tableData in tableDatas:
        #テーブルの存在確認
        sql="SELECT * FROM sqlite_master WHERE type='table' and name='{}'".format(tableData["name"])
        logger.debug("execute sql: {}".format(sql))
        c.execute(sql)
        if c.fetchone() == None:
            sql="CREATE TABLE {}({})".format(tableData["name"],tableData["columns"])
            logger.debug("execute sql: {}".format(sql))
            conn.execute(sql)
        else:
            logger.debug("table {} is already exist.".format(tableData["name"]))

def registData(c,conn,villageData):

    ## 既にDB登録されている村番だったら登録処理終了
    sql="select village_num from Village where village_num = {}".format(villageData["village"]["village_num"])
    logger.debug("execute sql: {}".format(sql))
    c.execute(sql)
    ret=c.fetchone()
    if ret != None:
        #print(ret)
        logger.info("village_num {} was already registed.".format(villageData["village"]["village_num"]))
        return True

    ## DB登録されていない村番だったら登録処理実行
    ## Village テーブルへの登録
    logger.info("regist village_num {} is start.".format(villageData["village"]["village_num"]))
    sql="insert into Village(village_num, people_num, title) values({},{},'{}')".format(
        villageData["village"]["village_num"],
        villageData["village"]["people_num"],
        villageData["village"]["title"]
        )
    logger.debug("execute sql: {}".format(sql))
    c.execute(sql)

    ## Village_participants テーブルへの登録
    for participantData in villageData["participants"]:
        sql=r"""insert into Village_participants(
                    village_num, member_id, CN, HN, trip, role_id)
                values({},{},'{}','{}','{}',{})""".format(
                    villageData["village"]["village_num"],
                    participantData["member_id"],
                    participantData["CN"],
                    participantData["HN"],
                    participantData["trip"],
                    participantData["Role"].value)
        logger.debug("execute sql: {}".format(sql))
        c.execute(sql)
#    conn.commit()
    return True
        
def dumpDB(conn, filename="database.dump"):
    f=open(filename,"w")
    for line in conn.iterdump():
        f.write(line)
    f.close()
    

def parseVillageData(htmldata):
    """
    sample:
    return { village: {
                village_num: 111111,
                people_num: 17,
                title: "aaa",
                winner_camp:Camp.MURA},
            participants : [{
                    member_id:"0",
                    CN:"aaa",
                    HN:"iii",
                    trip:"uuuuu",
                    Role:Role.URANAISHI,
                    CauseOfDeath:"",
                    DeathDate:4},
                {
                    member_id:"1",
                    CN:"aaa",
                    HN:"iii",
                    trip:"uuuuu",
                    Role:Role.URANAISHI,
                    CauseOfDeath:"",
                    DeathDate:4},
                {
                    member_id:"2",
                    CN:"aaa",
                    HN:"iii",
                    trip:"uuuuu",
                    Role:Role.URANAISHI,
                    CauseOfDeath:"",
                    DeathDate:4}
                ]
                
    """
    returnData=dict()

    
    soup = BeautifulSoup(htmldata,"html.parser")

#    print(soup.body.prettify())

    ### make returnData["village"]
    village=dict()
    head_title=soup.head.title.string
    village_num=head_title[:head_title.index("番")]
    village["village_num"]=village_num
    title=head_title.lstrip(str(village_num)+"番 ")
    village["title"]=html.escape(title)
    returnData["village"]=village
#    return None

    ### make returnData["participants"]
    participants_HTML_datas=soup.body.form.table.find_all("tr")[2].table.find_all("td")
    participantsDatas=list()
    ## スライスの指定で、何番目の要素から何個飛ばしで取得、ってことができる。
    ## a="1234567890"
    ## print(a[1::2])
    ## > "24680"
    for participant_HTML_data in participants_HTML_datas[1::2]:
        participantData=dict()
        if participant_HTML_data.text=="":
            continue
        tmp_flag2="CN"
        for name in participant_HTML_data.strings:
            if tmp_flag2=="CN":
                CN=html.escape(name)
                tmp_flag2="HN"
            elif tmp_flag2=="HN":
                if "◆" in name:
                    HN=html.escape(name.split("◆")[0][:-1])
                    trip=name.split("◆")[1]
                else:
                    HN=html.escape(name)
                    trip=None
                tmp_flag2="Role"
                Role=""
            elif tmp_flag2=="Role":
                Role+=name
                if "]" in Role:
                    tmp_flag2="CN"
                    break
        Role=returnRole(Role)
        participantData["CN"]=CN
        participantData["HN"]=HN
        participantData["trip"]=trip
        participantData["Role"]=Role
        participantData["member_id"]=len(participantsDatas)
        participantsDatas.append(participantData)

    village["people_num"]=len(participantsDatas)

    returnData["village"]=village
    returnData["participants"]=participantsDatas
    
    return returnData





if __name__=="__main__":
    main()

