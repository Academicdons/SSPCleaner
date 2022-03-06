from concurrent.futures import thread
from optparse import Values
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import time
import os
import sys
import threading
from selenium.webdriver.support.events import EventFiringWebDriver, AbstractEventListener
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
import json
from selenium.common.exceptions import (
    ElementClickInterceptedException, StaleElementReferenceException, NoSuchElementException, InvalidArgumentException
)
import smtplib
from email.mime.text import MIMEText
import smtplib, ssl
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.message import EmailMessage
import re
import winsound



BASE_PATH = os.path.dirname(sys.executable)
if 'DJANGO_DEVELOPMENT' in os.environ:
    BASE_PATH = './'


def get_path(filepath):
    return os.path.join(BASE_PATH, filepath)


class MyListener(AbstractEventListener):

    def __init__(self, config):
        self.config = config


class FB_WhatsappLinksBot(object):
    def __init__(self):
        self.state = "Headless"
        self.thread_count = 2
        # data = self.openlogins()
        # link = "https://l.facebook.com/l.php?u=https%3A%2F%2Fchat.whatsapp.com%2FJiZ6zTmIFIaD8dV4nXRzfY%3Ffbclid%3DIwAR3huiuXP7m1eQNrDXCROBaeQfdPMIm1EefyLZlq0sZ3hdYVKRE5i4UuhXg&h=AT0_saz9Zt_aLONJru3E2rLiyFoSxq_SdofVouEVUvR-sjoRWx2snh19s4_XwJB56POtfPB64SKB9rc8WTQNthrlTZ3tZZqAUb45tz0sf036hWlJp9Ls_TitNUzQTpI__cHH&__tn__=H-R&c[0]=AT111Cz_506RNvW_wu1rd-9IzUem9bYiCEIVjxRd0UbfldeOW8WX3RLzG1UCTs_OdIvELTXJmr8XOadTKtJliJK8UA-iKknGGcCBiCvvjyiTcTDYJdld2EW9a2Cj4hM7x71EEzjRMRk7DcbaW3bier0TG89w6MlyEmg"

    def get_path(self, filepath):
        try:
            print("getting path")
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, filepath)

    def get_first_link(self):
        try:
            with open(self.get_path('resources\\DataBase\\new.txt'), 'r') as fin:
                linkdata = fin.read().splitlines(True)
            with open(self.get_path('resources\\DataBase\\new.txt'), 'w') as fout:
                
                fout.writelines(linkdata[1:])
                try:
                    link = linkdata[0]
                    if link == "":
                        self.get_first_link()
                    
                except IndexError:
                    mess = "Hooray..... You are done You can exit the app now"
            return link
        except UnboundLocalError:
            sys.stdout.write('\nList is empty....\nAll links are done and dusted')
            winsound.MessageBeep()
            sys.exit(0)
            
    def get_driver(self):
        chrome_options = webdriver.ChromeOptions()
        headstate = self.state
        chrome_options.add_argument("--headless")
        chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        chrome_options.add_argument('--disable-notifications')
        #chrome_options.add_argument("--disable-logging")
        path = (self.get_path("resources\\chromedriver.exe"))
        driver = webdriver.Chrome(options=chrome_options, executable_path=path)
        driver.maximize_window()
        return driver

    
    def init_bot(self):
        sys.stdout.write("\nHold On\n")
        self.openFirstDoc()
        for x in range(0, self.thread_count): 
            driver = self.get_driver()
            # self.thread = multiprocessing.Process(target=self.login, args=(driver,), name="thread_{}".format(x), )
            thread = threading.Thread(target=self.checkUrl, args=(driver,), name="thread_{}".format(x), )
            thread.daemon = False
            thread.start()
            time.sleep(3)


    def checkUrl(self, driver):
        sys.stdout.write("\nAttempting To check Url...")
        link = self.get_first_link()
        try:
            driver.get(link)
            elem = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//*[contains(text(), 'Follow Link')]")))


            elem.click()
            link = driver.current_url
            time.sleep(0.5)
        finally:
            self.checkLinkValidity(driver) 

    def checkLinkValidity(self, driver): 
        time.sleep(2)
        sys.stdout.write("\nChecking Validity of the link")
        elem = driver.find_element(By.ID, "action-icon")
        elem = elem.find_element(by=By.TAG_NAME, value="span")
        # find_element_by_tag_name("span")
        style = elem.get_attribute("style")
        if 'pps' in style and 'whatsapp' in style and 'net' in style:
            sys.stdout.write('\nLink is valid')
            self.processData(driver)
        else:
            sys.stdout.write('\nLink is not valid')
            self.checkUrl(driver)

    def processData(self, driver):
        global linksCount
        print("\nTrying to save data now")
        try:
            with open(self.get_path("resources\\workinglinks.txt")) as W:
                if driver.current_url in W.read():
                    print('\nLink already been viewed before')
                else:
                    with open(self.get_path("resources\\workinglinks.txt"), "a") as f:
                        print('\nlink Saved successfully')
                        link = driver.current_url
                        f.write(f"{link} \n \n")
                        winsound.Beep(1000, 500)
                        f.close()
        finally:
    
            self.checkUrl(driver)

    def openSecDoc(self,line):
        global AllLinksFound
        linkFound = False
        with open(self.get_path("resources\\DataBase\\AllWhatsAppURLSDB.txt")) as f:
            for data in f:
                if line in data:
                    linkFound = True
                
            if linkFound == False:
                self.dataAppend(line)
                
        

    def dataAppend(self, line):
        with open(self.get_path("resources\\DataBase\\AllWhatsAppURLSDB.txt"), "a") as f:
            f.write(f"{line} \n")
            f.close()
        with open(self.get_path("resources\\DataBase\\new.txt"), "a") as G:
            print('\nLink Not found in db...\nadding link Now..')
            G.write(f"{line} \n")


    def openFirstDoc(self):
        global AllLinksFound
        print("\nCounterchecking Link with DB")
        empty_list = ""

        with open(self.get_path('resources\\whatsAppUrls.txt')) as fp:
            for line in fp:
                time.sleep(0.5)
                self.openSecDoc(line)

        




if __name__ == '__main__':
    ed = FB_WhatsappLinksBot()
    sys.stdout.write("\n The bot is now starting...")
    ed.init_bot()
