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
    module_dir = os.path.dirname(__file__)   #get current directory
    file_path = os.path.join(module_dir, 'static/sample.txt')   #full path to text.
    try:
        st = ""
        fn = open(file_path,'rb')
        for i in fn.readlines():
            print(i)
    except:
        return HttpResponse("<H1>Error</H1>")
    # print("data=", data)
    return HttpResponse("<H1>"+st+"</H1>")


def Fetch(request):
    chromedriver = "E:\\chromedriver_win32\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options=options, executable_path=chromedriver)
    driver.maximize_window()
