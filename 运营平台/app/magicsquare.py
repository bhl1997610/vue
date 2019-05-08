# coding=utf-8
from selenium import webdriver #webdriver
from selenium.webdriver.chrome.options import Options#无头浏览器
from PIL import Image
import mysql#数据库
import threading#定时器
import time#time.sleep代码暂停
import sys 
import re
import json
import os
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
reload(sys)
sys.setdefaultencoding('utf8')
sys.setrecursionlimit(10000)

load_dict = {}
with open("configure.json", 'r') as load_f:
    load_dict = json.load(load_f)

info = []
channeltext = []
channellsit = []
channelclick=[]
first=True
firstlable=True
n = 0
obj = {}


def refreshQrcode():
    global n
    n += 1
    if n == 12:
        driver.refresh()
        time.sleep(2)
    
        os.remove(".\\public\\images\\" +
                    load_dict[sys.argv[1]].split(",")[0]+".png")
    
        time.sleep(2)
        driver.find_element_by_xpath(
            "/html/body/div/div/div[2]/ul/li[2]").click()
        img = driver.find_element_by_class_name("qrcode")
        img.screenshot(".\\public\\images\\"+load_dict[sys.argv[1]].split(",")[0]+".png")
        
        n = 0
def init():
    if driver.current_url == url:
        refreshQrcode()
    else:
            global first
            global firstlable
            if first==True:
                time.sleep(2)
                os.remove(".\\public\\images\\" +
                    load_dict[sys.argv[1]].split(",")[0]+".png")
                time.sleep(2)
                driver.find_element_by_xpath(
                    "//*[@id='app']/div[2]/div[3]/div/div/div/div[1]/div/a[1]/div/div/div/div[1]").click()#日常分析
                
                time.sleep(2)
                table = driver.find_element_by_tag_name("tbody")
                tr = table.find_elements_by_tag_name("tr")
                td = []
                for i in tr:
                    td.append(i.find_elements_by_tag_name("td"))
                for j in td:
                    for item in j:
                        if item.text == load_dict[sys.argv[1]].split(",")[1]:
                        # if item.text == "408_670":
                            target=item
                target.click()
                first=False
            else:
                try:
                    driver.find_element_by_link_text('概况').click()
                    time.sleep(2)
                    
                
                except:
                    init()
            try:
                
                time.sleep(2)
            
                driver.find_element_by_link_text("筛选").click()
               
                time.sleep(2)
                
                lable=driver.find_elements_by_class_name("i-switch")
                for j in range(len(lable)) :#开关
                    if j==0 and firstlable==True:
                        lable[j].click()
                        firstlable=False
                        break
                
                time.sleep(2)
                textbut=driver.find_elements_by_class_name("text-btn") #不选
        
                for but in textbut:
                    if but.text=="不选":
                        but.click()
                        break
               
                div = driver.find_element_by_css_selector("div.subNav-filter-body")#总的渠道
                    
                global channellsit
                global channeltext
                
                channellsit = div.find_elements_by_tag_name("div")
                for item in channellsit:
                    channeltext.append(item.text)#获取渠道名称
                time.sleep(2)
                btn=driver.find_elements_by_class_name("layout-right") # 确定
                for i in btn:
                    if i.text=="确定":
                        i.click()
                        break
                time.sleep(2)
                try:
                    driver.find_element_by_link_text("渠道日报").click()
                except:
                    alist=driver.find_elements_by_css_selector("a.ng-binding")
                    for i in alist:
                        if i.text=="渠道日报":
                            i.click()
                            break
                time.sleep(3)
                driver.find_element_by_css_selector("div.subNav-dateRange").click()
                time.sleep(2)
                a=driver.find_elements_by_css_selector("span.month")
                for i in a:
                    try:
                        i.click()
                    except:
                        continue
                time.sleep(2)
              
                b=driver.find_elements_by_css_selector("button.applyBtn")
                for i in b:
                    try:
                        i.click()
                    except:
                        continue
            except Exception,e:
                print e
                firstlable=True
                driver.refresh()
                init()
            
                
                
          
              
           
            findchannel()
            argpalynum()
            updatenewzc()
            # 数据库更新开局率
            mysql.updateKaiJuLv(load_dict[sys.argv[1]].split(",")[0].split("-")[1])
            channeltext=[]
         
    time.sleep(5)
    init()
    
        
      

