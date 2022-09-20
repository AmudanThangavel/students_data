<<<<<<< Updated upstream
=======
from django.shortcuts import render,redirect
from django.http import HttpResponse
from .models import students_data
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login , logout
from django.contrib.auth.models import User
from django.template import RequestContext
import re,random, time, openpyxl, os,sys
from openpyxl import workbook,load_workbook
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from collections import defaultdict
from .views import *
from django.contrib.staticfiles.storage import staticfiles_storage


def DriverWait(driver,link):
    driver.get(link)
    timeout = 5
    try:
        element_present = EC.presence_of_element_located((By.CLASS_NAME, 'dummy'))
        WebDriverWait(driver, timeout).until(element_present)
    except TimeoutException:
        #print(link,"Not found")
        pass

def driver_scroll(driver):
    lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
    match=False
    while(match==False):
        lastCount = lenOfPage
        time.sleep(5)
        lenOfPage = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);var lenOfPage=document.body.scrollHeight;return lenOfPage;")
        if lastCount==lenOfPage:
            match=True

def index(request):
    fle_url = staticfiles_storage.url('')


def Fetch(request):
    chromedriver = "E:\\chromedriver_win32\\chromedriver.exe"
    options = webdriver.ChromeOptions()
    options.add_experimental_option('excludeSwitches', ['enable-logging'])
    driver = webdriver.Chrome(options = options,executable_path=chromedriver)
    driver.maximize_window()
>>>>>>> Stashed changes
