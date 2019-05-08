# coding=utf-8
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
import mysql
import threading
import time
import sys
import json
import os
reload(sys)
sys.setdefaultencoding('utf8')
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--ignore-certificate-errors')
range2= [0, 3, 4, 5, 6]
range1=[0,1]
n = 0
obj={}
load_dict = {}
first=True
with open("configure.json", 'r') as load_f:
    load_dict = json.load(load_f)




def getqrcode():
    global n
    n += 1
    if n == 30:
        driver.refresh()
        time.sleep(2)
        os.remove(".\\public\\images\\"+load_dict[sys.argv[1]]+".png")
        
        time.sleep(2)
        driver.switch_to.frame(driver.find_element_by_xpath(
            "//*[@id='login_container']/iframe"))
        img = driver.find_element_by_class_name("qrcode")
        time.sleep(2)
        img.screenshot(".\\public\\images\\"+load_dict[sys.argv[1]]+".png")
            
        n = 0


def wxinit():
    time.sleep(3)
    global first
    if first==True:
        try:
           
            driver.find_element_by_xpath(
                "//*[@id='root']/div/span/div/main/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[8]/div/div/a[1]").click()
            changeTab()
            first=False
            os.remove(".\\public\\images\\"+load_dict[sys.argv[1]]+".png")
        except:
            
            driver.refresh()
            time.sleep(2)
            driver.find_element_by_xpath(
                "//*[@id='root']/div/span/div/main/div/div[2]/div[2]/div[2]/div[2]/table/tbody/tr/td[8]/div/div/a[1]").click()
            changeTab()
            first=False
            os.remove(".\\public\\images\\"+load_dict[sys.argv[1]]+".png")
    time.sleep(2)
    driver.find_element_by_xpath(
        "//*[@id='ad_manage']/a").click()
    time.sleep(2)
    driver.find_element_by_xpath(
        "//*[@id='wxadcontainer']/div[1]/div/div[1]/div[2]/ul/li[3]/a").click()
    time.sleep(2)
    driver.find_element_by_xpath(
        "//*[@id='wxadcontainer']/div[1]/div/div[2]/div/div[1]/div[1]/div[1]/nav/div[2]").click()    
    mysql.emptytable(load_dict[sys.argv[1]].split("-")[1])
    # mysql.emptytable("干瞪眼")
    findchannel()
    
    
    time.sleep(1200)
    wxinit()


def init():
    if driver.current_url == url:
        getqrcode()

    else:
        wxinit()
        return
   
    time.sleep(20)
    init()

def infotable():
    try:
        try:
            cols=[]
            table = driver.find_element_by_xpath(
                "//*[@id='wxadcontainer']/div[1]/div/div[2]/div/div/div[4]/div[2]/div[2]/table/tbody")
            rows = table.find_elements_by_tag_name("tr")
            for index in range(len(rows)):
                cols.append(rows[index].find_elements_by_tag_name("td"))
            return cols
        except:
            infotable()
    except:
        changeTab()
        init()
def findinfo():
    try:
        time.sleep(2)
        info=[]
        try:
            driver.find_element_by_xpath("//*[@id='wxadcontainer']/div[1]/div/div[2]/div/div/div[4]/div[3]")#换页栏
            pagenum = int(driver.find_element_by_xpath(
            "//*[@id='wxadcontainer']/div[1]/div/div[2]/div/div/div[4]/div[3]/div/span/span[1]/label[3]").text)
            curpagenum = int(driver.find_element_by_xpath(
            "//*[@id='wxadcontainer']/div[1]/div/div[2]/div/div/div[4]/div[3]/div/span/span[1]/label[1]").text)
            nextbut = driver.find_element_by_xpath(
            "//*[@id='wxadcontainer']/div[1]/div/div[2]/div/div/div[4]/div[3]/div/span/button[3]/span")
        except:
            pagenum=1
            curpagenum=1
        cols=infotable()
        for j in range(len(cols)):
            if j==0:
                continue
            for i in range(len(range2)):
                global obj
                if range2[i] == 0:
                    obj["date"] = str(cols[j][range2[i]].text)

                elif range2[i] == 3:
                    obj["consume"] = str(cols[j][range2[i]].text)

                elif range2[i] == 4:
                    obj["exposure"] = str(cols[j][range2[i]].text)

                elif range2[i] == 5:
                    obj["clicknum"] = str(cols[j][range2[i]].text)

                else:
                    obj["probability"] = str(cols[j][range2[i]].text)
                    obj["mp"] = "MP"
                    info.append(obj)
                    channel=obj["channel"]
                    imgsrc=obj["img"]
                    obj={}
                    obj["channel"]=channel  
                    obj["img"]=imgsrc  
                
        if j == len(cols)-1:
            for i in range(len(info)):
                mysql.addMPDB(info[i].values()[0], info[i].values()[1],info[i].values()[2],load_dict[sys.argv[1]].split("-")[1], info[i].values()[
                    3], info[i].values()[4], info[i].values()[5], info[i].values()[6],info[i].values()[7])
                
            if(curpagenum == pagenum):
                obj={}
                changeTab()
                return
            else:
                nextbut.click()
                findinfo()
    except:
        changeTab()
        init()