def findnewzc():
    try:
        global obj
        global info
        celllist=[]
        try:
            dlist = driver.find_elements_by_class_name("gridContentRow")
            for i in dlist:
                celllist.append(i.find_elements_by_class_name("gridCell"))
            return celllist
        except:
            findnewzc()
    except:
        init()
def meirzhclick():
    time.sleep(2)
    try:
        driver.find_element_by_class_name("fa-table").click() 
        time.sleep(2)  
        tablist = driver.find_element_by_class_name(
            "tabDashboardInner").find_elements_by_tag_name("div")
        time.sleep(2)
        for tab in tablist:
            if tab.text == "新账号每日转化数":
                tab.click()  # 新账号每日转化数
                break
    
    except:
        init()
  
def updatezc(celllist,cltext):
    global obj
    global info
    for item in celllist:
        try:
            date = item[0].text.split("-")
            date[1] = "0"+date[1]
            obj["date"] = '-'.join(date)
            obj["newgame"] = item[3].text
            obj["channel"] = cltext
            info.append(obj)
            obj = {}
        
            for item in info:
                mysql.updateNewGamePlnum(load_dict[sys.argv[1]].split(",")[0].split("-")[1], item.values()[
                    0], item.values()[1], item.values()[2])
                # mysql.updateNewGamePlnum("干瞪眼", item.values()[
                #     0], item.values()[1], item.values()[2])
                
            info = []
        except:
            continue
def findtable():
    try:
        time.sleep(3)
        try:
            driver.find_element_by_class_name("loading-error")
            return False
           
           
        except:
            table = driver.find_element_by_class_name("gridWrap")  # 表
            return table
            
    except:
        findtable()
def updatenewzc():
    try:
        driver.find_element_by_link_text('行为分析').click()  
        time.sleep(1)
        driver.find_element_by_link_text('新用户开局').click()
        time.sleep(3)
        try:
            meirzhclick()#转为表
        except:
            init()
        time.sleep(2)
        body = driver.find_element_by_xpath("/html/body")
        for cltext in channeltext:
            if re.search(load_dict[sys.argv[1]].split(",")[2], cltext) != None:
                changechannel(cltext)
                time.sleep(3)
                for i in range(17):
                        table=findtable()
                        if table==False:
                            break
                        if i == 0:
                            celllist = findnewzc()
                            updatezc(celllist,cltext)
                        ActionChains(driver).click(table).perform()
                        time.sleep(2)
                        body.send_keys(Keys.ARROW_DOWN)

                        if i == 8:
                            celllist = findnewzc()
                            updatezc(celllist,cltext)
                        if i == 16:
                            celllist = findnewzc()
                            updatezc(celllist,cltext)
    except:
        init()
                
def renjunpanshu():
    try:
        try:
            tablist = driver.find_element_by_class_name(
                "tabDashboardInner").find_elements_by_tag_name("div")
            for tab in tablist:
                if tab.text == "人均盘数-设备":
                    tab.click()  # 人均盘数
                    break
        except :
            init()
    except:
        renjunpanshu()
# 寻找svg点
def findpath():
    try:
        try:
            totaldiv = driver.find_element_by_class_name("highcharts-container")
            textdiv = totaldiv.find_element_by_tag_name("div")  # 日期 次数div
            return textdiv
           
        except:
           
            return False
    except:
        findpath()
def findsvginfo():
    try:
        try: 
            totalpath = driver.find_element_by_class_name(
                "highcharts-markers")  # svg
            paths = totalpath.find_elements_by_tag_name("path")  # 点
            return paths
        
        except:
            return False

    except:
        findsvginfo()
def argpalynum():
    try:
        driver.find_element_by_link_text('行为分析').click()   
        time.sleep(4)
        renjunpanshu()
        time.sleep(2)
        global channeltext
        for cltext in channeltext:
            if re.search(load_dict[sys.argv[1]].split(",")[2], cltext) != None:
                changechannel(cltext)
                time.sleep(5)
                textdiv = findpath()
                if textdiv==False:
                    continue
                time.sleep(2)
                sp = textdiv.find_element_by_tag_name("span")  # 日期 次数 span
                paths=findsvginfo()
                if paths==False:
                    continue
                time.sleep(2)
                for j in range(len(paths)):
                    try:
                        global obj
                        ActionChains(driver).move_to_element(paths[j]).perform()
                        time.sleep(2)
                        datesp = sp.find_element_by_tag_name("span").text
                        num = sp.find_element_by_tag_name(
                            "div").find_elements_by_tag_name("div")[1].text
                        date = datesp.split("-")
                        date[1] = "0"+date[1]
                        obj["date"] = '-'.join(date)
                        obj["channel"] = cltext
                        obj["ps"] = num
                        global info
                        info.append(obj)
                        obj = {}
                    except:
                        continue
                for item in info:
                
                    mysql.updatePlayNum(load_dict[sys.argv[1]].split(",")[0].split("-")[1], item.values()[
                        0], item.values()[1], item.values()[2])
                   
                
                info = []
    except:
        init()
