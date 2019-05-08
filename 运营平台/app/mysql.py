# coding=utf-8
import pymysql
import sys
reload(sys)
sys.setdefaultencoding('utf8')
conn = pymysql.connect(
    host="localhost", user="root", password="", database="mysql", port=3306, charset="utf8")
cursor = conn.cursor()


def addMPDB(consume,img,click,proname, probability, mp, date, channle,exposure):
    channlelist=channle.split("MP")
    if len(channlelist)>1:
        channle=channlelist[1]
    else:
        channle=channlelist[0]
    print channle
    table = "CREATE TABLE  " + proname + " (项目名 varchar(255),渠道号 varchar(255),渠道名 varchar(255),素材 varchar(255),消耗 varchar(255),曝光 varchar(255),点击 varchar(255),点击率 varchar(255),新增（授权前） varchar(255),新增（授权后） varchar(255),授权转化 varchar(255),开局账号数 varchar(255),开局率 varchar(255),人均盘数 varchar(255),日期 varchar(255))ENGINE=InnoDB DEFAULT CHARSET=utf8"
    sql = "INSERT INTO  "+proname+" (项目名,素材,日期,渠道号,渠道名,消耗,曝光,点击,点击率) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)" % (
      '"'+proname+'"','"'+img+'"', '"'+date+'"', '"'+channle+'"','"' + mp + '"', '"' + consume + '"', '"' + exposure + '"', '"' + click + '"', '"' + probability + '"')
    exsit = "SELECT table_name FROM information_schema.TABLES WHERE table_name =" +  "'"+proname+"'"+""
    try:
        if  cursor.execute(exsit)==1:
            cursor.execute(sql)
            conn.commit()
            
            print "success1"
        else :
            cursor.execute(table)
            cursor.execute(sql)
            conn.commit()
            print "success2"

    except Exception, e:
        print e

def updateMagicDB(proname,date,newsb,newzc,conversion,channel):
    # WHERE 日期=%s and 渠道号=%s
    sql=  "UPDATE " + proname + " SET 新增（授权前）=%s, 新增（授权后）=%s ,授权转化=%s WHERE 日期=%s and 渠道号=%s " %('"' + newsb + '"', '"' + newzc + '"', '"' + conversion + '"', '"' + date + '"','"' + channel + '"')
    try:
        cursor.execute(sql)
        conn.commit()
        print "update授权"
    except:
        conn.rollback()

def updateNewGamePlnum(proname,date,newgame,channel):
    # WHERE 日期=%s and 渠道号=%s
    print newgame,date
    sql=  "UPDATE " + proname + " SET 开局账号数=%s WHERE 日期=%s  and 渠道号=%s " %('"' + newgame + '"', '"' + date + '"', '"' + channel + '"')
    try:
        cursor.execute(sql)
        conn.commit()
        print "update新注册"
    except:
        conn.rollback()        
def updatePlayNum(proname,date,ps,channel):
    sql=  "UPDATE " + proname + " SET 人均盘数=%s WHERE 日期=%s and 渠道号=%s " %('"' + ps + '"', '"' + date + '"', '"' + channel + '"')        
    try:
        cursor.execute(sql)
        conn.commit()
        print "update盘数"
    except:
        conn.rollback()

def emptytable(tablename):
    sql = "delete from  "+tablename+""
    exsit = "SELECT table_name FROM information_schema.TABLES WHERE table_name =" +  "'"+tablename+"'"+""
    try:
        if cursor.execute(exsit)==1:
            cursor.execute(sql)
            conn.commit()
            print "dele success"
        else:
            return 
    except Exception, e:
        print e
def updateKaiJuLv(tablename):
    sql="SELECT 开局账号数,新增（授权后）,日期,渠道号  FROM "+tablename+" WHERE  新增（授权后） IS NOT NULL and 开局账号数 IS NOT NULL"
    
    try:
        cursor.execute(sql)
        results = cursor.fetchall()
        # print results
        if len(results)==0:
            return
        for item in results:
            
            if int(item[1])==0:
                rare="0%"
                updatesql="UPDATE " + tablename + " SET 开局率=%s WHERE 日期=%s and 渠道号=%s" %('"' + rare + '"','"' + item[2] + '"','"' + item[3] + '"')
                cursor.execute(updatesql)
                conn.commit()
                print "update 开局率"
            
            else:
                rare=str(int(round(float(item[0])/float(item[1]), 2)*100))+"%"
                updatesql="UPDATE " + tablename + " SET 开局率=%s WHERE 日期=%s and 渠道号=%s" %('"' + rare + '"','"' + item[2] + '"','"' + item[3] + '"')
                cursor.execute(updatesql)
                conn.commit()
                print "update 开局率"

        
    except Exception, e:
        print e

# addMPDB("a","aa","aaa","aaaaa", "干瞪眼", "--", "fff", "MP45114", "qqq")
# insertdict("aaaa","bbbbbbbb")
# addMagicDB("干瞪眼1","2019-02-20","10","10","100%","MP45098")
# updateNewGamePlnum("干瞪眼","2019-02-20","111","45116")
# updateKaiJuLv("干瞪眼")
