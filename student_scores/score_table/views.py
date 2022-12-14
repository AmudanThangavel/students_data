import datetime
from turtle import update
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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict
from .views import *
from django.templatetags.static import static
import heapq
import platform
import pytz

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
    if request.user.is_authenticated:
        module_dir = os.path.dirname(__file__)  # get current directory
        # full path to text.
        file_path = os.path.join(module_dir, 'static/sample.txt')
        try:
            st = ""
            run_selenium()
            fn = open(file_path, 'rb')
            for i in fn.readlines():
                st += (bytes.decode(i)+"<br>")

        except:
            return HttpResponse("<H1>Error</H1>")
        # print("data=", data)
        return HttpResponse("<H1>"+st+"</H1>")

    else:
        return redirect("/")


def run_selenium():
        th=0
        while(th!=1):
            try:
                module_dir = os.path.dirname(__file__)  # get current directory
                # full path to text.
                chromedriver = ""
                if('mac' in platform.platform()):
                    chromedriver = os.path.join(module_dir, 'static/chromedriver')
                else:
                    chromedriver = os.path.join(module_dir, 'static/chromedriver.exe')
                options = webdriver.ChromeOptions()
                options.add_experimental_option('excludeSwitches', ['enable-logging'])
                driver = webdriver.Chrome(
                    options=options, executable_path=chromedriver)
                driver.minimize_window()
                DriverWait(driver, "https://www.interviewbit.com/users/sign_in/")
                driver.find_element(
                    'xpath', '//input[@id = "user_email_field"]').send_keys("cdczoom@kpriet.ac.in")
                driver.find_element(
                    'xpath', '//input[@id = "user_password_field"]').send_keys("12345678")
                driver.find_element(
                    'xpath', '//input[@data-gtm-element = "login"]').click()
                id1, score = [], []
                for page in range(1, 13):
                    DriverWait(
                        driver, "https://www.interviewbit.com/leaderboard/?followers=1&page="+str(page))
                    for i in driver.find_elements(By.TAG_NAME, "a"):
                        try:
                            if str(i.get_attribute('href')).count('profile') > 0 and str(i.get_attribute('href')).count('cdc-zoom') == 0:
                                #                 print(i.get_attribute('href'),i.text)
                                id1.append(i.get_attribute('href')[
                                        i.get_attribute('href').rindex('/')+1:])
                        except:
                            pass
                    for i in driver.find_elements(By.TAG_NAME, "tr"):
                        try:
                            if i.text != 'Rank User Level Streak Score':
                                score.append(int(i.text[i.text.rindex(' ')+1:]))
                        except:
                            pass
                print(id1, score)
                for i, j in zip(id1, score):
                    try:
                        obj = students_data.objects.get(roll_no=i.upper())
                        obj.score = j
                        obj.name = obj.name.upper()
                        obj.updated_at = datetime.datetime.now()
                        obj.save()
                        pass
                    except:
                        print(i)
                driver.close()
            except:
                print(sys.exc_info())
            time.sleep(600)
        else:
            return redirect('/score/')


def Fetch(request):
    module_dir = os.path.dirname(__file__)  # get current directory
    chromedriver = os.path.join(module_dir, 'static/chromedriver.exe')
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=chromedriver)
    driver.maximize_window()


def ScoreTable(request):
    d = {}
    top10mem = []
    top10team = []
    top10score = []
    teamScore = students_data.objects.all()
    
    temp = students_data.objects.all()
    m = max([i.team_no for i in temp])
    sc = list(set([j.score for j in temp]))
    top10 = heapq.nlargest(10, sc)
    for data in top10:
        b = students_data.objects.filter(score=data)
        l = []
        scr = []
        for iter in b:
            scr.append(int(iter.score))
            l.append((iter.name).ljust(30)+(iter.department))
        top10mem.append(l)
        top10score.append(scr)
    count = {}
    for i in range(1, m+1):
        fl = students_data.objects.filter(team_no=i)
        c = students_data.objects.filter(team_no=i).count()
        sum = 0
        for j in fl:
            sum += int(j.score)
        d[i] = round(sum/c,2)
        count[i] = c
    a = dict(reversed(sorted(d.items(), key=lambda item: item[1])))
    print("a",a)
    x = 0
    for i in a:
        top10team.append([str(i).zfill(2),str(a[i])])

        x += 1
        if x == 10:
            break
    print(top10team)
    print(top10mem)
    print(top10score)
    rng = [i for i in range(1,11)]

    #Time
    updatedTime = datetime.datetime.now(pytz.timezone('Asia/Kolkata'))
    # uptimeobj = students_data.objects.get(roll_no = "20EC023")
    # updatedTime = uptimeobj.updated_at
    print(str(updatedTime))
    # timestr = str(updatedTime.day) + "-" + str(updatedTime.month) + "Time : " + str(updatedTime.hour) + ":" + str(updatedTime.minute )
    timestr = "Updated at " +  updatedTime.strftime('%Y:%m:%d %H:%M:%S')
    # print(times)

    return render(request, 'scores.html', {"students_data": teamScore, "rank": a, "count": count, "top10team": top10team, "top10per": top10mem, "top10score": top10score, "range": rng, "updateTime" : timestr})