def findchannel():
    try:
        channel=[]
       
        for i in channeltext:
            if re.search(load_dict[sys.argv[1]].split(",")[2], i) != None:
                channel.append(i)
                changechannel(i)
                time.sleep(5)
                findDateTable()
        channeldict={}
        with open("channellist.json", 'r') as j:
            channeldict=json.load(j)
            channeldict[str(int(sys.argv[1])-1000)]=channel
        with open("channellist.json", 'w') as f:
            json.dump(channeldict,f)
    except:
        init()

def findDateTable(): 
    try:
        info = []
        cols1 = []
        cols2 = []   
        try:
            tbody2 = driver.find_element_by_xpath(
                "//*[@id='operate-table-content-table']/tbody")
            rows2 = tbody2.find_elements_by_tag_name("tr")
            tbody1 = driver.find_element_by_xpath(
                " //*[@id='channelAnalyics']/div/div/div[2]/div/div[2]/div/table/tbody")
            rows1 = tbody1.find_elements_by_tag_name("tr")
            for i in range(len(rows1)):
                cols1.append(rows1[i].find_elements_by_tag_name("td"))
            for j in range(len(rows2)):
                cols2.append(rows2[j].find_elements_by_tag_name("td"))
            for index in range(len(cols1)):
                global obj
                obj["channel"] = cols1[index][0].get_attribute("title")
                obj["date"] = cols1[index][1].get_attribute("title")
                obj["newsb"] = cols2[index][0].text
                obj["newzc"] = cols2[index][1].text
                if int(obj["newsb"]) == 0:
                    obj["conversion"] = "0"+"%"
                else:
                    obj["conversion"] = str(
                        int(round(float(obj["newzc"])/float(obj["newsb"]), 2)*100))+"%"
                info.append(obj)
                obj = {}
                
                if index == len(cols1)-1:
                    for i in info:
                        mysql.updateMagicDB(load_dict[sys.argv[1]].split(",")[0].split("-")[1], i.values()[0], i.values()[1], i.values()[
                                            2], i.values()[3], i.values()[4])
                      
                    info = []
                    cols1 = []
                    cols2 = []
                    break
                else:
                    continue
        except:
            findDateTable()
    except:
        init()
def changechannel(i):
    try:
        time.sleep(2)
        driver.find_element_by_link_text("筛选").click()#筛选
        time.sleep(2)
        textbut=driver.find_elements_by_class_name("text-btn") #不选
    
        for but in textbut:
            if but.text=="不选":
                but.click()
                break
        global channelclick
        if channelclick==[]:
            div = driver.find_element_by_css_selector("div.subNav-filter-body")#总的渠道
            channelclick = div.find_elements_by_tag_name("div")

        time.sleep(2)
        for item in channelclick:
            if item.text == i:
                item.click()
                break
        btn=driver.find_elements_by_class_name("layout-right") # 确定
        for i in btn:
            if i.text=="确定":
                i.click()
                break
        channelclick=[]
    except:
       init()


chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
driver = webdriver.Chrome(chrome_options=chrome_options)#无头浏览器
url = "http://box.imeete.com/auth/login?redirect=http%3A%2F%2Fmc2.bianfeng.com%3A8003%2F&appid=84&advance=1&vpn=0"
# driver = webdriver.Chrome()#有头浏览器
driver.get(url)
driver.set_window_size('3100','1900')
time.sleep(2)
driver.find_element_by_xpath("/html/body/div/div/div[2]/ul/li[2]").click()
img = driver.find_element_by_class_name("qrcode")
time.sleep(2)
img.screenshot(".\\public\\images\\"+load_dict[sys.argv[1]].split(",")[0]+".png")

init()

                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                    