def changeTab():
    handlelist=driver.window_handles
    cur=driver.current_window_handle
    for i in handlelist:
        if i!=cur:
            driver.close()
            driver.switch_to.window(i)

def channeltable():
    try:
        try:
            newcols=[]
            tbody = driver.find_element_by_tag_name("tbody")
            time.sleep(1)    
            newrows = tbody.find_elements_by_tag_name("tr") 
            for index in range(len(newrows)):
                newcols.append(newrows[index].find_elements_by_tag_name("td"))
            return newcols
        except:
            channeltable()
    except:
        init()
def getimg(div):  
    try:
        try:        
            obj["img"]=div.find_element_by_tag_name("img").get_attribute("src")
            head=driver.find_element_by_xpath("//*[@id='main_content']/div[1]/div/div[1]/div")
            butlist=head.find_elements_by_tag_name("button")
            return butlist
        except:
            getimg(div)
    except:
        init()
def findchannel():
    try:
        newobj={}
        try:
            driver.find_element_by_xpath("//*[@id='wxadcontainer']/div[1]/div/div[2]/div/main/div[2]")#换页栏
            curpage=int(driver.find_element_by_xpath(
                "//*[@id='test_pagination']/span/span[1]/label[1]").text)
            totalpage=int(driver.find_element_by_xpath(
                "//*[@id='test_pagination']/span/span[1]/label[3]").text)
            nextbut=driver.find_element_by_xpath(
                "//*[@id='test_pagination']/span/button[3]") 
            
        except:
            curpage=1
            totalpage=1 
        newcols=channeltable()
        channeldict={}
        with open("channellist.json", 'r') as j:
            channeldict=json.load(j)
        try:
            channel=channeldict[sys.argv[1]] 
        except:
            channel=[]  
        for j in range(len(newcols)):
            for item in range(len(range1)):
                if range1[item] == 0:
                    link=newcols[j][0].find_element_by_tag_name('a')
                    cnlist= newcols[j][0].find_element_by_tag_name('a').text.split("-")
                    newobj["channel"]=False
                    for h in cnlist:
                        if  newobj["channel"]==True:
                                break
                        for k in channel:
                            if "MP"+k == h or k==h:
                                obj["channel"]=k
                                newobj["channel"]=True
                                break
                            else:
                                newobj["channel"]=False

                    
                else :
                    state= newcols[j][1].text
                
                    if state=="已暂停" or state=="已结束" or state=="投放中":
                        newobj["state"]=True
                    else:
                        newobj["state"]=False 
                    
            if newobj["channel"]==True and  newobj["state"]==True:
                time.sleep(3)
                link.click()
                time.sleep(2)
                try:    
                    div=driver.find_element_by_xpath("//*[@id='main_content']/div[1]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div")
                except:
                    link.click()
                    time.sleep(2)
                    div=driver.find_element_by_xpath("//*[@id='main_content']/div[1]/div/div[2]/div[2]/div/div/div/div/div[1]/div/div")
                butlist=getimg(div)
                time.sleep(2)
                for i in butlist:
                    if i.text=="查看数据":
                        i.click()
                        break
                time.sleep(2)
                handlelist=driver.window_handles
                cur=driver.current_window_handle
                for i in handlelist:
                    if i!=cur:
                        driver.switch_to.window(i)
                        break
                findinfo()
                time.sleep(2)
                driver.find_element_by_xpath("//*[@id='close_plan_detail']").click()#关闭div
                continue
            elif j == len(newcols)-1:
                if curpage==totalpage:
                    return  
                else:
                    nextbut.click()
                    findchannel()
            else:
                continue
    except:
        changeTab()
        init()
driver = webdriver.Chrome(chrome_options=chrome_options)#无头
url = "https://a.weixin.qq.com/adres/htmledition/agency/index.html"

# driver = webdriver.Chrome()#有头
driver.set_window_size('3100','1900')
driver.get(url)
time.sleep(2)
driver.switch_to.frame(driver.find_element_by_xpath(
    "//*[@id='login_container']/iframe"))
img = driver.find_element_by_class_name("qrcode")
time.sleep(2)
img.screenshot(".\\public\\images\\"+load_dict[sys.argv[1]]+".png")



init()
