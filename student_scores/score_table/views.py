from django.shortcuts import render, redirect
from django.http import HttpResponse
from accounts.models import students_data
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.template import RequestContext
import re
import random
import time
import openpyxl
import os
import sys
from openpyxl import workbook, load_workbook
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict
from .views import *
from django.templatetags.static import static
import heapq

# imports for rendering the table
from accounts.models import students_data


def DriverWait(driver, link):
    driver.get(link)
    timeout = 5
    try:
        element_present = EC.presence_of_element_located(
            (By.CLASS_NAME, 'dummy'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        #print(link,"Not found")
        pass


def driver_scroll(driver):
    lenOfPage = driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match = False
    while(match == False):
        lastCount = lenOfPage
        time.sleep(5)
        lenOfPage = driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount == lenOfPage:
            match = True

# Create your views here.


def index(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    # full path to text.
    file_path = os.path.join(module_dir, 'static/sample.txt')
    try:
        st = ""
        run_selenium()
        fn = open(file_path,'rb')
        for i in fn.readlines():
            st += (bytes.decode(i)+"<br>")
    except:
        return HttpResponse("<H1>Error</H1>")
    # print("data=", data)
    return HttpResponse("<H1>"+st+"</H1>")

def run_selenium():
    try:
        module_dir = os.path.dirname(__file__)   #get current directory
        chromedriver = os.path.join(module_dir, 'static/chromedriver.exe')   #full path to text.
        options = webdriver.ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        driver = webdriver.Chrome(options = options,executable_path=chromedriver)
        driver.minimize_window()
        DriverWait(driver,"https://www.interviewbit.com/users/sign_in/")
        driver.find_element_by_xpath('//input[@id = "user_email_field"]').send_keys("cdczoom@kpriet.ac.in")
        driver.find_element_by_xpath('//input[@id = "user_password_field"]').send_keys("12345678")
        driver.find_element_by_xpath('//input[@data-gtm-element = "login"]').click()
        id1,score=[],[]
        for page in range(1,12):
            DriverWait(driver,"https://www.interviewbit.com/leaderboard/?followers=1&page="+str(page))
            for i in driver.find_elements_by_tag_name("a"):
                try:
                    if str(i.get_attribute('href')).count('profile')>0 and str(i.get_attribute('href')).count('cdc-zoom')==0:
        #                 print(i.get_attribute('href'),i.text)
                        id1.append(i.get_attribute('href')[i.get_attribute('href').rindex('/')+1:])
                except:
                    pass
            for i in driver.find_elements_by_tag_name("tr"):
                try:
                    if i.text!='Rank User Level Streak Score':
                        score.append(int(i.text[i.text.rindex(' ')+1:]))
                except:
                    pass
        print(id1,score)
        for i,j in zip(id1,score):
            try:
                obj = students_data.objects.get(roll_no=i.upper())
                obj.score = j
                obj.name = obj.name.upper()
                obj.save()
                pass
            except:
                print(i)
    except:
        print(sys.exc_info())
    
    
def Fetch(request):
    chromedriver = "E:\\chromedriver_win32\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=chromedriver)
    driver.maximize_window()


def ScoreTable(request):
    d ={}
    top10mem =[]
    top10team = []
    teamScore = students_data.objects.all()
    temp = students_data.objects.all()
    m = max([i.team_no for i in temp])
    sc = list(set([ j.score for  j in temp]))
    top10 = heapq.nlargest(10,sc)
    for data in top10:
        b =students_data.objects.filter(score = data)
        l =[]
        for iter in b:
            l.append(iter.name)
        top10mem.append(l)
    count={}
    for i in range(1,m+1):
        fl = students_data.objects.filter(team_no = i)
        c = students_data.objects.filter(team_no = i).count()
        sum =0
        for j in fl:
            sum+=int(j.score)
        d[i] = sum/c
        count[i] = c
    a =dict(reversed(sorted(d.items(), key=lambda item: item[1])))
   
    x =0
    for i in a.keys():
        top10team.append(i)
        x+=1
        if x ==10:
            break
    print(top10team)
    print(top10mem)
    return render(request, 'scores.html', {"students_data": teamScore, "rank" : a, "count" : count, "top10per" : top10mem,'top10team':top10team})
